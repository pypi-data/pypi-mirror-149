import ProbDistro.discrete_distributions.binomial as binomial
import ProbDistro.discrete_distributions.bernoulli as bernoulli
import ProbDistro.discrete_distributions.poisson as poisson
import ProbDistro.discrete_distributions.geometric as geometric
import ProbDistro.continuous_distributions.normal as normal
import ProbDistro.continuous_distributions.exponential as exponential


def binomial_to_normal(binomial_distro: binomial.Binomial) -> normal.Normal:
    mu = binomial_distro.n * binomial_distro.p
    sigma = mu * binomial_distro.q

    return normal.Normal(mu, sigma)


def normal_to_binomial(normal_distro: normal.Normal) -> binomial.Binomial:
    q = normal_distro.sigma / normal_distro.mu
    p = 1 - q
    n = normal_distro.mu / p

    return binomial.Binomial(int(n), p)


def bernoulli_to_binomial(bernoulli_distro: bernoulli.Bernoulli) -> binomial.Binomial:
    return binomial.Binomial(1, bernoulli_distro.p)


def binomial_to_bernoulli(binomial_distro: binomial.Binomial) -> bernoulli.Bernoulli:
    return bernoulli.Bernoulli(binomial_distro.p)


def binomial_to_poisson(binomial_distro: binomial.Binomial) -> poisson.Poisson:
    return poisson.Poisson(binomial_distro.n * binomial_distro.p)


def exponential_to_poisson(exponential_distro: exponential.Exponential) -> poisson.Poisson:
    return poisson.Poisson(1 / exponential_distro.rate)


def poisson_to_exponential(poisson_distro: poisson.Poisson) -> exponential.Exponential:
    return exponential.Exponential(1 / poisson_distro.rate)


def exponential_to_geometric(exponential_distro: exponential.Exponential) -> geometric.Geometric:
    return geometric.Geometric(1 + exponential_distro.rate)


def geometric_to_exponential(geometric_distro: geometric.Geometric) -> exponential.Exponential:
    return exponential.Exponential(geometric_distro.p - 1)
