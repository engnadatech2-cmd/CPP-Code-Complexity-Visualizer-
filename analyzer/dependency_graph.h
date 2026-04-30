#pragma once
#include <string>
#include <vector>
#include <unordered_map>
#include <unordered_set>

/**
 * DependencyGraph
 *
 * Builds a directed graph of #include relationships between files.
 * Uses std::unordered_map for O(1) average lookup.
 * Detects circular dependencies via DFS.
 */
class DependencyGraph {
public:
    /**
     * Add a file and its direct #include dependencies to the graph.
     *
     * @param filename      Basename of the file (e.g. "hospital.cpp")
     * @param dependencies  List of included local headers (e.g. {"patient.h", "utils.h"})
     */
    void addFile(const std::string& filename,
                 const std::vector<std::string>& dependencies);

    /**
     * Extract #include directives from raw C++ source.
     * Only local includes (with "") are returned; <system> headers are ignored.
     *
     * @param source    Raw file content
     * @return          Vector of included filenames (basename only)
     */
    std::vector<std::string> extractIncludes(const std::string& source) const;

    /**
     * Run DFS-based circular dependency detection across the whole graph.
     *
     * @return  List of circular dependency chains, e.g. {"a.cpp -> b.h -> a.cpp"}
     */
    std::vector<std::string> detectCircularDependencies() const;

    /**
     * Get all nodes (filenames) in the graph.
     */
    std::vector<std::string> getNodes() const;

    /**
     * Get all edges as (from, to) pairs.
     */
    std::vector<std::pair<std::string, std::string>> getEdges() const;

    /**
     * Get direct dependencies of a given file.
     */
    const std::vector<std::string>& getDependencies(const std::string& filename) const;

    /**
     * Check if a specific file has any circular dependency.
     */
    bool hasCircularDependency(const std::string& filename) const;

private:
    // filename → list of direct dependencies
    std::unordered_map<std::string, std::vector<std::string>> graph_;

    // Set of files involved in circular dependencies
    mutable std::unordered_set<std::string> circularFiles_;

    // Cached circular dependency list (computed once)
    mutable std::vector<std::string> circularDeps_;
    mutable bool circularDepsComputed_ = false;

    /** DFS helper for circular dependency detection */
    bool dfs(const std::string& node,
             std::unordered_set<std::string>& visited,
             std::unordered_set<std::string>& inStack,
             std::vector<std::string>& path,
             std::vector<std::string>& cycles) const;

    static const std::vector<std::string> EMPTY_DEPS;
};
