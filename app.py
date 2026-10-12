from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Base de datos en memoria para pruebas de clase
tasks = [
    {"id": 1, "title": "Levantamiento de requerimientos", "cost": 150},
    {"id": 2, "title": "Diseño de arquitectura", "cost": 300}
]
@app.route('/')
def index():
    total_budget = sum(t["cost"] for t in tasks)
    return render_template(
        'index.html',
        tasks=tasks,
        total_budget=total_budget
    )

@app.route('/task/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    cost_raw = request.form.get('cost')

    try:
        cost = int(cost_raw)
    except (ValueError, TypeError):
        return "Error: el costo debe ser un número entero válido.", 400

    new_id = max([t["id"] for t in tasks], default=0) + 1

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
