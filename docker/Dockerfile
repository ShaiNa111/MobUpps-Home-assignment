FROM python:3.13

WORKDIR /app

# Copy requirements first for better caching
COPY docker/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the source code needed for the app
COPY . .

EXPOSE 8080

CMD ["uvicorn", "src.api.endpoints:app", "--host", "0.0.0.0", "--port", "8080"]
