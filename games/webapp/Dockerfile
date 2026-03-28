FROM python:3.11-slim
WORKDIR /app
COPY ../puzzles.py ./
COPY templates ./templates
COPY static ./static
COPY app.py ./app.py
RUN pip install --no-cache-dir Flask
EXPOSE 5000
CMD ["python", "app.py", "5000"]
