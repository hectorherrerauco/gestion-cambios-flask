from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Base de datos en memoria para pruebas de clase
tasks = [
    {"id": 1, "title": "Levantamiento de requerimientos", "cost": 150},
    {"id": 2, "title": "Diseño de arquitectura", "cost": 300}
]


@app.route('/')
def index():
    # Calcular el presupuesto total
    total_budget = sum(t["cost"] for t in tasks) if tasks else 0

    return render_template(
        'index.html',
        tasks=tasks,
        total_budget=total_budget
    )


@app.route('/task/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    cost_raw = request.form.get('cost')

    # Validar que el título no esté vacío
    if not title or not title.strip():
        return redirect(url_for('index'))

    # Convertir el costo a número
    try:
        cost = int(cost_raw) if cost_raw else 0
    except ValueError:
        cost = 0

    new_id = len(tasks) + 1

    tasks.append({
        "id": new_id,
        "title": title.strip(),
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
