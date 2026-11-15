
FROM python:3.12-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Create directories for persistent data
RUN mkdir -p /app/data/chroma_db /app/data/uploads

# Streamlit port
EXPOSE 8501

# Start the application
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
