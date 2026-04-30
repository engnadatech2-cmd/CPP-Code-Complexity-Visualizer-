/**
 * test_comment_stripper.cpp
 *
 * Unit tests for CommentStripper.
 * All 6 tests from the SPEC are covered, plus edge-case extras.
 *
 * Invariants tested:
 *   1. Line count ALWAYS preserved (no lines added or removed)
 *   2. Non-comment source characters preserved verbatim
 *   3. Comment/string content replaced with spaces (same length)
 *   4. Keywords inside strings NOT treated as code
 *
 * Compile (from project root):
 *   g++ -std=c++17 -Wall -Wextra \
 *       analyzer/comment_stripper.cpp \
 *       tests/test_comment_stripper.cpp \
 *       -o tests/run_stripper_tests
 */

#include "../analyzer/comment_stripper.h"
#include <iostream>
#include <string>

static int g_total = 0, g_passed = 0;

static void check(const std::string& name, bool ok, const std::string& detail = "") {
    ++g_total;
    if (ok) { ++g_passed; std::cout << "  \033[32m[PASS]\033[0m " << name << "\n"; }
    else    { std::cout << "  \033[31m[FAIL]\033[0m " << name;
               if (!detail.empty()) std::cout << " — " << detail;
               std::cout << "\n"; }
}
static void checkEq(const std::string& name,
                    const std::string& got, const std::string& exp) {
    ++g_total;
    if (got == exp) { ++g_passed; std::cout << "  \033[32m[PASS]\033[0m " << name << "\n"; }
    else { std::cout << "  \033[31m[FAIL]\033[0m " << name << "\n"
                     << "         Exp: |" << exp << "|\n"
                     << "         Got: |" << got << "|\n"; }
}

static std::size_t nlCount(const std::string& s) {
    std::size_t n = 0; for (char c : s) if (c == '\n') ++n; return n;
}

static CommentStripper stripper;

// ── SPEC Test 1: simple line comment ─────────────────────────────────────────
void test1() {
    const std::string in = "int x = 5; // this is x\nint y = 6;";
    const std::string r  = stripper.strip(in);
    check("T1a: same total length",     in.size() == r.size(),
          "in=" + std::to_string(in.size()) + " out=" + std::to_string(r.size()));
    check("T1b: newlines preserved",    nlCount(in) == nlCount(r));
    check("T1c: 'int x = 5;' intact",  r.substr(0,10) == "int x = 5;");
    check("T1d: '//' removed",          r.find("//") == std::string::npos);
    const std::string line2 = r.substr(r.find('\n') + 1);
    check("T1e: second line intact",    line2 == "int y = 6;", "got:|" + line2 + "|");
}

// ── SPEC Test 2: block comment ────────────────────────────────────────────────
void test2() {
    const std::string in = "int x = /* value */ 5;";
    const std::string r  = stripper.strip(in);
    check("T2a: same length",     in.size() == r.size());
    check("T2b: prefix intact",   r.substr(0,8) == "int x = ", "got:|" + r.substr(0,8) + "|");
    check("T2c: ends with ' 5;'", r.size() >= 3 && r.substr(r.size()-3) == " 5;");
    check("T2d: no /* or */",     r.find("/*") == std::string::npos);
}

// ── SPEC Test 3: keyword inside string ───────────────────────────────────────
void test3() {
    const std::string in = "string s = \"if this is not code\";";
    const std::string r  = stripper.strip(in);
    check("T3a: same length",         in.size() == r.size());
    check("T3b: 'string s = ' intact", r.substr(0,11) == "string s = ");
    check("T3c: ends with ';'",        !r.empty() && r.back() == ';');
    check("T3d: 'if' gone after assign", r.substr(11).find("if") == std::string::npos);
}

// ── SPEC Test 4: comment-like inside string ───────────────────────────────────
void test4() {
    const std::string in = "cout << \"// not a comment\" << endl;";
    const std::string r  = stripper.strip(in);
    check("T4a: same length",         in.size() == r.size());
    check("T4b: 'cout << ' intact",   r.substr(0,8) == "cout << ");
    check("T4c: ' << endl;' at end",  r.size() >= 9 &&
                                       r.substr(r.size()-9) == " << endl;");
    check("T4d: '//' inside string gone", r.substr(8, r.size()-17).find("//") == std::string::npos);
}

// ── SPEC Test 5: multi-line block comment (line count critical) ───────────────
void test5() {
    const std::string in = "int a;\n/* line1\nline2\n*/\nint b;";
    const std::string r  = stripper.strip(in);
    check("T5a: newlines preserved", nlCount(in) == nlCount(r),
          "in=" + std::to_string(nlCount(in)) + " out=" + std::to_string(nlCount(r)));
    check("T5b: same total length",  in.size() == r.size());
    check("T5c: 'int a;' first",     r.substr(0,6) == "int a;");
    const std::string last = r.substr(r.rfind('\n')+1);
    check("T5d: 'int b;' last",      last == "int b;", "got:|" + last + "|");
    check("T5e: no /* or */",        r.find("/*") == std::string::npos);
}

// ── SPEC Test 6: escaped quote inside string ──────────────────────────────────
void test6() {
    const std::string in = "string s = \"say \\\"hello\\\"\";";
    const std::string r  = stripper.strip(in);
    check("T6a: same length",           in.size() == r.size());
    check("T6b: 'string s = ' intact",  r.substr(0,11) == "string s = ");
    check("T6c: ends with ';'",         !r.empty() && r.back() == ';');
    check("T6d: 'hello' blanked",       r.substr(11).find("hello") == std::string::npos);
}

// ── Extra tests ───────────────────────────────────────────────────────────────
void testExtras() {
    checkEq("Extra: empty input",        stripper.strip(""), "");
    const std::string noComment = "int main() {\n    return 0;\n}\n";
    checkEq("Extra: no-comment code unchanged", stripper.strip(noComment), noComment);

    const std::string unterm = "int a;\n/* unterminated\nint b;";
    const std::string ru = stripper.strip(unterm);
    check("Extra: unterminated block no crash", nlCount(unterm) == nlCount(ru));

    const auto lines = stripper.stripLines("a;\n//c\nb;\n/*x*/\nc;");
    check("Extra: stripLines count", lines.size() == 5,
          "got " + std::to_string(lines.size()));

    const std::string adj = "int a; // line\nint b = /* x */ 5;\nint c;";
    const std::string ra  = stripper.strip(adj);
    check("Extra: adjacent comments same length", adj.size() == ra.size());
    check("Extra: adjacent comments newlines ok", nlCount(adj) == nlCount(ra));
}

int main() {
    std::cout << "\n\033[1m\033[36mCommentStripper Tests\033[0m\n"
              << "═════════════════════\n\n";
    test1(); test2(); test3(); test4(); test5(); test6(); testExtras();
    std::cout << "\n─────────────────────\n";
    if (g_passed == g_total) {
        std::cout << "\033[32m✅ All " << g_total << " tests passed.\033[0m\n\n";
        return 0;
    }
    std::cout << "\033[31m❌ " << (g_total - g_passed) << " / " << g_total << " FAILED.\033[0m\n\n";
    return 1;
}
