# Implementation of the method(s) studied in the thesis

# Classical t-based confidence interval for the mean
ci_mean <- function(x, level = 0.95) {
  q <- qt(1 - (1 - level) / 2, df = length(x) - 1)
  mean(x) + c(-1, 1) * q * sd(x) / sqrt(length(x))
}
