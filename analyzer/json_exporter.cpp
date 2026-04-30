#include "json_exporter.h"
#include <fstream>
#include <sstream>
#include <stdexcept>
#include <algorithm>
#include <numeric>
#include <ctime>
#include <iomanip>

// ---------------------------------------------------------------------------
// JsonExporter::exportToFile
// ---------------------------------------------------------------------------
void JsonExporter::exportToFile(const std::vector<FileMetrics>& files,
                                 const DependencyGraph& graph,
                                 const std::string& projectName,
                                 const std::string& outputPath) const {
    const std::string json = buildJson(files, graph, projectName);

    std::ofstream out(outputPath);
    if (!out.is_open()) {
        throw std::runtime_error("JsonExporter: Cannot open output file: " + outputPath);
    }
    out << json;
    if (!out.good()) {
        throw std::runtime_error("JsonExporter: Write failed for: " + outputPath);
    }
}

// ---------------------------------------------------------------------------
// JsonExporter::buildJson
// ---------------------------------------------------------------------------
std::string JsonExporter::buildJson(const std::vector<FileMetrics>& files,
                                     const DependencyGraph& graph,
                                     const std::string& projectName) const {
    std::ostringstream j;
    j << "{\n";
    j << indent(1) << "\"project\": "          << "\"" << escapeString(projectName) << "\",\n";
    j << indent(1) << "\"analyzed_at\": "       << "\"" << currentTimestamp()        << "\",\n";
    j << indent(1) << "\"analyzer_version\": "  << "\"1.0.0\",\n";

    // Summary
    j << indent(1) << "\"summary\": " << buildSummary(files) << ",\n";

    // Files array
    j << indent(1) << "\"files\": [\n";
    for (std::size_t fi = 0; fi < files.size(); ++fi) {
        j << buildFileObject(files[fi], graph, 2);
        if (fi + 1 < files.size()) j << ",";
        j << "\n";
    }
    j << indent(1) << "],\n";

    // Dependency graph
    j << indent(1) << "\"dependency_graph\": " << buildDependencyGraph(graph) << "\n";

    j << "}\n";
    return j.str();
}

// ---------------------------------------------------------------------------
// JsonExporter::buildSummary
// ---------------------------------------------------------------------------
std::string JsonExporter::buildSummary(const std::vector<FileMetrics>& files) const {
    int totalFunctions  = 0;
    int totalLines      = 0;
    int highRiskFuncs   = 0;
    int medRiskFuncs    = 0;
    int lowRiskFuncs    = 0;
    int highRiskFiles   = 0;
    int medRiskFiles    = 0;
    int lowRiskFiles    = 0;
    int maxComplexity   = 0;
    std::string riskiestFile;
    std::string riskiestFunction;
    int riskiestFuncComplexity = 0;

    for (const auto& file : files) {
        totalLines += file.total_lines;
        totalFunctions += static_cast<int>(file.functions.size());

        if (file.risk == "high")       ++highRiskFiles;
        else if (file.risk == "medium") ++medRiskFiles;
        else                            ++lowRiskFiles;

        for (const auto& func : file.functions) {
            if (func.risk == "high")       ++highRiskFuncs;
            else if (func.risk == "medium") ++medRiskFuncs;
            else                            ++lowRiskFuncs;

            if (func.complexity > riskiestFuncComplexity) {
                riskiestFuncComplexity = func.complexity;
                riskiestFunction = func.name;
                riskiestFile     = file.name;
            }
            maxComplexity = std::max(maxComplexity, func.complexity);
        }
    }

    double avgComplexity = 0.0;
    if (totalFunctions > 0) {
        int totalCC = 0;
        for (const auto& file : files)
            for (const auto& func : file.functions)
                totalCC += func.complexity;
        avgComplexity = static_cast<double>(totalCC) / totalFunctions;
    }

    std::ostringstream s;
    s << std::fixed;
    s << "{\n";
    s << indent(2) << "\"total_files\": "        << files.size()       << ",\n";
    s << indent(2) << "\"total_functions\": "    << totalFunctions     << ",\n";
    s << indent(2) << "\"total_lines\": "        << totalLines         << ",\n";

    // Format avg_complexity to 1 decimal
    std::ostringstream avgStr;
    avgStr << std::fixed << std::setprecision(1) << avgComplexity;
    s << indent(2) << "\"avg_complexity\": "     << avgStr.str()       << ",\n";

    s << indent(2) << "\"max_complexity\": "     << maxComplexity      << ",\n";
    s << indent(2) << "\"riskiest_file\": \""    << escapeString(riskiestFile)     << "\",\n";
    s << indent(2) << "\"riskiest_function\": \"" << escapeString(riskiestFunction) << "\",\n";
    s << indent(2) << "\"high_risk_count\": "    << highRiskFuncs      << ",\n";
    s << indent(2) << "\"medium_risk_count\": "  << medRiskFuncs       << ",\n";
    s << indent(2) << "\"low_risk_count\": "     << lowRiskFuncs       << "\n";
    s << indent(1) << "}";
    return s.str();
}

