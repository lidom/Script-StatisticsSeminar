# Monte Carlo simulation study
# Run from the folder that contains thesis.tex:  Rscript R/simulation.R
# It writes the table and the figure that thesis.tex includes to results/.
# Upload the updated results/ folder to Overleaf afterwards.

source("R/functions.R")
set.seed(123)

B  <- 5000                     # number of Monte Carlo replications
ns <- c(10, 25, 50, 100, 250)  # sample sizes

# Data generating processes: name, sampler, true mean
dgps <- list(
  list(name = "Normal (baseline)",        rdata = function(n) rnorm(n),          mu = 0),
  list(name = "Exponential (skewed)",     rdata = function(n) rexp(n),           mu = 1),
  list(name = "Log-normal (very skewed)", rdata = function(n) rlnorm(n, sdlog = 1.5),
       mu = exp(1.5^2 / 2))
)

results <- do.call(rbind, lapply(dgps, function(dgp) {
  do.call(rbind, lapply(ns, function(n) {
    covered <- replicate(B, {
      ci <- ci_mean(dgp$rdata(n))
      ci[1] <= dgp$mu && dgp$mu <= ci[2]
    })
    data.frame(dgp = dgp$name, n = n, coverage = mean(covered))
  }))
}))

dir.create("results", showWarnings = FALSE)

## Table: one row per data generating process, one column per sample size
tab <- reshape(results, idvar = "dgp", timevar = "n", direction = "wide")
lines <- c(
  paste0("\\begin{tabular}{l", strrep("r", length(ns)), "}"),
  "\\toprule",
  paste0("Distribution & ", paste0("$n = ", ns, "$", collapse = " & "), " \\\\"),
  "\\midrule",
  apply(tab, 1, function(row) {
    paste0(row[1], " & ",
           paste(sprintf("%.3f", as.numeric(row[-1])), collapse = " & "), " \\\\")
  }),
  "\\bottomrule",
  "\\end{tabular}"
)
writeLines(lines, "results/coverage-table.tex")

## Figure
pdf("results/coverage.pdf", width = 6, height = 3.5)
par(mar = c(4, 4, 1, 1))
plot(NULL, xlim = range(ns), ylim = c(min(results$coverage, 0.85), 1),
     log = "x", xlab = "Sample size n", ylab = "Coverage probability")
abline(h = 0.95, lty = 2)
for (i in seq_along(dgps)) {
  d <- results[results$dgp == dgps[[i]]$name, ]
  lines(d$n, d$coverage, type = "b", pch = i, lty = 1)
}
legend("bottomright", legend = sapply(dgps, `[[`, "name"), pch = seq_along(dgps),
       bty = "n")
invisible(dev.off())

## Number of replications, so that the text can use \nreps
writeLines(paste0("\\newcommand{\\nreps}{", B, "}"), "results/settings.tex")
