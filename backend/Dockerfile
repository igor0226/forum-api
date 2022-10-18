FROM python:3.8.15-alpine3.15

RUN mkdir backend
COPY . backend
# non-root user + venv
RUN cd backend && pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "backend/app.py"]

EXPOSE 5000:5000
