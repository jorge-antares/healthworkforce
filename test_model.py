import json
from app.model.linprog import optimal_hiring_policy


alpha = 0.1
beta = 0.2
gamma = 0.95
lambda_ = 2.0
mu = 1.0
delta = 0.2

# Population and nurse stock initialization
population = [1000, 1050, 1100, 1000, 1000, 1000, 900]
n_init = 100

results = optimal_hiring_policy(
    alpha=alpha,
    beta=beta,
    gamma=gamma,
    lam=lambda_,
    mu=mu,
    delta=delta,
    population=population,
    n_init=n_init
    )
print(json.dumps(results, indent=2))