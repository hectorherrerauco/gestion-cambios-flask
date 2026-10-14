from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

tasks = [
    {"id": 1, "title": "Levantamiento de requerimientos", "cost": 150},
    {"id": 2, "title": "Diseño de arquitectura", "cost": 300}
]


@app.route('/')
def index():
    total_budget = sum(float(task["cost"]) for task in tasks)

    return render_template(
        'index.html',
        tasks=tasks,
        total_budget=total_budget,
        error=None,
        title_value='',
        cost_value=''
    )


@app.route('/task/add', methods=['POST'])
def add_task():
    title = request.form.get('title', '').strip()
    cost_raw = request.form.get('cost', '').strip()
    error = None

    if not title:
        error = "El nombre de la tarea es obligatorio."
    elif not cost_raw:
        error = "El costo es obligatorio."
    else:
        try:
            cost = float(cost_raw)

            if cost < 0:
                error = "El costo no puede ser negativo."
            elif not cost_raw.replace('.', '', 1).isdigit():
                error = "El costo debe contener únicamente números."
        except ValueError:
            error = "El costo debe contener únicamente números."

    if error:
        total_budget = sum(float(task["cost"]) for task in tasks)

        return render_template(
            'index.html',
            tasks=tasks,
            total_budget=total_budget,
            error=error,
            title_value=title,
            cost_value=cost_raw
        )

    new_id = max((task["id"] for task in tasks), default=0) + 1

    tasks.append({
        "id": new_id,
        "title": title,
        "cost": cost
    })

    return redirect(url_for('index'))


@app.route('/task/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)