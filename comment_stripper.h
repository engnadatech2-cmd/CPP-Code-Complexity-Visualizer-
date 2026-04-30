#pragma once
#include <string>
#include <vector>

/**
 * CommentStripper
 *
 * Uses a 4-state machine to remove C++ comments (// and /* *\/)
 * and string literals from source code, while preserving line numbers
 * by replacing removed content with spaces instead of deleting lines.
 *
 * States:
 *   CODE          - Normal C++ code
 *   LINE_COMMENT  - After // until end of line
 *   BLOCK_COMMENT - After /* until *\/
 *   STRING        - Inside "" or ''
 */
class CommentStripper {
public:
    /**
     * Strip all comments and string literals from the given C++ source.
     * Line count is preserved; removed content becomes spaces.
     *
     * @param source  Raw C++ source code as a single string
     * @return        Cleaned code with comments/strings replaced by spaces
     */
    std::string strip(const std::string& source) const;

    /**
     * Same as strip(), but splits the result into individual lines.
     * Useful for testing and for line-by-line analysis.
     *
     * @param source  Raw C++ source code
     * @return        Vector of cleaned lines (preserves line count)
     */
    std::vector<std::string> stripLines(const std::string& source) const;

private:
    enum class State {
        CODE,
        LINE_COMMENT,
        BLOCK_COMMENT,
        STRING
    };
};
