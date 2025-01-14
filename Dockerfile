# Используем базовый образ с Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Указываем порт, который будет слушать Flask
EXPOSE 5000

# Команда для запуска приложения
CMD ["python", "app.py"]
