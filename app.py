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
    cost_input = request.form.get('cost', '').strip()

    # Validar que el título no esté vacío
    if not title:
        return "Error: el título es obligatorio", 400

    # Validar que el costo sea numérico y no negativo
    try:
        cost = float(cost_input)
    except (ValueError, TypeError):
        return "Error: el costo debe ser numérico", 400

    if cost < 0:
        return "Error: el costo no puede ser negativo", 400

    # Agregar la tarea únicamente si los datos son válidos
    task = {
        'id': len(tasks) + 1,
        'title': title,
        'cost': cost
    }

    tasks.append(task)

    return redirect('/')

@app.route('/task/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
