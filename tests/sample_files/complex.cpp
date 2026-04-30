/**
 * complex.cpp
 * Intentionally high-complexity file for testing risk classification.
 * Expected: several "high" risk functions.
 */

#include <vector>
#include <string>
#include <stdexcept>

// ── processData: HIGH risk (many branches + deep nesting) ────────
int processData(const std::vector<int>& data, int mode, bool strict) {
    if (data.empty()) {
        throw std::invalid_argument("Empty data");
    }

    int result = 0;

    for (std::size_t i = 0; i < data.size(); ++i) {
        if (data[i] > 0) {
            if (mode == 1) {
                if (strict) {
                    if (data[i] > 100) {
                        result += data[i] * 2;
                    } else {
                        result += data[i];
                    }
                } else {
                    result += data[i];
                }
            } else if (mode == 2) {
                for (int j = 0; j < data[i]; ++j) {
                    result += (j % 2 == 0) ? j : -j;
                }
            } else {
                switch (data[i] % 3) {
                    case 0: result += data[i]; break;
                    case 1: result -= data[i]; break;
                    case 2: result ^= data[i]; break;
                    default: break;
                }
            }
        } else if (data[i] < 0) {
            result -= data[i];
        }
    }

    return result;
}

// ── validate: MEDIUM risk ────────────────────────────────────────
bool validate(const std::string& input, int minLen, int maxLen) {
    if (input.empty()) return false;
    if (static_cast<int>(input.size()) < minLen) return false;
    if (static_cast<int>(input.size()) > maxLen) return false;

    for (char c : input) {
        if (!std::isalnum(static_cast<unsigned char>(c)) && c != '_' && c != '-') {
            return false;
        }
    }
    return true;
}

// ── simple helper: LOW risk ──────────────────────────────────────
int clamp(int value, int lo, int hi) {
    if (value < lo) return lo;
    if (value > hi) return hi;
    return value;
}
