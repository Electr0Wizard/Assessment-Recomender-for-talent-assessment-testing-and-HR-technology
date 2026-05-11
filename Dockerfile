# Use a lightweight, stable Python version
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy your requirements first (this makes builds faster)
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your code into the container
COPY . .

# Hugging Face Spaces REQUIRES the app to run on port 7860
EXPOSE 7860

# The command to start your FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]