// ---------------------------------------------------------------------------
// JsonExporter::buildFileObject
// ---------------------------------------------------------------------------
std::string JsonExporter::buildFileObject(const FileMetrics& file,
                                           const DependencyGraph& graph,
                                           int level) const {
    std::ostringstream o;
    o << indent(level) << "{\n";
    o << indent(level+1) << "\"name\": \""         << escapeString(file.name) << "\",\n";
    o << indent(level+1) << "\"path\": \""         << escapeString(file.path) << "\",\n";
    o << indent(level+1) << "\"total_lines\": "    << file.total_lines        << ",\n";
    o << indent(level+1) << "\"code_lines\": "     << file.code_lines         << ",\n";
    o << indent(level+1) << "\"comment_lines\": "  << file.comment_lines      << ",\n";
    o << indent(level+1) << "\"blank_lines\": "    << file.blank_lines        << ",\n";
    o << indent(level+1) << "\"function_count\": " << file.functions.size()   << ",\n";
    o << indent(level+1) << "\"complexity_score\": "<< file.complexity_score  << ",\n";
    o << indent(level+1) << "\"risk\": \""         << file.risk               << "\",\n";

    // Dependencies array
    const auto& deps = graph.getDependencies(file.name);
    o << indent(level+1) << "\"dependencies\": [";
    for (std::size_t di = 0; di < deps.size(); ++di) {
        o << "\"" << escapeString(deps[di]) << "\"";
        if (di + 1 < deps.size()) o << ", ";
    }
    o << "],\n";

    o << indent(level+1) << "\"has_circular_dep\": "
      << (graph.hasCircularDependency(file.name) ? "true" : "false") << ",\n";

    // Functions array
    o << indent(level+1) << "\"functions\": [\n";
    for (std::size_t fi = 0; fi < file.functions.size(); ++fi) {
        o << buildFunctionObject(file.functions[fi], level + 2);
        if (fi + 1 < file.functions.size()) o << ",";
        o << "\n";
    }
    o << indent(level+1) << "]\n";
    o << indent(level) << "}";
    return o.str();
}

