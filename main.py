import json
from model.linprog import optimal_hiring_policy


alpha = 0.1
beta = 0.2
gamma = 0.95
lambda_ = 0.1
mu = 0.03

# Population and nurse stock initialization
population = [1000, 1050, 1100, 1000, 1000, 1000, 900]
n_init = 100

results = optimal_hiring_policy(alpha, beta, gamma, lambda_, mu, population, n_init)
print(json.dumps(results, indent=2))