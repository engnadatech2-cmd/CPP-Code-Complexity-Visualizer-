#include "comment_stripper.h"
#include "metrics_calculator.h"
#include "dependency_graph.h"
#include "json_exporter.h"

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <filesystem>
#include <algorithm>
#include <stdexcept>
#include <iomanip>

namespace fs = std::filesystem;

// ---------------------------------------------------------------------------
// Terminal color codes (ANSI — work on Windows 10+ with VT mode)
// ---------------------------------------------------------------------------
namespace Color {
    constexpr const char* RESET   = "\033[0m";
    constexpr const char* RED     = "\033[31m";
    constexpr const char* YELLOW  = "\033[33m";
    constexpr const char* GREEN   = "\033[32m";
    constexpr const char* CYAN    = "\033[36m";
    constexpr const char* BOLD    = "\033[1m";
    constexpr const char* WHITE   = "\033[37m";
}

// ---------------------------------------------------------------------------
// Utility: read a file into a string
// ---------------------------------------------------------------------------
static std::string readFile(const fs::path& path) {
    std::ifstream file(path, std::ios::binary);
    if (!file.is_open()) {
        throw std::runtime_error("Cannot open file: " + path.string());
    }
    std::ostringstream ss;
    ss << file.rdbuf();
    return ss.str();
}

// ---------------------------------------------------------------------------
// Utility: collect all .cpp and .h files in a directory (recursive)
// ---------------------------------------------------------------------------
static std::vector<fs::path> collectCppFiles(const fs::path& dir) {
    std::vector<fs::path> files;
    for (const auto& entry : fs::recursive_directory_iterator(dir)) {
        if (!entry.is_regular_file()) continue;
        const auto ext = entry.path().extension().string();
        if (ext == ".cpp" || ext == ".h" || ext == ".hpp" || ext == ".cc") {
            files.push_back(entry.path());
        }
    }
    std::sort(files.begin(), files.end());
    return files;
}

// ---------------------------------------------------------------------------
// Utility: draw a simple progress bar string
// ---------------------------------------------------------------------------
static std::string progressBar(int complexity, int maxComplexity, int width = 10) {
    if (maxComplexity == 0) {
        std::string empty;
        for (int i = 0; i < width; ++i) empty += "░";
        return empty;
    }
    const int filled = static_cast<int>(
        (static_cast<double>(complexity) / maxComplexity) * width
    );
    std::string bar;
    for (int i = 0; i < width; ++i) {
        bar += (i < filled) ? "█" : "░";
    }
    return bar;
}

// ---------------------------------------------------------------------------
// Utility: risk color
// ---------------------------------------------------------------------------
static const char* riskColor(const std::string& risk) {
    if (risk == "high")   return Color::RED;
    if (risk == "medium") return Color::YELLOW;
    return Color::GREEN;
}

// ---------------------------------------------------------------------------
// Utility: risk symbol
// ---------------------------------------------------------------------------
static const char* riskSymbol(const std::string& risk) {
    if (risk == "high")   return "⚠ HIGH  ";
    if (risk == "medium") return "~ MEDIUM";
    return "✓ LOW   ";
}

// ---------------------------------------------------------------------------
// printHelp
// ---------------------------------------------------------------------------
static void printHelp(const char* programName) {
    std::cout << Color::BOLD << Color::CYAN
              << "\n🔍 C++ Code Complexity Visualizer v1.0.0\n"
              << Color::RESET
              << "\nUsage:\n"
              << "  " << programName << " --path <dir> [--name <name>] [--output <file>]\n\n"
              << "Options:\n"
              << "  --path   <dir>   Directory containing .cpp/.h files to analyze\n"
              << "  --name   <name>  Project name (default: directory basename)\n"
              << "  --output <file>  Output JSON path (default: output/output.json)\n"
              << "  --help           Show this help message\n\n"
              << "Example:\n"
              << "  " << programName << " --path ./HospitalSystem --name \"Hospital System\" --output report.json\n\n"
              << "After running, generate the visual report:\n"
              << "  python visualizer/html_generator.py output/output.json\n\n";
}

