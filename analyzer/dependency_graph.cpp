#include <sstream>
#include "dependency_graph.h"
#include <regex>
#include <algorithm>
#include <stdexcept>

// Static member
const std::vector<std::string> DependencyGraph::EMPTY_DEPS;

// ---------------------------------------------------------------------------
// DependencyGraph::addFile
// ---------------------------------------------------------------------------
void DependencyGraph::addFile(const std::string& filename,
                               const std::vector<std::string>& dependencies) {
    // Ensure the file appears as a node even if it has no deps
    if (graph_.find(filename) == graph_.end()) {
        graph_[filename] = {};
    }

    for (const auto& dep : dependencies) {
        // Avoid duplicate edges
        auto& deps = graph_[filename];
        if (std::find(deps.begin(), deps.end(), dep) == deps.end()) {
            deps.push_back(dep);
        }
        // Ensure the dependency itself is a node
        if (graph_.find(dep) == graph_.end()) {
            graph_[dep] = {};
        }
    }

    // Invalidate the cached circular dependency result
    circularDepsComputed_ = false;
}

// ---------------------------------------------------------------------------
// DependencyGraph::extractIncludes
// ---------------------------------------------------------------------------
// Pattern: #include "filename.h"  (local only — <system> headers ignored)
// ---------------------------------------------------------------------------
std::vector<std::string> DependencyGraph::extractIncludes(const std::string& source) const {
    std::vector<std::string> includes;

    // Match: #include "something"  (with optional leading whitespace)
    static const std::regex localInclude("^\\s*#include\\s*\"([^\"]+)\"");

    std::istringstream stream(source);
    std::string line;
    while (std::getline(stream, line)) {
        std::smatch match;
        if (std::regex_search(line, match, localInclude)) {
            // Extract only the basename
            std::string includePath = match[1].str();
            const auto slashPos = includePath.find_last_of("/\\");
            if (slashPos != std::string::npos) {
                includePath = includePath.substr(slashPos + 1);
            }
            includes.push_back(includePath);
        }
    }

    return includes;
}

// ---------------------------------------------------------------------------
// DependencyGraph::detectCircularDependencies
// ---------------------------------------------------------------------------
std::vector<std::string> DependencyGraph::detectCircularDependencies() const {
    if (circularDepsComputed_) {
        return circularDeps_;
    }

    circularDeps_.clear();
    circularFiles_.clear();

    std::unordered_set<std::string> visited;
    std::unordered_set<std::string> inStack;
    std::vector<std::string> path;

    for (const auto& kv : graph_) {
        if (visited.find(kv.first) == visited.end()) {
            dfs(kv.first, visited, inStack, path, circularDeps_);
        }
    }

    circularDepsComputed_ = true;
    return circularDeps_;
}

// ---------------------------------------------------------------------------
// DependencyGraph::dfs  (private)
// ---------------------------------------------------------------------------
bool DependencyGraph::dfs(const std::string& node,
                           std::unordered_set<std::string>& visited,
                           std::unordered_set<std::string>& inStack,
                           std::vector<std::string>& path,
                           std::vector<std::string>& cycles) const {
    visited.insert(node);
    inStack.insert(node);
    path.push_back(node);

    const auto it = graph_.find(node);
    if (it != graph_.end()) {
        for (const auto& neighbor : it->second) {
            if (visited.find(neighbor) == visited.end()) {
                dfs(neighbor, visited, inStack, path, cycles);
            } else if (inStack.find(neighbor) != inStack.end()) {
                // Cycle detected — build a human-readable description
                std::string cycle;
                bool found = false;
                for (const auto& n : path) {
                    if (n == neighbor) found = true;
                    if (found) cycle += n + " -> ";
                }
                cycle += neighbor;
                cycles.push_back(cycle);

                // Mark all nodes in the cycle
                for (const auto& n : path) {
                    circularFiles_.insert(n);
                }
                circularFiles_.insert(neighbor);
            }
        }
    }

    path.pop_back();
    inStack.erase(node);
    return false;
}

// ---------------------------------------------------------------------------
// DependencyGraph::getNodes
// ---------------------------------------------------------------------------
std::vector<std::string> DependencyGraph::getNodes() const {
    std::vector<std::string> nodes;
    nodes.reserve(graph_.size());
    for (const auto& kv : graph_) {
        nodes.push_back(kv.first);
    }
    std::sort(nodes.begin(), nodes.end());
    return nodes;
}

// ---------------------------------------------------------------------------
// DependencyGraph::getEdges
// ---------------------------------------------------------------------------
std::vector<std::pair<std::string, std::string>> DependencyGraph::getEdges() const {
    std::vector<std::pair<std::string, std::string>> edges;
    for (const auto& kv : graph_) {
        for (const auto& dep : kv.second) {
            edges.emplace_back(kv.first, dep);
        }
    }
    return edges;
}

// ---------------------------------------------------------------------------
// DependencyGraph::getDependencies
// ---------------------------------------------------------------------------
const std::vector<std::string>& DependencyGraph::getDependencies(
        const std::string& filename) const {
    const auto it = graph_.find(filename);
    if (it == graph_.end()) return EMPTY_DEPS;
    return it->second;
}

// ---------------------------------------------------------------------------
// DependencyGraph::hasCircularDependency
// ---------------------------------------------------------------------------
bool DependencyGraph::hasCircularDependency(const std::string& filename) const {
    if (!circularDepsComputed_) {
        detectCircularDependencies();
    }
    return circularFiles_.find(filename) != circularFiles_.end();
}
