## Notification Project
Система доставки уведомлений.

### Установка

1. Клонировать репозиторий:
```bash
git clone https://github.com/MariaBusorgina/test_task.git
cd test_task
```

2. Создать и активировать виртуальное окружение
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Установить зависимости
```bash
pip install -r requirements.txt
```

4. Создать базу данных и суперпользователя
```bash
CREATE DATABASE notification_db;   
CREATE USER myuser WITH PASSWORD 'mypassword';   
GRANT ALL PRIVILEGES ON DATABASE notification_db TO myuser1;
```

5. Создать .env с PostgreSQL настройками:
```bash
PG_USER=myuser  
PG_PASSWORD=mypassword  
PG_DATABASE=notification_db  
PG_HOST=localhost  
PG_PORT=5432  
```

6. Применить миграции
```bash
python manage.py migrate
```

7. Запуск сервера
```bash
python manage.py runserver
```

8. Создать суперпользователя
```bash
python manage.py createsuperuser
```

9. Административная панель - http://127.0.0.1:8000/admin, создать:  
- пользователей  
- профили пользователей  
- каналы с приоритетом  отправки (например, telegram=1, email=2, sms=3)

11. Запуск редис 
```bash
redis-server
```

12. Запуск Celery  
```bash
celery -A core worker -l info
```

13. Отправка уведомления через API  
POST http://127.0.0.1:8000/api/v1/notifications/send/  
Content-Type: application/json  
```bash
{  
    "user_id": 1,  
    "message": "Hello"  
}  
```
user_id – ID пользователя (целое число, обязательный)  
message – текст уведомления (строка, обязательный)
