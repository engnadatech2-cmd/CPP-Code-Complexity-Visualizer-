#include "metrics_calculator.h"
#include <sstream>
#include <algorithm>
#include <cctype>
#include <regex>
#include <stdexcept>
#include <unordered_set>

// ---------------------------------------------------------------------------
// Helper utilities (file-local)
// ---------------------------------------------------------------------------
namespace {

/** Trim leading/trailing whitespace from a string. */
std::string trim(const std::string& s) {
    const auto start = s.find_first_not_of(" \t\r\n");
    if (start == std::string::npos) return "";
    const auto end = s.find_last_not_of(" \t\r\n");
    return s.substr(start, end - start + 1);
}

/** Split a string into lines. */
std::vector<std::string> splitLines(const std::string& s) {
    std::vector<std::string> lines;
    std::istringstream stream(s);
    std::string line;
    while (std::getline(stream, line)) {
        lines.push_back(line);
    }
    return lines;
}

/** Check whether a line is effectively blank (all whitespace). */
bool isBlankLine(const std::string& line) {
    return trim(line).empty();
}

/** Count occurrences of a whole-word token in text. */
int countWholeWordOccurrences(const std::string& text, const std::string& word) {
    int count = 0;
    std::size_t pos = 0;
    while ((pos = text.find(word, pos)) != std::string::npos) {
        // Ensure it is a whole word (not part of identifier)
        bool leftOk  = (pos == 0) || !std::isalnum(static_cast<unsigned char>(text[pos - 1]))
                                   && text[pos - 1] != '_';
        bool rightOk = (pos + word.size() >= text.size())
                    || !std::isalnum(static_cast<unsigned char>(text[pos + word.size()]))
                    && text[pos + word.size()] != '_';
        if (leftOk && rightOk) ++count;
        ++pos;
    }
    return count;
}

} // anonymous namespace

// ---------------------------------------------------------------------------
// MetricsCalculator::analyze
// ---------------------------------------------------------------------------
FileMetrics MetricsCalculator::analyze(const std::string& rawSource,
                                        const std::string& strippedSource,
                                        const std::string& filePath) const {
    FileMetrics fm;

    // Derive name from path
    const auto slashPos = filePath.find_last_of("/\\");
    fm.name = (slashPos == std::string::npos) ? filePath : filePath.substr(slashPos + 1);
    fm.path = filePath;

    // Count lines
    countLines(rawSource, strippedSource,
               fm.total_lines, fm.code_lines, fm.comment_lines, fm.blank_lines);

    // Extract functions from stripped source
    fm.functions = extractFunctions(strippedSource);

    // Compute per-file complexity score and risk
    fm.complexity_score = 0;
    for (const auto& func : fm.functions) {
        fm.complexity_score += func.complexity;
    }

    // File risk = worst function risk
    fm.risk = "low";
    for (const auto& func : fm.functions) {
        if (func.risk == "high") { fm.risk = "high"; break; }
        if (func.risk == "medium") { fm.risk = "medium"; }
    }

    return fm;
}

