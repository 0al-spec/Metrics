.PHONY: all build clean view help

# Default target
all: build

# Compile the LaTeX document
build:
	pdflatex metrics.tex

# Clean build artifacts (keep PDF)
clean:
	rm -f metrics.aux metrics.log metrics.out metrics.fls metrics.fdb_latexmk

# Clean all artifacts including PDF
distclean: clean
	rm -f metrics.pdf

# View the compiled PDF
view: build
	open metrics.pdf

# Help message
help:
	@echo "Makefile targets:"
	@echo "  make build     - Compile the LaTeX document to PDF"
	@echo "  make clean     - Remove build artifacts (keep PDF)"
	@echo "  make distclean - Remove all artifacts including PDF"
	@echo "  make view      - Compile and open the PDF"
	@echo "  make help      - Show this help message"
