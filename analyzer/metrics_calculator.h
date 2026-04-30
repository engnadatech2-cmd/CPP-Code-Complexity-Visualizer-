#pragma once
#include <string>
#include <vector>

/**
 * FunctionMetrics
 * Holds all per-function analysis results.
 */
struct FunctionMetrics {
    std::string name;
    int line_start      = 0;
    int line_end        = 0;
    int lines           = 0;
    int complexity      = 1;   // baseline = 1
    int nesting_depth   = 0;
    int parameter_count = 0;
    std::string risk;                       // "low" | "medium" | "high"
    std::vector<std::string> risk_reasons;  // e.g. "high_complexity", "deep_nesting"
};

/**
 * FileMetrics
 * Holds all per-file analysis results plus its function list.
 */
struct FileMetrics {
    std::string name;
    std::string path;
    int total_lines      = 0;
    int code_lines       = 0;
    int comment_lines    = 0;
    int blank_lines      = 0;
    int complexity_score = 0;  // sum of all function complexities
    std::string risk;          // "low" | "medium" | "high"
    std::vector<FunctionMetrics> functions;
};

/**
 * MetricsCalculator
 *
 * Analyzes stripped (comment-free) C++ source to compute:
 *   - Cyclomatic Complexity per function (branch-keyword counting)
 *   - Nesting depth
 *   - Parameter count
 *   - Line counts (total / code / comment / blank)
 *   - Risk classification
 */
class MetricsCalculator {
public:
    /**
     * Analyze a single file.
     *
     * @param rawSource     Original source (with comments) — used for line counting
     * @param strippedSource Source after comment stripping — used for logic analysis
     * @param filePath      Full path of the file (for metadata)
     * @return              Populated FileMetrics struct
     */
    FileMetrics analyze(const std::string& rawSource,
                        const std::string& strippedSource,
                        const std::string& filePath) const;

private:
    /** Extract all functions from stripped source */
    std::vector<FunctionMetrics> extractFunctions(const std::string& stripped) const;

    /** Count branch keywords to compute cyclomatic complexity */
    int calculateComplexity(const std::string& functionBody) const;

    /** Find maximum brace nesting depth in a function body */
    int calculateNestingDepth(const std::string& functionBody) const;

    /** Count parameters in a function signature */
    int countParameters(const std::string& signature) const;

    /** Classify risk level from complexity score */
    std::string classifyRisk(int complexity, int nestingDepth) const;

    /** Build risk_reasons list */
    std::vector<std::string> buildRiskReasons(int complexity, int nestingDepth) const;

    /** Count code/comment/blank lines in raw source */
    void countLines(const std::string& rawSource,
                    const std::string& strippedSource,
                    int& total, int& code, int& comment, int& blank) const;
};
