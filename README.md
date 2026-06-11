#Сервис бронирования переговорных комнат

#Запуск через Docker Compose (рекомендуемый способ)

```bash
docker-compose up --build

#Запуск через Docker 
docker build -t booking-service .
docker run -p 8000:8000 booking-service

#Запуск локально
poetry install
poetry run uvicorn app.main:app --reload

API Endpoints

Аутентификация:
    POST /auth/register - регистрация
    POST /auth/login - получение JWT токена
    GET /auth/me - текущий пользователь

Комнаты:
    GET /rooms/{room_id}/availability?date=YYYY-MM-DD - свободные слоты
    POST /rooms/ - создать комнату
    DELETE /rooms/{room_id} - удалить комнату

Бронирования:
    POST /bookings - создать бронь
    GET /bookings - список своих броней
    DELETE /bookings/{booking_id} - отменить бронь

Примеры:
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "password": "pass123"}'

curl -X POST http://localhost:8000/auth/login \
  -d "username=user1&password=pass123"

curl -X POST http://localhost:8000/bookings \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"room_id": 1, "date": "2026-12-31", "start_time": "10:00", "end_time": "11:00"}'