.PHONY: all pdf clean distclean help

PDF_DIRS := SIB SIB_FULL SIB_ECONOMIC_OBSERVABILITY

all: pdf

pdf:
	@set -e; \
	for dir in $(PDF_DIRS); do \
		echo "==> Building PDF in $$dir"; \
		$(MAKE) -C $$dir build; \
	done

clean:
	@set -e; \
	for dir in $(PDF_DIRS); do \
		echo "==> Cleaning build artifacts in $$dir"; \
		$(MAKE) -C $$dir clean; \
	done

distclean:
	@set -e; \
	for dir in $(PDF_DIRS); do \
		echo "==> Removing all generated artifacts in $$dir"; \
		$(MAKE) -C $$dir distclean; \
	done

help:
	@echo "Makefile targets:"
	@echo "  make pdf       - Build all PDFs in the repository"
	@echo "  make clean     - Remove LaTeX build artifacts in all PDF directories"
	@echo "  make distclean - Remove all generated artifacts, including PDFs"
	@echo "  make help      - Show this help message"
