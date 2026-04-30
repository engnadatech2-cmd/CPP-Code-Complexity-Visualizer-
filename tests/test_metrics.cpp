/**
 * test_metrics.cpp
 *
 * Unit tests for MetricsCalculator.
 * Covers: complexity calculation, nesting depth, parameter count,
 * risk classification, and full file analysis.
 *
 * Compile (from project root):
 *   g++ -std=c++17 -Wall -Wextra \
 *       analyzer/comment_stripper.cpp \
 *       analyzer/metrics_calculator.cpp \
 *       tests/test_metrics.cpp \
 *       -o tests/run_metrics_tests
 */

#include "../analyzer/metrics_calculator.h"
#include "../analyzer/comment_stripper.h"

#include <iostream>
#include <string>
#include <cassert>

// ---------------------------------------------------------------------------
// Tiny test harness (same pattern as test_comment_stripper.cpp)
// ---------------------------------------------------------------------------
static int g_total  = 0;
static int g_passed = 0;

static void check(const std::string& name, bool condition,
                  const std::string& detail = "") {
    ++g_total;
    if (condition) {
        ++g_passed;
        std::cout << "  \033[32m[PASS]\033[0m " << name << "\n";
    } else {
        std::cout << "  \033[31m[FAIL]\033[0m " << name;
        if (!detail.empty()) std::cout << " — " << detail;
        std::cout << "\n";
    }
}

template<typename T>
static void checkEq(const std::string& name, T got, T expected) {
    ++g_total;
    if (got == expected) {
        ++g_passed;
        std::cout << "  \033[32m[PASS]\033[0m " << name
                  << " (= " << got << ")\n";
    } else {
        std::cout << "  \033[31m[FAIL]\033[0m " << name
                  << " — expected " << expected << ", got " << got << "\n";
    }
}

// ---------------------------------------------------------------------------
static MetricsCalculator calc;
static CommentStripper   stripper;

// ---------------------------------------------------------------------------
// Helper: analyze a snippet (strip first, then analyze as "test.cpp")
// ---------------------------------------------------------------------------
static FileMetrics analyzeSnippet(const std::string& code) {
    const std::string stripped = stripper.strip(code);
    return calc.analyze(code, stripped, "test.cpp");
}

// ---------------------------------------------------------------------------
// Test: baseline complexity (no branches)
// ---------------------------------------------------------------------------
void test_complexity_baseline() {
    const std::string code = R"(
void noOp() {
}
)";
    const auto fm = analyzeSnippet(code);
    check("baseline: 1 function detected",
          fm.functions.size() == 1,
          "found " + std::to_string(fm.functions.size()));
    if (!fm.functions.empty()) {
        checkEq("baseline: complexity = 1", fm.functions[0].complexity, 1);
        checkEq("baseline: risk = low",     fm.functions[0].risk, std::string("low"));
    }
}

// ---------------------------------------------------------------------------
// Test: complexity with if / for / &&
// ---------------------------------------------------------------------------
void test_complexity_branches() {
    // Expected: 1 + if(1) + for(1) + if(1) + ||(1) = 5
    const std::string code = R"(
void foo() {
    if (a) {
        for (int i = 0; i < n; ++i) {
            if (b || c) {
            }
        }
    }
}
)";
    const auto fm = analyzeSnippet(code);
    check("branches: 1 function detected",
          fm.functions.size() == 1,
          "found " + std::to_string(fm.functions.size()));
    if (!fm.functions.empty()) {
        // complexity = 1 + 1(if) + 1(for) + 1(if) + 1(||) = 5
        checkEq("branches: complexity = 5", fm.functions[0].complexity, 5);
        checkEq("branches: risk = low",     fm.functions[0].risk, std::string("low"));
    }
}

// ---------------------------------------------------------------------------
// Test: high complexity triggers high risk
// ---------------------------------------------------------------------------
void test_complexity_high_risk() {
    // Pile up branches to get CC >= 11
    const std::string code = R"(
int complex(int a, int b, int c) {
    if (a > 0) {
        if (b > 0) {
            if (c > 0) {
                for (int i = 0; i < a; ++i) {
                    while (b-- > 0) {
                        switch (c) {
                            case 1: break;
                            case 2: break;
                            default: break;
                        }
                    }
                }
            } else if (c < 0) {
                return a && b ? a : b;
            }
        }
    }
    return 0;
}
)";
    const auto fm = analyzeSnippet(code);
    check("high_risk: 1 function detected",
          fm.functions.size() == 1,
          "found " + std::to_string(fm.functions.size()));
    if (!fm.functions.empty()) {
        check("high_risk: complexity >= 11",
              fm.functions[0].complexity >= 11,
              "got " + std::to_string(fm.functions[0].complexity));
        checkEq("high_risk: risk = high", fm.functions[0].risk, std::string("high"));
    }
}

// ---------------------------------------------------------------------------
// Test: medium complexity (CC 6-10)
// ---------------------------------------------------------------------------
void test_complexity_medium_risk() {
    const std::string code = R"(
int medium(int a, int b, int c, int d, int e) {
    if (a > 0) return a;
    if (b > 0) return b;
    if (c > 0) return c;
    if (d > 0) return d;
    if (e > 0) return e;
    return 0;
}
)";
    const auto fm = analyzeSnippet(code);
    check("medium_risk: 1 function detected",
          fm.functions.size() == 1,
          "found " + std::to_string(fm.functions.size()));
    if (!fm.functions.empty()) {
        check("medium_risk: complexity in [6,10]",
              fm.functions[0].complexity >= 6 && fm.functions[0].complexity <= 10,
              "got " + std::to_string(fm.functions[0].complexity));
        checkEq("medium_risk: risk = medium", fm.functions[0].risk, std::string("medium"));
    }
}