// ---------------------------------------------------------------------------
// MetricsCalculator::extractFunctions
// ---------------------------------------------------------------------------
// Strategy:
//   Walk stripped source line by line.
//   A function starts when we see a line that looks like a function signature
//   (contains '(' and ')') followed by '{', and ends when the matching '}'
//   is found (brace counting).
// ---------------------------------------------------------------------------
std::vector<FunctionMetrics> MetricsCalculator::extractFunctions(
        const std::string& stripped) const {

    std::vector<FunctionMetrics> functions;
    const std::vector<std::string> lines = splitLines(stripped);
    const int totalLines = static_cast<int>(lines.size());

    // Regex to detect a function-like signature:
    //   optional return type, function name, parameter list
    //   We require: identifier ( ... ) at the end of the line OR followed by {
    // We use a broad pattern and filter out obvious non-functions (if/for/while/etc.)
    static const std::regex funcSignaturePattern(
        R"(^\s*(?:(?:inline|static|virtual|explicit|friend|constexpr|const|override|final|noexcept)\s+)*)"
        R"([\w:~<>\*&\s]+\s+(\w+)\s*\(([^;]*)\)\s*(?:const\s*)?(?:noexcept\s*)?(?:override\s*)?(?:->\s*[\w:&\*<>\s]+)?\s*\{?\s*$)"
    );

    // Keywords that look like functions but are control flow
    static const std::unordered_set<std::string> controlFlow = {
        "if", "for", "while", "switch", "catch", "do", "else"
    };

    int i = 0;
    while (i < totalLines) {
        const std::string& line = lines[i];

        // Skip blank lines quickly
        if (isBlankLine(line)) { ++i; continue; }

        std::smatch match;
        bool isSignature = std::regex_search(line, match, funcSignaturePattern);

        if (!isSignature) { ++i; continue; }

        // Extract function name
        std::string funcName = match[1].str();
        if (controlFlow.count(funcName)) { ++i; continue; }
        if (funcName.empty()) { ++i; continue; }

        // Extract parameter string
        std::string paramStr = match[2].str();

        // Find the opening brace (might be on this line or the next)
        int braceDepth  = 0;
        int funcStart   = i + 1;  // 1-indexed line number
        int openLine    = i;

        // Scan forward to find the opening '{'
        bool foundOpen = false;
        for (int scan = i; scan < std::min(totalLines, i + 5); ++scan) {
            for (char ch : lines[scan]) {
                if (ch == '{') { foundOpen = true; openLine = scan; break; }
                if (ch == ';') { goto nextLine; }  // declaration only, not definition
            }
            if (foundOpen) break;
        }
        if (!foundOpen) { ++i; continue; }

        {
            // Collect body until matching closing brace
            std::string body;
            int funcEnd = openLine;

            // Walk from the opening brace line
            for (int scan = openLine; scan < totalLines; ++scan) {
                const std::string& scanLine = lines[scan];
                for (char ch : scanLine) {
                    if (ch == '{') ++braceDepth;
                    else if (ch == '}') {
                        --braceDepth;
                        if (braceDepth == 0) {
                            funcEnd = scan;
                            goto doneScanning;
                        }
                    }
                }
                body += scanLine + '\n';
            }

            doneScanning:
            if (braceDepth != 0) { ++i; continue; }  // unmatched braces

            // Accumulate the last line too
            for (int scan = funcEnd; scan <= funcEnd && scan < totalLines; ++scan) {
                body += lines[scan] + '\n';
            }

            FunctionMetrics fm;
            fm.name            = funcName;
            fm.line_start      = funcStart;
            fm.line_end        = funcEnd + 1;   // 1-indexed
            fm.lines           = fm.line_end - fm.line_start + 1;
            fm.complexity      = calculateComplexity(body);
            fm.nesting_depth   = calculateNestingDepth(body);
            fm.parameter_count = countParameters(paramStr);
            fm.risk            = classifyRisk(fm.complexity, fm.nesting_depth);
            fm.risk_reasons    = buildRiskReasons(fm.complexity, fm.nesting_depth);

            functions.push_back(std::move(fm));
            i = funcEnd + 1;
            continue;
        }

        nextLine:
        ++i;
    }

    return functions;
}

// ---------------------------------------------------------------------------
// MetricsCalculator::calculateComplexity
// ---------------------------------------------------------------------------
// Cyclomatic complexity = 1 + number of decision points.
// Decision points: if, else if, for, while, do, case, catch, &&, ||, ?
// ---------------------------------------------------------------------------
int MetricsCalculator::calculateComplexity(const std::string& body) const {
    int complexity = 1;  // baseline

    // Whole-word keywords
    static const std::vector<std::string> keywords = {
        "if", "for", "while", "do", "case", "catch"
    };
    for (const auto& kw : keywords) {
        complexity += countWholeWordOccurrences(body, kw);
    }

    // Operators (not whole-word, just substring)
    auto countOp = [&](const std::string& op) {
        int count = 0;
        std::size_t pos = 0;
        while ((pos = body.find(op, pos)) != std::string::npos) {
            ++count; pos += op.size();
        }
        return count;
    };

    complexity += countOp("&&");
    complexity += countOp("||");
    complexity += countOp("?");   // ternary operator

    return complexity;
}

