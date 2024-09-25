from celery_app import app

@app.task
def multiply(x, y):
    return x * y
