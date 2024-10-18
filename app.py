import json
import os.path
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

def read_tasks():
    '''Функция чтения задач из файла'''
    if not os.path.exists('tasks.json'):
        return []
    with open('tasks.json', 'r') as f:
        return json.load(f)

def write_tasks(tasks):
    '''Функция для записи задач в файл'''
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f, indent = 2)

# Главная страница
@app.route('/')
def index():
    return render_template('index.html')

# Получаем все задачи
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = read_tasks()
    return jsonify(tasks)

# Добавляем новую задачу
@app.route('/tasks', methods=['POST'])
def add_task():
    task = request.json
    tasks = read_tasks()
    tasks.append({'id': len(tasks) + 1, 'title': task['title'], 'completed': False})
    write_tasks(tasks)
    return jsonify(tasks[-1]), 201

# Удаляем задачи
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    tasks = read_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    write_tasks(tasks)
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)