// ---------------------------------------------------------------------------
// JsonExporter::buildFunctionObject
// ---------------------------------------------------------------------------
std::string JsonExporter::buildFunctionObject(const FunctionMetrics& func,
                                               int level) const {
    std::ostringstream o;
    o << indent(level) << "{\n";
    o << indent(level+1) << "\"name\": \""           << escapeString(func.name) << "\",\n";
    o << indent(level+1) << "\"line_start\": "        << func.line_start         << ",\n";
    o << indent(level+1) << "\"line_end\": "          << func.line_end           << ",\n";
    o << indent(level+1) << "\"lines\": "             << func.lines              << ",\n";
    o << indent(level+1) << "\"complexity\": "        << func.complexity         << ",\n";
    o << indent(level+1) << "\"nesting_depth\": "     << func.nesting_depth      << ",\n";
    o << indent(level+1) << "\"parameter_count\": "   << func.parameter_count    << ",\n";
    o << indent(level+1) << "\"risk\": \""            << func.risk               << "\",\n";
    o << indent(level+1) << "\"risk_reasons\": [";
    for (std::size_t ri = 0; ri < func.risk_reasons.size(); ++ri) {
        o << "\"" << escapeString(func.risk_reasons[ri]) << "\"";
        if (ri + 1 < func.risk_reasons.size()) o << ", ";
    }
    o << "]\n";
    o << indent(level) << "}";
    return o.str();
}

// ---------------------------------------------------------------------------
// JsonExporter::buildDependencyGraph
// ---------------------------------------------------------------------------
std::string JsonExporter::buildDependencyGraph(const DependencyGraph& graph) const {
    std::ostringstream o;
    o << "{\n";

    // Nodes
    const auto nodes = graph.getNodes();
    o << indent(2) << "\"nodes\": [";
    for (std::size_t ni = 0; ni < nodes.size(); ++ni) {
        o << "\"" << escapeString(nodes[ni]) << "\"";
        if (ni + 1 < nodes.size()) o << ", ";
    }
    o << "],\n";

    // Edges
    const auto edges = graph.getEdges();
    o << indent(2) << "\"edges\": [\n";
    for (std::size_t ei = 0; ei < edges.size(); ++ei) {
        o << indent(3) << "{\"from\": \"" << escapeString(edges[ei].first)
          << "\", \"to\": \"" << escapeString(edges[ei].second) << "\"}";
        if (ei + 1 < edges.size()) o << ",";
        o << "\n";
    }
    o << indent(2) << "],\n";

    // Circular dependencies
    const auto cycles = graph.detectCircularDependencies();
    o << indent(2) << "\"circular_dependencies\": [";
    for (std::size_t ci = 0; ci < cycles.size(); ++ci) {
        o << "\"" << escapeString(cycles[ci]) << "\"";
        if (ci + 1 < cycles.size()) o << ", ";
    }
    o << "]\n";

    o << indent(1) << "}";
    return o.str();
}

// ---------------------------------------------------------------------------
// JsonExporter::escapeString
// ---------------------------------------------------------------------------
std::string JsonExporter::escapeString(const std::string& s) const {
    std::string result;
    result.reserve(s.size());
    for (char c : s) {
        switch (c) {
            case '"':  result += "\\\""; break;
            case '\\': result += "\\\\"; break;
            case '\n': result += "\\n";  break;
            case '\r': result += "\\r";  break;
            case '\t': result += "\\t";  break;
            default:   result += c;      break;
        }
    }
    return result;
}

// ---------------------------------------------------------------------------
// JsonExporter::indent
// ---------------------------------------------------------------------------
std::string JsonExporter::indent(int level) const {
    return std::string(static_cast<std::size_t>(level) * 2, ' ');
}

// ---------------------------------------------------------------------------
// JsonExporter::currentTimestamp
// ---------------------------------------------------------------------------
std::string JsonExporter::currentTimestamp() const {
    const std::time_t now = std::time(nullptr);
    std::tm tm_utc = *localtime(&now);
    std::ostringstream oss;
    oss << (tm_utc.tm_year + 1900) << "-"
        << std::setfill('0') << std::setw(2) << (tm_utc.tm_mon + 1) << "-"
        << std::setfill('0') << std::setw(2) <<  tm_utc.tm_mday     << "T"
        << std::setfill('0') << std::setw(2) <<  tm_utc.tm_hour     << ":"
        << std::setfill('0') << std::setw(2) <<  tm_utc.tm_min      << ":"
        << std::setfill('0') << std::setw(2) <<  tm_utc.tm_sec;
    return oss.str();
}
