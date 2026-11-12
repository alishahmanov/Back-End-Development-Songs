FROM python:3.12-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN pip install --no-cache-dir 'Flask>=3.1,<4' 'pymongo>=4.6,<5' 'gunicorn>=23,<24'
COPY app.py .
COPY backend ./backend
EXPOSE 8080
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
