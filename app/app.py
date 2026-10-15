from flask import Flask, render_template, request
from model.linprog import optimal_hiring_policy

app = Flask(__name__)

DEFAULT_PARAMS = {"alpha": 0.01, "beta": 0.02, "gamma": 0.9, "mu": 0.05, "lam": 0.05}
DEFAULT_POPULATION = [1000, 1050, 1100, 1150, 1200, 1250, 1300, 1350, 1400, 1450]


@app.route("/solve", methods=["GET", "POST"])
def solve():
    params = dict(DEFAULT_PARAMS)
    population = list(DEFAULT_POPULATION)
    n_init = 0.0
    result = error = None

    if request.method == "POST":
        try:
            params = {k: float(request.form[k]) for k in DEFAULT_PARAMS}
            n_init = float(request.form["n_init"])
            population = [float(request.form[f"p{i}"]) for i in range(10)]
            result = optimal_hiring_policy(
                params["alpha"], params["beta"], params["gamma"],
                params["lam"], params["mu"], population, n_init,
            )
            result["rows"] = list(zip(range(10), population, result["x"],
                                      result["yplus"], result["yminus"]))
        except (KeyError, ValueError, RuntimeError) as e:
            error = str(e)

    return render_template("solve.html", params=params, population=population, n_init=n_init,
                           result=result, error=error)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
