# Makefile for VAM Papers and Appendices

MAIN = main
APPENDICES = Appendix_1 Appendix_2

.PHONY: all clean standalone

all: $(MAIN).pdf

%.pdf: %.tex
	pdflatex -interaction=nonstopmode $<
	bibtex $(basename $<) || true
	pdflatex -interaction=nonstopmode $<
	pdflatex -interaction=nonstopmode $<

standalone:
	for f in $(APPENDICES); do \
		pdflatex -interaction=nonstopmode sections/$$f.tex; \
		bibtex sections/$$f || true; \
		pdflatex -interaction=nonstopmode sections/$$f.tex; \
		pdflatex -interaction=nonstopmode sections/$$f.tex; \
	done

clean:
	rm -f *.aux *.log *.bbl *.blg *.toc *.out sections/*.aux sections/*.log sections/*.bbl sections/*.blg
