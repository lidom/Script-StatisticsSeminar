# Seminar Thesis Template

Quarto template for the seminar thesis in the Statistics Seminar.

## Files

* `thesis.qmd`: the thesis text. Render it with `quarto render thesis.qmd` to get `thesis.pdf`.
* `R/functions.R`: your implementation of the method.
* `R/simulation.R`: your Monte Carlo simulation study. It saves its results to `results/simulation.rds`, which `thesis.qmd` reads, so the (possibly slow) simulation does not rerun every time you render. Delete `results/simulation.rds` to rerun it.
* `references.bib`: your literature in BibTeX format. Cite with `@key`.

## Code

Code is hidden in the PDF by default. Show only short snippets that help the reader understand the method (`#| echo: true`). Put everything else in the `R/` folder.

Python users: replace the R files with Python files and the R chunks with Python chunks; the structure stays the same.

## Submission

* `thesis.pdf`
* A ZIP file of this whole folder, so that all results can be reproduced by rendering `thesis.qmd`.
