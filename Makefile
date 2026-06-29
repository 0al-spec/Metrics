.PHONY: all pdf validate validate-idea-maturity clean distclean help

PDF_DIRS := SIB SIB_FULL SIB_ECONOMIC_OBSERVABILITY
PYTHON ?= python3

all: pdf

pdf:
	@set -e; \
	for dir in $(PDF_DIRS); do \
		echo "==> Building PDF in $$dir"; \
		$(MAKE) -C $$dir build; \
	done

validate: validate-idea-maturity

validate-idea-maturity:
	@$(PYTHON) scripts/metrics.py validate idea-maturity
	@$(PYTHON) scripts/validate_idea_maturity_examples.py

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
	@echo "  make validate  - Validate machine-readable metric-pack examples"
	@echo "  make clean     - Remove LaTeX build artifacts in all PDF directories"
	@echo "  make distclean - Remove all generated artifacts, including PDFs"
	@echo "  make help      - Show this help message"
