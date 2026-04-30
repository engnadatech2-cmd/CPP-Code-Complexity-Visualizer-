/*
 * with_comments.cpp
 * Demonstrates various C++ comment styles that must be stripped correctly.
 */

#include <vector>
#include <string>

// ── Constants ────────────────────────────────────────────────────
/* Maximum number of retries */
const int MAX_RETRIES = 3;

/**
 * Check if a value is positive.
 * @param x  The value to check.
 * @return   true if x > 0.
 */
bool isPositive(int x) {
    // Simple check
    return x > 0;  // return result
}

// This function has a string that looks like a comment: "// not a comment"
void trickyCases() {
    std::string s = "// this is inside a string, not a comment";
    std::string t = "/* also not */ a real comment";
    /* but THIS
       is a real
       multi-line comment */
    std::string u = "done";
}

/**
 * Binary search — medium complexity.
 */
int binarySearch(const std::vector<int>& arr, int target) {
    int lo = 0, hi = static_cast<int>(arr.size()) - 1;

    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (arr[mid] == target) {
            return mid;      // found
        } else if (arr[mid] < target) {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    return -1; // not found
}
