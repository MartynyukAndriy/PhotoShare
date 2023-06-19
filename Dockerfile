FROM python:3.10-slim-buster
RUN apt update
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]