# Monte Carlo simulation study
# Run from the folder that contains thesis.qmd; saves results/simulation.rds

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
saveRDS(list(results = results, B = B), "results/simulation.rds")
