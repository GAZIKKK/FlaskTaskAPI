from flask import Flask, request, jsonify
from datetime import datetime
import json

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False

tasks = []


def validate_deadline(deadline_str):
    try:
        datetime.strptime(deadline_str, '%d-%m-%Y')
        return True
    except ValueError:
        return False


# Кастомный JSON-сериализатор с форматированием
def json_utf8_dump(data):
    return json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8')


@app.route('/tasks', methods=['POST'])
def add_task():
    if not request.is_json:
        return jsonify({'error': 'Content-Type must be application/json'}), 400

    try:
        data = request.get_json(force=True)
    except Exception as e:
        return jsonify({'error': f'Invalid JSON: {str(e)}'}), 400

    if not all(key in data for key in ['title', 'description', 'deadline']):
        return jsonify({'error': 'Missing required fields'}), 400

    if not validate_deadline(data['deadline']):
        return jsonify({'error': 'Invalid deadline format. Use DD-MM-YYYY'}), 400

    task = {
        'id': len(tasks) + 1,
        'title': data['title'],
        'description': data['description'],
        'deadline': data['deadline']
    }
    tasks.append(task)
    return app.response_class(
        response=json_utf8_dump(task),
        status=201,
        mimetype='application/json'
    )


@app.route('/tasks', methods=['GET'])
def get_tasks():
    sorted_tasks = sorted(tasks, key=lambda x: datetime.strptime(x['deadline'], '%d-%m-%Y'))
    return app.response_class(
        response=json_utf8_dump(sorted_tasks),
        status=200,
        mimetype='application/json'
    )


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    initial_len = len(tasks)
    tasks = [task for task in tasks if task['id'] != task_id]
    if len(tasks) < initial_len:
        return jsonify({'message': f'Task {task_id} deleted'}), 200
    return jsonify({'error': 'Task not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)

"""
Для продакшена я бы сделал следующие улучшения:
1. Заменил бы список в памяти на базу данных (например, SQLite или PostgreSQL) для постоянного хранения данных.
2. Добавил бы аутентификацию пользователей через JWT или OAuth, чтобы разделять задачи между пользователями.
3. Реализовал бы более строгую валидацию входных данных с помощью библиотеки вроде Marshmallow.
4. Добавил бы обработку исключений и логирование для лучшей отладки в продакшене.
5. Настроил бы CORS для безопасного доступа с фронтенда.
6. Развернул бы приложение через WSGI-сервер (например, Gunicorn) с Nginx как прокси.
Эти изменения сделали бы API более надёжным, безопасным и масштабируемым для реального использования.
"""