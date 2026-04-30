#include "comment_stripper.h"
#include <sstream>

// ---------------------------------------------------------------------------
// CommentStripper::strip
// ---------------------------------------------------------------------------
// Core 4-state machine.  Walks the source character by character.
// Rules (see SPEC for the full state transition table):
//
//   STATE_CODE:
//     //  -> LINE_COMMENT  (emit space x2 in place of the two slashes)
//     /*  -> BLOCK_COMMENT (emit space x2)
//     "   -> STRING        (emit space)
//     \n  -> stay CODE     (emit \n to preserve line numbers)
//     else-> emit char as-is
//
//   STATE_LINE_COMMENT:
//     \n  -> CODE          (emit \n)
//     else-> emit space
//
//   STATE_BLOCK_COMMENT:
//     */  -> CODE          (emit space x2)
//     \n  -> stay BLOCK    (emit \n — critical for line preservation)
//     else-> emit space
//
//   STATE_STRING:
//     \"  -> stay STRING   (escaped quote, emit space x2)
//     "   -> CODE          (emit space)
//     \n  -> CODE          (broken literal, emit \n)
//     else-> emit space
// ---------------------------------------------------------------------------

std::string CommentStripper::strip(const std::string& source) const {
    std::string result;
    result.reserve(source.size());

    State state = State::CODE;
    const std::size_t len = source.size();

    for (std::size_t i = 0; i < len; ++i) {
        const char c  = source[i];
        const char nc = (i + 1 < len) ? source[i + 1] : '\0';

        switch (state) {

        // ── CODE ──────────────────────────────────────────────────────────
        case State::CODE:
            if (c == '/' && nc == '/') {
                // Start of line comment
                result += "  ";   // replace // with two spaces
                state = State::LINE_COMMENT;
                ++i;              // consume the second '/'
            } else if (c == '/' && nc == '*') {
                // Start of block comment
                result += "  ";
                state = State::BLOCK_COMMENT;
                ++i;              // consume '*'
            } else if (c == '"' || c == '\'') {
                // Start of string/char literal
                result += ' ';
                state = State::STRING;
            } else if (c == '\n') {
                result += '\n';   // preserve newline
            } else {
                result += c;      // normal code character
            }
            break;

        // ── LINE COMMENT ──────────────────────────────────────────────────
        case State::LINE_COMMENT:
            if (c == '\n') {
                result += '\n';   // end of comment, preserve line
                state = State::CODE;
            } else {
                result += ' ';    // replace comment content with space
            }
            break;

        // ── BLOCK COMMENT ─────────────────────────────────────────────────
        case State::BLOCK_COMMENT:
            if (c == '*' && nc == '/') {
                result += "  ";   // replace */ with two spaces
                state = State::CODE;
                ++i;              // consume '/'
            } else if (c == '\n') {
                result += '\n';   // IMPORTANT: preserve newline inside block
            } else {
                result += ' ';
            }
            break;

        // ── STRING ────────────────────────────────────────────────────────
        case State::STRING:
            if (c == '\\' && nc == '"') {
                // Escaped quote — stay in STRING
                result += "  ";
                ++i;
            } else if (c == '\\' && nc == '\'') {
                // Escaped single quote — stay in STRING
                result += "  ";
                ++i;
            } else if (c == '"' || c == '\'') {
                // End of string literal
                result += ' ';
                state = State::CODE;
            } else if (c == '\n') {
                // Unterminated string literal — return to CODE
                result += '\n';
                state = State::CODE;
            } else {
                result += ' ';
            }
            break;
        }
    }

    return result;
}

// ---------------------------------------------------------------------------
// CommentStripper::stripLines
// ---------------------------------------------------------------------------
std::vector<std::string> CommentStripper::stripLines(const std::string& source) const {
    const std::string stripped = strip(source);
    std::vector<std::string> lines;
    std::istringstream stream(stripped);
    std::string line;
    while (std::getline(stream, line)) {
        lines.push_back(line);
    }
    return lines;
}
