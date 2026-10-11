from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Base de datos en memoria para pruebas de clase
tasks = [
    {"id": 1, "title": "Levantamiento de requerimientos", "cost": 150},
    {"id": 2, "title": "Diseño de arquitectura", "cost": 300}
]

def parse_cost(raw):
    """Convierte el costo recibido del formulario (texto) a un valor numérico."""
    value = float(raw)
    return int(value) if value.is_integer() else value

@app.route('/')
def index():
    total_budget = round(sum(t["cost"] for t in tasks), 2)
    return render_template('index.html', tasks=tasks, total_budget=total_budget)

@app.route('/task/add', methods=['POST'])
def add_task():
    title = request.form.get('title')
    cost_raw = request.form.get('cost')

    # BUG 2: Permite títulos vacíos y almacena cost como string sin convertir a entero
    new_id = len(tasks) + 1
    tasks.append({
        "id": new_id,
        "title": title,
        "cost": parse_cost(cost_raw)
    })
    return redirect(url_for('index'))

@app.route('/task/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
