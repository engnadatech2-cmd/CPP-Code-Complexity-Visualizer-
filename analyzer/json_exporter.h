#pragma once
#include "metrics_calculator.h"
#include "dependency_graph.h"
#include <string>
#include <vector>

/**
 * JsonExporter
 *
 * Produces a JSON file matching the project contract exactly.
 * Zero external dependencies — all JSON is built manually.
 *
 * Output format:
 * {
 *   "project": "...",
 *   "analyzed_at": "...",
 *   "analyzer_version": "1.0.0",
 *   "summary": { ... },
 *   "files": [ ... ],
 *   "dependency_graph": { ... }
 * }
 */
class JsonExporter {
public:
    /**
     * Build and write the JSON report to disk.
     *
     * @param files       All file metrics produced by MetricsCalculator
     * @param graph       Fully populated dependency graph
     * @param projectName Human-readable project name
     * @param outputPath  Path where output.json will be written
     */
    void exportToFile(const std::vector<FileMetrics>& files,
                      const DependencyGraph& graph,
                      const std::string& projectName,
                      const std::string& outputPath) const;

private:
    /** Assemble the complete JSON string */
    std::string buildJson(const std::vector<FileMetrics>& files,
                          const DependencyGraph& graph,
                          const std::string& projectName) const;

    /** Escape special JSON characters in a string value */
    std::string escapeString(const std::string& s) const;

    /** Return N*2 spaces for indentation */
    std::string indent(int level) const;

    /** Get current UTC timestamp in ISO-8601 format */
    std::string currentTimestamp() const;

    /** Build the "summary" object */
    std::string buildSummary(const std::vector<FileMetrics>& files) const;

    /** Build a single file object */
    std::string buildFileObject(const FileMetrics& file,
                                const DependencyGraph& graph,
                                int indentLevel) const;

    /** Build a single function object */
    std::string buildFunctionObject(const FunctionMetrics& func,
                                    int indentLevel) const;

    /** Build the "dependency_graph" object */
    std::string buildDependencyGraph(const DependencyGraph& graph) const;
};
