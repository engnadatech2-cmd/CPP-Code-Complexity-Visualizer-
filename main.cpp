#include "comment_stripper.h"
#include "metrics_calculator.h"
#include "dependency_graph.h"
#include "json_exporter.h"

#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <dirent.h>
#include <sys/stat.h>
#include <algorithm>
#include <stdexcept>
#include <iomanip>

// ---------------------------------------------------------------------------
// Terminal color codes
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
static std::string readFile(const std::string& path) {
    std::ifstream file(path, std::ios::binary);
    if (!file.is_open()) {
        throw std::runtime_error("Cannot open file: " + path);
    }
    std::ostringstream ss;
    ss << file.rdbuf();
    return ss.str();
}

// ---------------------------------------------------------------------------
// Utility: collect all .cpp and .h files in a directory
// ---------------------------------------------------------------------------
static std::vector<std::string> collectCppFiles(const std::string& dir) {
    std::vector<std::string> files;
    DIR* dp = opendir(dir.c_str());
    if (!dp) return files;
    struct dirent* entry;
    while ((entry = readdir(dp)) != nullptr) {
        std::string name = entry->d_name;
        if (name == "." || name == "..") continue;
        std::string full = dir + "/" + name;
        std::string ext = name.size() > 4 ? name.substr(name.rfind('.')) : "";
        if (ext == ".cpp" || ext == ".h" || ext == ".hpp" || ext == ".cc")
            files.push_back(full);
    }
    closedir(dp);
    std::sort(files.begin(), files.end());
    return files;
}

// ---------------------------------------------------------------------------
// Utility: draw a simple progress bar string
// ---------------------------------------------------------------------------
static std::string progressBar(int complexity, int maxComplexity, int width = 10) {
    if (maxComplexity == 0) return std::string(width, '-');
    const int filled = static_cast<int>(
        (static_cast<double>(complexity) / maxComplexity) * width
    );
    std::string bar;
    for (int i = 0; i < width; ++i) {
        bar += (i < filled) ? '#' : '-';
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
    if (risk == "high")   return "! HIGH  ";
    if (risk == "medium") return "~ MEDIUM";
    return "* LOW   ";
}

// ---------------------------------------------------------------------------
// printHelp
// ---------------------------------------------------------------------------
static void printHelp(const char* programName) {
    std::cout << Color::BOLD << Color::CYAN
              << "\nC++ Code Complexity Visualizer v1.0.0\n"
              << Color::RESET
              << "\nUsage:\n"
              << "  " << programName << " --path <dir> [--name <name>] [--output <file>]\n\n"
              << "Options:\n"
              << "  --path   <dir>   Directory containing .cpp/.h files to analyze\n"
              << "  --name   <name>  Project name (default: directory basename)\n"
              << "  --output <file>  Output JSON path (default: output/output.json)\n"
              << "  --help           Show this help message\n\n"
              << "Example:\n"
              << "  " << programName << " --path ./src --output report.json\n\n";
}

// ---------------------------------------------------------------------------
// enableAnsiColors - Windows-specific
// ---------------------------------------------------------------------------
#ifdef _WIN32
#include <windows.h>
static void enableAnsiColors() {
    HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
    DWORD dwMode = 0;
    GetConsoleMode(hOut, &dwMode);
    dwMode |= 0x0004;
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

    struct stat _s;
    if (stat(inputPath.c_str(), &_s) != 0 || !(_s.st_mode & S_IFDIR)) {
        std::cerr << Color::RED
                  << "Error: Directory does not exist: " << inputPath << "\n"
                  << Color::RESET;
        return 1;
    }

    if (projectName.empty()) {
        projectName = inputPath;
        size_t p = projectName.find_last_of("/\\");
        if (p != std::string::npos) projectName = projectName.substr(p + 1);
        if (projectName.empty()) projectName = "MyProject";
    }

    mkdir("output");

    std::cout << "\n"
              << Color::BOLD << Color::CYAN
              << "C++ Code Complexity Visualizer\n"
              << Color::RESET
              << "================================\n\n"
              << "Analyzing: " << Color::BOLD << inputPath
              << Color::RESET << "\n";

    const auto files = collectCppFiles(inputPath);
    if (files.empty()) {
        std::cerr << Color::YELLOW
                  << "Warning: No .cpp/.h files found in " << inputPath << "\n"
                  << Color::RESET;
        return 1;
    }
    std::cout << "Found " << Color::BOLD << files.size() << Color::RESET << " file(s)...\n\n";

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
        const FileMetrics metrics  = calculator.analyze(raw, stripped, filePath);

        const auto includes = depGraph.extractIncludes(raw);
        depGraph.addFile(metrics.name, includes);

        allMetrics.push_back(metrics);
        maxComplexity = std::max(maxComplexity, metrics.complexity_score);
    }

    for (const auto& fm : allMetrics) {
        const std::string bar = progressBar(fm.complexity_score, maxComplexity);
        const char* color     = riskColor(fm.risk);
        const char* symbol    = riskSymbol(fm.risk);

        std::string paddedName = fm.name;
        if (paddedName.size() < 24) paddedName += std::string(24 - paddedName.size(), ' ');
        if (paddedName.size() > 24) paddedName = paddedName.substr(0, 21) + "...";

        std::cout << "  " << Color::GREEN << "* " << Color::RESET
                  << Color::BOLD << paddedName << Color::RESET
                  << " [" << color << bar << Color::RESET << "] "
                  << std::setw(2) << fm.functions.size() << " function(s) | "
                  << "Complexity: " << Color::BOLD << std::setw(4) << fm.complexity_score
                  << Color::RESET << "  | "
                  << color << symbol << Color::RESET << "\n";
    }

    int totalFunctions  = 0;
    int highFuncs = 0, medFuncs = 0, lowFuncs = 0;
    int highFiles = 0, medFiles = 0, lowFiles = 0;
    int totalComplexity = 0;
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

    std::cout << "\n================================\n"
              << Color::BOLD << "Summary:\n" << Color::RESET
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
        std::cout << "\n" << Color::RED << "Riskiest Function: "
                  << Color::BOLD << riskiestFunc << "()"
                  << Color::RESET << " in " << Color::BOLD << riskiestFile
                  << Color::RESET << " (complexity: " << Color::RED << riskiestCC
                  << Color::RESET << ")\n";
    }

    try {
        exporter.exportToFile(allMetrics, depGraph, projectName, outputPath);
        std::cout << "\n" << Color::GREEN << "Report saved: "
                  << Color::BOLD << outputPath << Color::RESET << "\n";
    } catch (const std::exception& e) {
        std::cerr << Color::RED << "Error writing JSON: " << e.what() << Color::RESET << "\n";
        return 1;
    }

    std::cout << "\n" << Color::CYAN
              << "Next step - generate visual report:\n"
              << Color::BOLD
              << "   python visualizer/html_generator.py " << outputPath << "\n"
              << Color::RESET << "\n";

    return 0;
}