// ---------------------------------------------------------------------------
// Test: nesting depth
// ---------------------------------------------------------------------------
void test_nesting_depth() {
    const std::string code = R"(
void deepNest() {
    {           // depth 1
        {       // depth 2
            {   // depth 3
                {  // depth 4
                }
            }
        }
    }
}
)";
    const auto fm = analyzeSnippet(code);
    check("nesting: 1 function detected",
          fm.functions.size() == 1,
          "found " + std::to_string(fm.functions.size()));
    if (!fm.functions.empty()) {
        check("nesting: depth >= 4",
              fm.functions[0].nesting_depth >= 4,
              "got " + std::to_string(fm.functions[0].nesting_depth));
    }
}

// ---------------------------------------------------------------------------
// Test: parameter count
// ---------------------------------------------------------------------------
void test_parameter_count() {
    const std::string code = R"(
int add(int a, int b, int c) {
    return a + b + c;
}
)";
    const auto fm = analyzeSnippet(code);
    check("params: 1 function detected",
          fm.functions.size() == 1,
          "found " + std::to_string(fm.functions.size()));
    if (!fm.functions.empty()) {
        checkEq("params: 3 parameters", fm.functions[0].parameter_count, 3);
    }
}

// ---------------------------------------------------------------------------
// Test: zero-parameter function
// ---------------------------------------------------------------------------
void test_no_parameters() {
    const std::string code = R"(
void noArgs() {
    return;
}
)";
    const auto fm = analyzeSnippet(code);
    if (!fm.functions.empty()) {
        check("params: 0 parameters (void or empty)",
              fm.functions[0].parameter_count == 0,
              "got " + std::to_string(fm.functions[0].parameter_count));
    }
}

// ---------------------------------------------------------------------------
// Test: multiple functions detected
// ---------------------------------------------------------------------------
void test_multiple_functions() {
    const std::string code = R"(
int alpha() {
    return 1;
}

int beta(int x) {
    if (x > 0) return x;
    return -x;
}

void gamma(int a, int b, int c) {
    for (int i = 0; i < a; ++i) {}
}
)";
    const auto fm = analyzeSnippet(code);
    check("multi: 3 functions detected",
          fm.functions.size() == 3,
          "found " + std::to_string(fm.functions.size()));
}

// ---------------------------------------------------------------------------
// Test: line counts
// ---------------------------------------------------------------------------
void test_line_counts() {
    const std::string code =
        "// comment line\n"          // comment
        "int x = 5;\n"               // code
        "\n"                         // blank
        "/* block */\n"              // comment
        "int y = x + 1;\n";          // code

    const std::string stripped = stripper.strip(code);
    const auto fm = calc.analyze(code, stripped, "line_test.cpp");

    checkEq("line_counts: total_lines = 5",   fm.total_lines,   5);
    checkEq("line_counts: code_lines = 2",    fm.code_lines,    2);
    checkEq("line_counts: comment_lines = 2", fm.comment_lines, 2);
    checkEq("line_counts: blank_lines = 1",   fm.blank_lines,   1);
}

// ---------------------------------------------------------------------------
// Test: file risk = highest function risk
// ---------------------------------------------------------------------------
void test_file_risk_propagation() {
    const std::string code = R"(
int low() {
    return 0;
}

int high(int a, int b, int c) {
    if (a) { if (b) { if (c) { for(;;) { while(1) { do { switch(a) {
        case 1: break;
        case 2: break;
    }}}}}}}}
    return 0;
}
)";
    const auto fm = analyzeSnippet(code);
    checkEq("file_risk: propagates to high", fm.risk, std::string("high"));
}

// ---------------------------------------------------------------------------
// Test: complexity score = sum of function complexities
// ---------------------------------------------------------------------------
void test_complexity_score() {
    const std::string code = R"(
int f1() {
    if (true) return 1;
    return 0;
}

int f2() {
    for (int i=0;i<10;++i) {}
    return 0;
}
)";
    const auto fm = analyzeSnippet(code);
    int expected = 0;
    for (const auto& fn : fm.functions) expected += fn.complexity;
    checkEq("complexity_score = sum of function CCs",
            fm.complexity_score, expected);
}

// ---------------------------------------------------------------------------
// main
// ---------------------------------------------------------------------------
int main() {
    std::cout << "\n\033[1m\033[36mMetricsCalculator Tests\033[0m\n"
              << "═══════════════════════\n\n";

    test_complexity_baseline();
    test_complexity_branches();
    test_complexity_high_risk();
    test_complexity_medium_risk();
    test_nesting_depth();
    test_parameter_count();
    test_no_parameters();
    test_multiple_functions();
    test_line_counts();
    test_file_risk_propagation();
    test_complexity_score();

    std::cout << "\n───────────────────────\n";
    if (g_passed == g_total) {
        std::cout << "\033[32m✅ All " << g_total << " tests passed.\033[0m\n\n";
        return 0;
    } else {
        std::cout << "\033[31m❌ " << (g_total - g_passed) << " / " << g_total
                  << " tests FAILED.\033[0m\n\n";
        return 1;
    }
}
