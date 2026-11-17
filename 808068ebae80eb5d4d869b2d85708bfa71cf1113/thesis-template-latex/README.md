# Seminar Thesis Template (LaTeX / Overleaf)

LaTeX template for the seminar thesis in the Statistics Seminar.

## Getting Started on Overleaf

1. Log in to [Overleaf](https://www.overleaf.com).
2. Choose **New Project → Upload Project** and upload `thesis-template-latex.zip`.
3. Open `thesis.tex` and click **Recompile**. The compiler is pdfLaTeX (Overleaf's default).
4. Share the project with your group members (**Share** button).

With a local LaTeX installation, compile with `latexmk -pdf thesis.tex`.

## Files

* `thesis.tex`: the thesis text. It already implements all formal requirements.
* `references.bib`: your literature in BibTeX format. Cite with `\textcite{key}` or `\parencite{key}`.
* `R/functions.R`: your implementation of the method.
* `R/simulation.R`: your Monte Carlo simulation study. It writes the table (`results/coverage-table.tex`), the figure (`results/coverage.pdf`), and the number of replications (`results/settings.tex`) that `thesis.tex` includes.
* `results/`: output of `R/simulation.R`. The example results are included so that the template compiles right away.

## Code

Overleaf cannot run R or Python. Run your code on your own computer, from the folder that contains `thesis.tex`:

```
Rscript R/simulation.R
```

Then upload the updated files in `results/` to your Overleaf project (replace the old ones).

Code does not belong in the main text. Show only short snippets that help the reader understand the method (`lstlisting` environment).

Python users: replace the R files with Python files that write the same kind of output (a `.tex` table and a `.pdf` figure), and set `language = Python` in `thesis.tex`.

## Submission

* `thesis.pdf` (Overleaf: **Download PDF**)
* A ZIP file of the whole project including your code (Overleaf: **Menu → Download → Source**, then add the `R/` folder if you kept your code outside Overleaf), so that all results can be reproduced.
