import math
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "clave-solo-para-desarrollo"
# Base de datos en memoria para pruebas de clase
tasks = [
    {"id": 1, "title": "Levantamiento de requerimientos", "cost": 150},
    {"id": 2, "title": "Diseño de arquitectura", "cost": 300}
]

@app.route('/')
def index():
    # BUG 1: Si cost entra como string, causa TypeError al sumar int con str o concatena
    total_budget = sum([t["cost"] for t in tasks]) if tasks else 0
    return render_template('index.html', tasks=tasks, total_budget=total_budget)

@app.route('/task/add', methods=['POST'])
def add_task():
    title = (request.form.get('title') or '').strip()
    cost_raw = (request.form.get('cost') or '').strip()

    # RFC-003: validar el título
    if not title:
        flash("El nombre de la tarea es obligatorio.")
        return redirect(url_for('index'))
    if len(title) > 100:
        flash("El nombre no puede exceder 100 caracteres.")
        return redirect(url_for('index'))

    # RFC-003: validar el costo
    try:
        cost = float(cost_raw)
    except ValueError:
        flash("El costo debe ser un número válido.")
        return redirect(url_for('index'))
    if not math.isfinite(cost) or cost < 0:
        flash("El costo debe ser un número positivo.")
        return redirect(url_for('index'))

    new_id = max((t["id"] for t in tasks), default=0) + 1
    tasks.append({
        "id": new_id,
        "title": title,
        "cost": round(cost, 2)
    })
    return redirect(url_for('index'))

@app.route('/task/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
