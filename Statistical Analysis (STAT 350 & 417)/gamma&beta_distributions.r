# HW 10: Q1
# Parameters for the first gamma distribution
shape1 <- 2
rate1 <- 1

# Parameters for the second gamma distribution
shape2 <- 3
rate2 <- 2

# Define a sequence of x values for evaluation
x <- seq(0, 10, length.out = 100)

# Compute the cumulative gamma distributions
gamma1 <- pgamma(x, shape = shape1, rate = rate1)
gamma2 <- pgamma(x, shape = shape2, rate = rate2)

# Divide the two gamma distributions
gamma_ratio <- gamma1 / gamma2

# Plot the results
plot(x, gamma_ratio, type = "l", col = "blue", lwd = 2,
     main = "Ratio of Two Gamma Distributions",
     xlab = "x", ylab = "gamma1(x) / gamma2(x)")
grid()

## FROM HW SOLUTION
alpha <- 2
beta <- 2
n <- 3
x <- c(2, 5, 1)
S <- sum(x)
posterior_odds <- (1-pgamma(1,alpha+S,beta+n))/(pgamma(1,alpha+S,beta+n))
prior_odds <- (1-pgamma(1,alpha,beta))/(pgamma(1,alpha,beta))
BF <- posterior_odds/prior_odds
print(BF)

# HW10: Q2
# Parameters for the first beta distribution
shape1_a <- 2
shape1_b <- 5

# Parameters for the second beta distribution
shape2_a <- 3
shape2_b <- 4

# Define a sequence of x values for evaluation
x <- seq(0, 1, length.out = 100)

# Compute the beta PDFs
beta1 <- dbeta(x, shape1_a, shape1_b)
beta2 <- dbeta(x, shape2_a, shape2_b)

# Divide the two beta distributions
beta_ratio <- beta1 / beta2

# Plot the results
plot(x, beta_ratio, type = "l", col = "red", lwd = 2,
     main = "Ratio of Two Beta Distributions",
     xlab = "x", ylab = "beta1(x) / beta2(x)")
grid()

## FROM HW SOLUTION
alpha <- 2
beta <- 2
n <- 10
S <- 7
posterior_odds <- (1-pbeta(0.5,alpha+S,beta+n-S))/(pbeta(0.5,alpha+S,beta+n-S))
prior_odds <- (1-pbeta(0.5,alpha,beta))/(pbeta(0.5,alpha,beta))
BF <- posterior_odds/prior_odds
print(BF)
