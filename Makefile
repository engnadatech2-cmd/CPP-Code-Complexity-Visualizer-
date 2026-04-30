# ═══════════════════════════════════════════════════════════════
# C++ Code Complexity Visualizer — Makefile
# ═══════════════════════════════════════════════════════════════
# Usage:
#   make            — build the analyzer binary
#   make test       — build & run all unit tests
#   make demo       — analyze sample_files, open browser report
#   make clean      — remove build artifacts
# ═══════════════════════════════════════════════════════════════

CXX      := g++
CXXFLAGS := -std=c++17 -Wall -Wextra -Wpedantic -O2

# Source files (all in analyzer/)
SRCS := analyzer/comment_stripper.cpp \
        analyzer/metrics_calculator.cpp \
        analyzer/dependency_graph.cpp \
        analyzer/json_exporter.cpp \
        analyzer/main.cpp

OBJS     := $(SRCS:.cpp=.o)
TARGET   := analyzer/analyzer

# Test binaries
TEST_STRIPPER_SRC := tests/test_comment_stripper.cpp \
                     analyzer/comment_stripper.cpp
TEST_METRICS_SRC  := tests/test_metrics.cpp \
                     analyzer/comment_stripper.cpp \
                     analyzer/metrics_calculator.cpp

TEST_STRIPPER_BIN := tests/run_stripper_tests
TEST_METRICS_BIN  := tests/run_metrics_tests

# Output directory
OUTPUT_DIR := output

# ── Default target ───────────────────────────────────────────────
.PHONY: all
all: $(TARGET)

$(TARGET): $(SRCS)
	@echo "🔨 Building analyzer..."
	@mkdir -p $(OUTPUT_DIR)
	$(CXX) $(CXXFLAGS) -o $@ $^
	@echo "✅ Built: $@"

# ── Tests ────────────────────────────────────────────────────────
.PHONY: test test-stripper test-metrics
test: test-stripper test-metrics

test-stripper: $(TEST_STRIPPER_SRC)
	@echo ""
	@echo "🔨 Building CommentStripper tests..."
	$(CXX) $(CXXFLAGS) -o $(TEST_STRIPPER_BIN) $^
	@echo "▶  Running CommentStripper tests..."
	@./$(TEST_STRIPPER_BIN)

test-metrics: $(TEST_METRICS_SRC)
	@echo ""
	@echo "🔨 Building MetricsCalculator tests..."
	$(CXX) $(CXXFLAGS) -o $(TEST_METRICS_BIN) $^
	@echo "▶  Running MetricsCalculator tests..."
	@./$(TEST_METRICS_BIN)

# ── Demo: analyze sample files ───────────────────────────────────
.PHONY: demo
demo: $(TARGET)
	@echo ""
	@echo "🔍 Running demo on tests/sample_files..."
	@mkdir -p $(OUTPUT_DIR)
	./$(TARGET) --path tests/sample_files \
	            --name "Sample Files" \
	            --output $(OUTPUT_DIR)/demo.json
	@echo ""
	@echo "🐍 Generating HTML report..."
	python3 visualizer/html_generator.py $(OUTPUT_DIR)/demo.json \
	        --out $(OUTPUT_DIR)/demo.html

# ── Clean ────────────────────────────────────────────────────────
.PHONY: clean
clean:
	@echo "🧹 Cleaning build artifacts..."
	@rm -f $(TARGET) $(TEST_STRIPPER_BIN) $(TEST_METRICS_BIN)
	@rm -f $(OUTPUT_DIR)/*.json $(OUTPUT_DIR)/*.html
	@echo "✅ Clean done."

# ── Help ─────────────────────────────────────────────────────────
.PHONY: help
help:
	@echo ""
	@echo "  \033[1mC++ Code Complexity Visualizer\033[0m"
	@echo ""
	@echo "  make           Build the analyzer binary"
	@echo "  make test      Build & run all unit tests"
	@echo "  make demo      Analyze sample files + open browser report"
	@echo "  make clean     Remove build artifacts"
	@echo ""
	@echo "  Manual usage:"
	@echo "    ./analyzer/analyzer --path <dir> [--name <name>] [--output <file>]"
	@echo "    python3 visualizer/html_generator.py <output.json>"
	@echo ""
