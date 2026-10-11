import math
import os

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
# Necesaria para mostrar los mensajes de validación con flash()
app.secret_key = os.environ.get("SECRET_KEY", "clave-solo-para-desarrollo")

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

def validate_task(title, cost_raw):
    """Devuelve un mensaje de error si los datos no son válidos; None si lo son."""
    if not title:
        return "El nombre de la tarea es obligatorio."
    try:
        cost = float(cost_raw)
    except ValueError:
        return "El costo es obligatorio y debe ser un valor numérico."
    if not math.isfinite(cost) or cost < 0:
        return "El costo debe ser un número mayor o igual a 0."
    return None

@app.route('/task/add', methods=['POST'])
def add_task():
    title = (request.form.get('title') or '').strip()
    cost_raw = (request.form.get('cost') or '').strip()

    # Si algún dato es inválido se rechaza la solicitud y no se registra nada
    error = validate_task(title, cost_raw)
    if error:
        flash(error)
        return redirect(url_for('index'))

    new_id = len(tasks) + 1
    tasks.append({
        "id": new_id,
        "title": title,
        "cost": cost_raw
    })
    return redirect(url_for('index'))

@app.route('/task/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
