from flask import Flask, request
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
import time
import psutil
import os

app = Flask(__name__)

# Metrics
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests", ['method', 'endpoint'])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "Request latency", ['endpoint'])
MEMORY_USAGE = Gauge("process_memory_mb", "Memory usage in MB")

def track_metrics(endpoint):
    def wrapper(func):
        def wrapped(*args, **kwargs):
            start_time = time.time()
            REQUEST_COUNT.labels(method=request.method, endpoint=endpoint).inc()
            result = func(*args, **kwargs)
            latency = time.time() - start_time
            REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)
            process = psutil.Process(os.getpid())
            MEMORY_USAGE.set(process.memory_info().rss / 1024 / 1024)  # MB
            return result
        wrapped.__name__ = func.__name__  # Needed for Flask to not break
        return wrapped
    return wrapper

@app.route('/')
@track_metrics('/')
def home():
    return "Hello from Flask + Docker + Render!"

@app.route('/v1')
@track_metrics('/v1')
def v1():
    return "Hello from Flask + Docker + Render! v1"

@app.route('/v2')
@track_metrics('/v2')
def v2():
    return "Hello from Flask + Docker + Render! v2"

@app.route('/v3')
@track_metrics('/v3')
def v3():
    return "Hello from Flask + Docker + Render! v3"

@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}