// ---------------------------------------------------------------------------
// MetricsCalculator::calculateNestingDepth
// ---------------------------------------------------------------------------
int MetricsCalculator::calculateNestingDepth(const std::string& body) const {
    int depth    = 0;
    int maxDepth = 0;

    for (char c : body) {
        if (c == '{') {
            ++depth;
            maxDepth = std::max(maxDepth, depth);
        } else if (c == '}') {
            if (depth > 0) --depth;
        }
    }
    // Subtract 1 for the function's own brace pair
    return std::max(0, maxDepth - 1);
}

// ---------------------------------------------------------------------------
// MetricsCalculator::countParameters
// ---------------------------------------------------------------------------
int MetricsCalculator::countParameters(const std::string& paramStr) const {
    const std::string trimmed = trim(paramStr);
    if (trimmed.empty() || trimmed == "void") return 0;

    // Count commas at brace depth 0 (handles templates like std::map<K,V>)
    int count = 1;
    int depth = 0;
    for (char c : trimmed) {
        if (c == '<' || c == '(' || c == '[') ++depth;
        else if (c == '>' || c == ')' || c == ']') --depth;
        else if (c == ',' && depth == 0) ++count;
    }
    return count;
}

// ---------------------------------------------------------------------------
// MetricsCalculator::classifyRisk
// ---------------------------------------------------------------------------
std::string MetricsCalculator::classifyRisk(int complexity, int nestingDepth) const {
    if (complexity >= 11 || nestingDepth >= 4) return "high";
    if (complexity >= 6  || nestingDepth >= 4) return "medium";
    return "low";
}

// ---------------------------------------------------------------------------
// MetricsCalculator::buildRiskReasons
// ---------------------------------------------------------------------------
std::vector<std::string> MetricsCalculator::buildRiskReasons(int complexity,
                                                               int nestingDepth) const {
    std::vector<std::string> reasons;
    if (complexity >= 11) reasons.push_back("high_complexity");
    else if (complexity >= 6) reasons.push_back("medium_complexity");
    if (nestingDepth >= 4) reasons.push_back("deep_nesting");
    return reasons;
}

// ---------------------------------------------------------------------------
// MetricsCalculator::countLines
// ---------------------------------------------------------------------------
// Counts total, code, comment, and blank lines.
// Strategy: compare raw vs stripped source line by line.
//   - If stripped line is blank and raw line is not → comment line
//   - If both blank → blank line
//   - Otherwise → code line
// ---------------------------------------------------------------------------
void MetricsCalculator::countLines(const std::string& rawSource,
                                    const std::string& strippedSource,
                                    int& total, int& code,
                                    int& comment, int& blank) const {
    total = code = comment = blank = 0;

    const std::vector<std::string> rawLines      = splitLines(rawSource);
    const std::vector<std::string> strippedLines = splitLines(strippedSource);

    const int lineCount = static_cast<int>(rawLines.size());
    total = lineCount;

    for (int i = 0; i < lineCount; ++i) {
        const std::string rawTrimmed = trim(rawLines[i]);
        const std::string strTrimmed = (i < static_cast<int>(strippedLines.size()))
                                     ? trim(strippedLines[i]) : "";

        if (rawTrimmed.empty()) {
            ++blank;
        } else if (strTrimmed.empty()) {
            // Line had content in raw but nothing in stripped → pure comment
            ++comment;
        } else {
            ++code;
        }
    }
}
