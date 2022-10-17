FROM python:3.8.15-alpine3.15

COPY . .
# non-root user + venv
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "app.py"]

EXPOSE 5000:5000
