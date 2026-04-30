.PHONY: all build clean distclean view help

TEX_FILE := sib_economic_observability.tex
PDF_FILE := $(TEX_FILE:.tex=.pdf)
AUX_FILES := $(TEX_FILE:.tex=.aux) $(TEX_FILE:.tex=.log) $(TEX_FILE:.tex=.out) \
	$(TEX_FILE:.tex=.fls) $(TEX_FILE:.tex=.fdb_latexmk)

all: build

build:
	pdflatex $(TEX_FILE)

clean:
	rm -f $(AUX_FILES)

distclean: clean
	rm -f $(PDF_FILE)

view: build
	open $(PDF_FILE)

help:
	@echo "Makefile targets:"
	@echo "  make build     - Compile the LaTeX document to PDF"
	@echo "  make clean     - Remove build artifacts (keep PDF)"
	@echo "  make distclean - Remove all artifacts including PDF"
	@echo "  make view      - Compile and open the PDF"
	@echo "  make help      - Show this help message"
