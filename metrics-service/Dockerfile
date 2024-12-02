FROM python:3.9-slim
WORKDIR /app
COPY app.py /app
RUN pip install flask flask_cors boto3
EXPOSE 5002
CMD ["python", "app.py"]