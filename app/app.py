from flask import Flask, render_template, request
from model.linprog import optimal_hiring_policy

app = Flask(__name__)

DEFAULT_PARAMS = {"alpha": 0.01, "beta": 0.02, "gamma": 0.9, "lam": 2.0, "mu": 1.0, "delta": 0.03}
DEFAULT_POPULATION = [1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450]


@app.route("/solve", methods=["GET", "POST"])
def solve():
    params = dict(DEFAULT_PARAMS)
    population = list(DEFAULT_POPULATION)
    n_init = 400.0
    result = error = None

    if request.method == "POST":
        try:
            params = {k: float(request.form[k]) for k in DEFAULT_PARAMS}
            n_init = float(request.form["n_init"])
            population = [float(request.form[f"p{i}"]) for i in range(10)]
            result = optimal_hiring_policy(
                alpha=params["alpha"],
                beta=params["beta"],
                gamma=params["gamma"],
                lam=params["lam"],
                mu=params["mu"],
                delta=params["delta"],
                population=population,
                n_init=n_init,
            )
            n, prev = [], n_init
            for x in result["x"]:
                prev = params["gamma"] * prev + x
                n.append(prev)
            result["demand"] = [round(params["alpha"] * p, 3) for p in population]
            result["supply"] = [round(params["beta"] * v, 3) for v in n]
            result["rows"] = list(zip(range(10), population, result["x"],
                                      result["yplus"], result["yminus"]))
        except (KeyError, ValueError, RuntimeError) as e:
            error = str(e)

    return render_template(
        "solve.html",
        params=params,
        population=population,
        n_init=n_init,
        result=result,
        error=error
        )

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
