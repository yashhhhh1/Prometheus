FROM python:3.9-slim

WORKDIR /app

COPY . /app
RUN pip install -r ./requirements.txt

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]
