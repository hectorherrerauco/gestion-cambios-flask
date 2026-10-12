from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

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
    title = request.form.get('title', '').strip()
    cost_raw = request.form.get('cost', '').strip()

    # Validar que el título no esté vacío
    if not title:
        return redirect(url_for('index'))

    # Validar que el costo no esté vacío
    if not cost_raw:
        return redirect(url_for('index'))

    # Validar que el costo sea numérico
    try:
        cost = float(cost_raw)
    except ValueError:
        return redirect(url_for('index'))

    # Evitar costos negativos o valores no finitos
    import math
    if not math.isfinite(cost) or cost < 0:
        return redirect(url_for('index'))

    # Crear y guardar la tarea con datos válidos
    new_id = max((t['id'] for t in tasks), default=0) + 1

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
