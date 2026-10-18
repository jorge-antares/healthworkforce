# Health Workforce Optimal Hiring

A small web application that computes an optimal nurse hiring policy over a 10-period horizon. Healthcare staffing demand is modeled as proportional to population, and the hiring plan minimizes the discounted cost of understaffing and overstaffing.

## Model

The model is a linear program solved with Google OR-Tools (SCIP). Over periods t, it minimizes the discounted penalties on shortage (`y+`) and surplus (`y-`):

- Demand: `d_t = alpha * p_t`
- Supply: `s_t = beta * n_t`
- Balance: `d_t - s_t = y+_t - y-_t`
- Workforce dynamics: `n_t = gamma * n_{t-1} + x_t`, where `x_t` is the number hired (non-negative integer)

Parameters: `alpha`, `beta`, `gamma` (retention), `lam` (shortage cost), `mu` (surplus cost), `delta` (discount rate), the population per period, and the initial workforce `n_init`. The implementation is in [app/model/linprog.py](app/model/linprog.py). Further details are in [presentation/presentation.pdf](presentation/presentation.pdf).

## Project structure

- `app/` - Flask application (`app.py`, `model/`, `templates/`, `Dockerfile`)
- `nginx/` - Nginx reverse proxy configuration, logs, and SSL certificates
- `compose.yml` - Docker Compose setup (Flask app and Nginx)
- `presentation/` - LaTeX source and PDF of the model description
- `test_model.py` - Example script that runs the solver and prints the result as JSON

## Running

With Docker (app behind Nginx on ports 80 and 443):

```
make run
```

Nginx expects its configuration in `nginx/conf.d` and certificates in `nginx/ssl`.

Locally without Docker:

```
python -m venv .venv
source .venv/bin/activate
pip install -r app/requirements.txt
cd app && python app.py
```

The app is then available at http://127.0.0.1:5000. The solver form is at `/solve`.

Run the example script from the repository root:

```
python test_model.py
```

## Presentation

Rebuild the PDF with `make create-pdf` (requires a LaTeX installation).
