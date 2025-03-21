# FlaskTaskAPI

Простое REST API для управления задачами, построенное на Flask. Позволяет добавлять, просматривать и удалять задачи с указанием названия, описания и дедлайна. Данные хранятся в памяти (без базы данных).

## Возможности
- **POST /tasks**: Добавление новой задачи с полями `title`, `description` и `deadline` (формат "DD-MM-YYYY").
- **GET /tasks**: Получение списка всех задач, отсортированных по дедлайну (ближайшие сверху).
- **DELETE /tasks/<id>**: Удаление задачи по её ID.

## Требования
- Python 3.x
- Flask (`pip install flask`)

## Запустите приложение:
python app.py

API будет доступно по адресу http://localhost:5000

Добавление задачи: 
`curl -X POST -H "Content-Type: application/json" -d "{\"title\":\"Купить молоко\",\"description\":\"Сходить в магазин\",\"deadline\":\"20-03-2025\"}" http://localhost:5000/tasks`

Получение списка задач:
`curl http://localhost:5000/tasks`

Удаление задачи:
`curl -X DELETE http://localhost:5000/tasks/1`
