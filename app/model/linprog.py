"""Optimal hiring policy model (see presentation/presentation.tex)."""
import math

from ortools.linear_solver import pywraplp


def _as_list(v, n):
    if isinstance(v, (int, float)):
        return [float(v)] * n
    v = list(v)
    if len(v) != n:
        raise ValueError(f"Expected {n} values, got {len(v)}")
    return v


def optimal_hiring_policy(alpha, beta, gamma, lam, mu, population, delta, n_init=0.0):
    """Solve the optimal hiring LP.

    min sum_t lam * e^{-delta * t} y+_t + sum_t mu * e^{-delta * t} y-_t
    s.t. d_t = alpha_t p_t;  s_t = beta_t n_t;  d_t - s_t = y+_t - y-_t;
         n_t = gamma n_{t-1} + x_t;  x, y+, y- >= 0

    alpha, beta: scalar or list (one value per period); gamma, lam, mu: scalars;
    population: list of population per period t = 0..T; n_init: nurses before t = 0.
    Returns dict with keys "x", "yplus", "yminus" (lists) and "objfun".
    """
    T = len(population)
    alpha = _as_list(alpha, T)
    beta = _as_list(beta, T)

    solver = pywraplp.Solver.CreateSolver("SCIP")
    if solver is None:
        raise RuntimeError("Could not create the SCIP solver")
    inf = solver.infinity()

    x = [solver.IntVar(0, inf, f"x_{t}") for t in range(T)]
    yp = [solver.NumVar(0, inf, f"yplus_{t}") for t in range(T)]
    ym = [solver.NumVar(0, inf, f"yminus_{t}") for t in range(T)]
    n = [solver.NumVar(0, inf, f"n_{t}") for t in range(T)]

    for t in range(T):
        prev = gamma * n[t - 1] if t > 0 else gamma * n_init
        solver.Add(n[t] == prev + x[t])
        # d_t - s_t = y+_t - y-_t with d_t = alpha_t p_t, s_t = beta_t n_t
        solver.Add(alpha[t] * population[t] - beta[t] * n[t] == yp[t] - ym[t])

    solver.Minimize(
        solver.Sum(lam * math.exp(-delta * t) * yp[t] for t in range(T))
        + solver.Sum(mu * math.exp(-delta * t) * ym[t] for t in range(T))
    )

    status = solver.Solve()
    if status != pywraplp.Solver.OPTIMAL:
        raise RuntimeError(f"Solver did not find an optimal solution (status {status})")

    return {
        "x": [round(v.solution_value(),3) for v in x],
        "yplus": [round(v.solution_value(),3) for v in yp],
        "yminus": [round(v.solution_value(),3) for v in ym],
        "objfun": solver.Objective().Value(),
    }
