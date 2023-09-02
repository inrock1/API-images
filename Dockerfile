FROM python:3.11-slim
LABEL maintainer="kaskov.e@gmail.com"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY . /app

RUN pip3 install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80
CMD ["uvicorn", "src.main:app", "--reload", "--host", "0.0.0.0", "--port", "80"]
