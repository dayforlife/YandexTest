# Используем Python 3.10
FROM python:3.10

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY . .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Указываем переменные окружения для Django
ENV PYTHONUNBUFFERED=1

# Запускаем сервер
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]