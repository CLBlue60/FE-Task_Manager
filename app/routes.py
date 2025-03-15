from flask import (
    Flask,
    request as flask_request,
    render_template,
    jsonify
)

app = Flask(__name__, static_folder='static')
import requests

app = Flask(__name__)
BACKEND_URL = "http://127.0.0.1:5000/tasks"

@app.get('/')
def index():
    return render_template('index.html')

@app.get("/about")
def about():
    return render_template('about.html')

@app.get("/tasks")
def get_tasks():
    response = requests.get(BACKEND_URL)
    if response.status_code == 200:
        task_list = response.json().get("tasks")
        return render_template('lists.html', tasks=task_list)
    return (
        render_template(
            'error.html',
            error=response.status_code
        ),
        response.status_code,
    )

@app.get("/tasks/<int:pk>")
def get_single_task(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    if response.status_code == 200:
        single_task = response.json().get("task")
        return render_template('detail.html', task=single_task)
    return (
        render_template(
            'error.html',
            error=response.status_code,
            error_message=response.text
        ),
        response.status_code
    )

# Update
@app.get("/tasks/<int:pk>/edit")
def get_edit_form(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    if response.status_code == 200:
        single_task = response.json().get("task")
        return render_template('edit.html', task=single_task)
    return (
        render_template(
            'error.html',
            error=response.status_code
        ),
        response.status_code
    )

@app.post("/tasks/<int:pk>/edit")
def edit_task(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    task_data = flask_request.form
    response = requests.put(url, json=task_data)
    if response.status_code == 204:
        return render_template("success.html", success_message="Task edited successfully")
    return (
        render_template(
            'error.html',
            error=response.status_code,
            error_message=response.text
        ),
        response.status_code
    )

# Create task
@app.get("/tasks/new")
def get_create_form():
    return render_template('create.html')

def create_task(data):
    response = requests.post(BACKEND_URL, json=data)
    if response.status_code != 201:
        raise Exception(response.text)

@app.post("/tasks")
def create_task_api():
    data = flask_request.json
    if not data:
        return jsonify({"error": "No data provided", "ok": False}), 400

    try:
        create_task(data)
        return jsonify({"message": "Task created", "ok": True}), 201
    except Exception as e:
        return jsonify({"error": str(e), "ok": False}), 500

# Delete Task
@app.get("/tasks/<int:pk>/delete")
def get_delete_form(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.get(url)
    if response.status_code == 200:
        single_task = response.json().get("task")
        return render_template('delete.html', task=single_task)
    return (
        render_template(
            'error.html',
            error=response.status_code,
            error_message=response.text
        ),
        response.status_code
    )

@app.post("/tasks/<int:pk>/delete")
def delete_task(pk):
    url = "%s/%s" % (BACKEND_URL, pk)
    response = requests.delete(url)
    if response.status_code == 204:
        return render_template("success.html", success_message="Task deleted successfully")
    return (
        render_template(
            'error.html',
            error=response.status_code,
            error_message=response.text
        ),
        response.status_code
    )

@app.get("/api/tasks")
def api_get_tasks():
    response = requests.get(BACKEND_URL)
    if response.status_code == 200:
        return response.json()
    return {"error": response.status_code}, response.status_code

if __name__ == "__main__":
    app.run(debug=True)
