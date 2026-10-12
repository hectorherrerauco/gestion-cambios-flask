import math
from decimal import Decimal, InvalidOperation

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

MAX_TITLE_LENGTH = 100
MAX_COST_DECIMAL_PLACES = 2

# Base de datos en memoria para pruebas
tasks = [
    {"id": 1, "title": "Levantamiento de requerimientos", "cost": 150},
    {"id": 2, "title": "Diseño de arquitectura", "cost": 300},
]


@app.route("/")
def index():
    total_budget = sum(task["cost"] for task in tasks)
    return render_template(
        "index.html",
        tasks=tasks,
        total_budget=total_budget,
    )


@app.route("/task/add", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    cost_raw = request.form.get("cost", "").strip()

    if not title:
        return "Error: el nombre de la tarea es obligatorio.", 400
    if len(title) > MAX_TITLE_LENGTH:
        return f"Error: el nombre no puede superar {MAX_TITLE_LENGTH} caracteres.", 400
    if not cost_raw:
        return "Error: el costo es obligatorio.", 400

    try:
        cost_decimal = Decimal(cost_raw)
    except InvalidOperation:
        return "Error: debes introducir un costo numérico válido.", 400

    if not cost_decimal.is_finite():
        return "Error: el costo debe ser un número válido.", 400
    if cost_decimal < 0:
        return "Error: el costo no puede ser negativo.", 400
    cost_parts = cost_decimal.as_tuple()
    decimal_places = cost_parts.exponent
    remaining_digits = list(cost_parts.digits)
    while decimal_places < 0 and remaining_digits and remaining_digits[-1] == 0:
        remaining_digits.pop()
        decimal_places += 1
    if decimal_places < -MAX_COST_DECIMAL_PLACES:
        return f"Error: el costo admite como máximo {MAX_COST_DECIMAL_PLACES} decimales.", 400

    cost = float(cost_decimal)
    if not math.isfinite(cost):
        return "Error: el costo está fuera del rango permitido.", 400
    if not math.isfinite(sum(task["cost"] for task in tasks) + cost):
        return "Error: el presupuesto total está fuera del rango permitido.", 400

    new_id = max((task["id"] for task in tasks), default=0) + 1
    tasks.append({"id": new_id, "title": title, "cost": cost})

    return redirect(url_for("index"))


@app.route("/task/remove/<int:task_id>", methods=["POST"])
@app.route("/task/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)

