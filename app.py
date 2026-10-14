from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Base de datos en memoria para pruebas de clase
tasks = [
    {"id": 1, "title": "Levantamiento de requerimientos", "cost": 150},
    {"id": 2, "title": "Diseño de arquitectura", "cost": 300}
]


def render_index(error=None, status=200):
    total_budget = sum(t["cost"] for t in tasks) if tasks else 0
    return render_template('index.html', tasks=tasks,
                           total_budget=total_budget, error=error), status


@app.route('/')
def index():
    return render_index()


@app.route('/task/add', methods=['POST'])
def add_task():
    title = (request.form.get('title') or '').strip()
    cost_raw = (request.form.get('cost') or '').strip()

    # RFC-003: validar el titulo
    if not title:
        return render_index("El nombre de la tarea no puede estar vacío.", 400)

    # RFC-003: validar que el costo sea numerico y no negativo
    # RFC-002: convertir el costo a numero antes de almacenarlo
    try:
        cost = float(cost_raw)
    except ValueError:
        return render_index("El costo debe ser un número válido (ejemplo: 100 o 99.50).", 400)

    if cost < 0:
        return render_index("El costo no puede ser negativo.", 400)

    # ID unico: evita repetidos despues de eliminar tareas
    new_id = max((t["id"] for t in tasks), default=0) + 1
    tasks.append({
        "id": new_id,
        "title": title,
        "cost": cost
    })
    return redirect(url_for('index'))


@app.route('/task/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)