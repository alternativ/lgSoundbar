FROM python:3-alpine
COPY . /app
WORKDIR /app
RUN apk update && apk add python3-dev gcc libc-dev libffi-dev
RUN pip install -r requirements.txt
CMD ["gunicorn", "-w 4", "-b", "0.0.0.0:8000", "main:app"]
