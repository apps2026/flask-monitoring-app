FROM python:3.11-slim

WORKDIR /app

# Copy the app folder into /app
COPY ./app /app/app
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

# Run the Flask app as a module so 'app' package works
CMD ["python", "-m", "app.main"]