// ---------------------------------------------------------------------------
// enableAnsiColors — Windows-specific: enable VT100 escape codes
// ---------------------------------------------------------------------------
#ifdef _WIN32
#include <windows.h>
static void enableAnsiColors() {
    HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    DWORD dwMode = 0;
    GetConsoleMode(hOut, &dwMode);
    dwMode |= ENABLE_VIRTUAL_TERMINAL_PROCESSING;
    SetConsoleMode(hOut, dwMode);
}
#else
static void enableAnsiColors() {}
#endif

// ---------------------------------------------------------------------------
// main
// ---------------------------------------------------------------------------
int main(int argc, char* argv[]) {
    enableAnsiColors();

    // ── Parse CLI arguments ─────────────────────────────────────────────
    std::string inputPath;
    std::string projectName;
    std::string outputPath = "output/output.json";

    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        if (arg == "--help" || arg == "-h") {
            printHelp(argv[0]);
            return 0;
        } else if (arg == "--path" && i + 1 < argc) {
            inputPath = argv[++i];
        } else if (arg == "--name" && i + 1 < argc) {
            projectName = argv[++i];
        } else if (arg == "--output" && i + 1 < argc) {
            outputPath = argv[++i];
        } else {
            std::cerr << Color::RED << "Unknown argument: " << arg << Color::RESET << "\n";
            printHelp(argv[0]);
            return 1;
        }
    }

    if (inputPath.empty()) {
        std::cerr << Color::RED << "Error: --path is required.\n" << Color::RESET;
        printHelp(argv[0]);
        return 1;
    }

    // ── Validate input directory ─────────────────────────────────────────
    const fs::path projectDir = fs::path(inputPath);
    if (!fs::exists(projectDir) || !fs::is_directory(projectDir)) {
        std::cerr << Color::RED
                  << "Error: Directory does not exist: " << inputPath << "\n"
                  << Color::RESET;
        return 1;
    }

    // Default project name = directory basename
    if (projectName.empty()) {
        projectName = projectDir.filename().string();
        if (projectName.empty() || projectName == ".") {
            projectName = fs::absolute(projectDir).filename().string();
        }
    }

    // Ensure output directory exists
    const fs::path outDir = fs::path(outputPath).parent_path();
    if (!outDir.empty() && !fs::exists(outDir)) {
        fs::create_directories(outDir);
    }

    // ── Banner ───────────────────────────────────────────────────────────
    std::cout << "\n"
              << Color::BOLD << Color::CYAN
              << "🔍 C++ Code Complexity Visualizer\n"
              << Color::RESET
              << "════════════════════════════════════\n\n"
              << "Analyzing: " << Color::BOLD << fs::absolute(projectDir).string()
              << Color::RESET << "\n";

    // ── Collect files ────────────────────────────────────────────────────
    const auto files = collectCppFiles(projectDir);
    if (files.empty()) {
        std::cerr << Color::YELLOW
                  << "Warning: No .cpp/.h files found in " << inputPath << "\n"
                  << Color::RESET;
        return 1;
    }
    std::cout << "Found " << Color::BOLD << files.size() << Color::RESET << " file(s)...\n\n";

    // ── Analyze each file ────────────────────────────────────────────────
    CommentStripper   stripper;
    MetricsCalculator calculator;
    DependencyGraph   depGraph;
    JsonExporter      exporter;

    std::vector<FileMetrics> allMetrics;
    allMetrics.reserve(files.size());

    int maxComplexity = 0;
    for (const auto& filePath : files) {
        const std::string raw      = readFile(filePath);
        const std::string stripped = stripper.strip(raw);
        const FileMetrics metrics  = calculator.analyze(raw, stripped, filePath.string());

        const auto includes = depGraph.extractIncludes(raw);
        depGraph.addFile(metrics.name, includes);

        allMetrics.push_back(metrics);
        maxComplexity = std::max(maxComplexity, metrics.complexity_score);
    }

    // ── Print per-file results ───────────────────────────────────────────
    for (const auto& fm : allMetrics) {
        const std::string bar    = progressBar(fm.complexity_score, maxComplexity);
        const char* color        = riskColor(fm.risk);
        const char* symbol       = riskSymbol(fm.risk);

        // Pad filename to 24 chars
        std::string paddedName = fm.name;
        if (paddedName.size() < 24) paddedName += std::string(24 - paddedName.size(), ' ');
        if (paddedName.size() > 24) paddedName = paddedName.substr(0, 21) + "...";

        std::cout << "  " << Color::GREEN << "✓ " << Color::RESET
                  << Color::BOLD << paddedName << Color::RESET
                  << " [" << color << bar << Color::RESET << "] "
                  << std::setw(2) << fm.functions.size() << " function(s) | "
                  << "Complexity: " << Color::BOLD << std::setw(4) << fm.complexity_score
                  << Color::RESET << "  | "
                  << color << symbol << Color::RESET << "\n";
    }

    // ── Summary ──────────────────────────────────────────────────────────
    int totalFunctions  = 0;
    int highFuncs       = 0, medFuncs = 0, lowFuncs = 0;
    int highFiles       = 0, medFiles = 0, lowFiles = 0;
    int totalComplexity = 0;
    int globalMaxCC     = 0;
    std::string riskiestFunc, riskiestFile;
    int riskiestCC = 0;

    for (const auto& fm : allMetrics) {
        totalFunctions += static_cast<int>(fm.functions.size());
        if (fm.risk == "high")        ++highFiles;
        else if (fm.risk == "medium") ++medFiles;
        else                          ++lowFiles;

        for (const auto& func : fm.functions) {
            totalComplexity += func.complexity;
            if (func.risk == "high")        ++highFuncs;
            else if (func.risk == "medium") ++medFuncs;
            else                            ++lowFuncs;

            if (func.complexity > riskiestCC) {
                riskiestCC   = func.complexity;
                riskiestFunc = func.name;
                riskiestFile = fm.name;
            }
        }
    }

    const double avgCC = totalFunctions > 0
                       ? static_cast<double>(totalComplexity) / totalFunctions
                       : 0.0;

    std::cout << "\n════════════════════════════════════\n"
              << Color::BOLD << "📊 Summary:\n" << Color::RESET
              << "   Total Functions : " << Color::BOLD << totalFunctions << Color::RESET << "\n"
              << "   Avg Complexity  : " << Color::BOLD
              << std::fixed << std::setprecision(1) << avgCC << Color::RESET << "\n"
              << "   High Risk       : " << Color::RED    << highFiles << " file(s)"
              << Color::RESET << " (" << highFuncs << " functions)\n"
              << "   Medium Risk     : " << Color::YELLOW << medFiles  << " file(s)"
              << Color::RESET << " (" << medFuncs  << " functions)\n"
              << "   Low Risk        : " << Color::GREEN  << lowFiles  << " file(s)"
              << Color::RESET << " (" << lowFuncs  << " functions)\n";

    if (!riskiestFunc.empty()) {
        std::cout << "\n" << Color::RED << "🔴 Riskiest Function: "
                  << Color::BOLD << riskiestFunc << "()"
                  << Color::RESET << " in " << Color::BOLD << riskiestFile
                  << Color::RESET << " (complexity: " << Color::RED << riskiestCC
                  << Color::RESET << ")\n";
    }

    // ── Export JSON ──────────────────────────────────────────────────────
    try {
        exporter.exportToFile(allMetrics, depGraph, projectName, outputPath);
        std::cout << "\n" << Color::GREEN << "✅ Report saved: "
                  << Color::BOLD << outputPath << Color::RESET << "\n";
    } catch (const std::exception& e) {
        std::cerr << Color::RED << "Error writing JSON: " << e.what() << Color::RESET << "\n";
        return 1;
    }

    // ── Next step hint ───────────────────────────────────────────────────
    std::cout << "\n" << Color::CYAN
              << "▶  Generate visual report:\n"
              << Color::BOLD
              << "   python visualizer/html_generator.py " << outputPath << "\n"
              << Color::RESET << "\n";

    return 0;
}
