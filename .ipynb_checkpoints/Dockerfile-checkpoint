# Use the official Python image from Docker Hub
FROM python:3.8-slim

# Set environment variables for Chrome installation
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROME_DRIVER_VERSION=114.0.5735.90

# Set the working directory in the container
WORKDIR /main.py

# Install system dependencies, including Chrome and ChromeDriver
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    wget \
    unzip \
    curl \
    gnupg \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && CHROME_DRIVER_URL=https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip \
    && wget -O /tmp/chromedriver.zip ${CHROME_DRIVER_URL} \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver \
    && rm /tmp/chromedriver.zip \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the rest of your application code to the container
COPY . .

# Expose the port Streamlit will run on
EXPOSE 8501

# Command to run the application
CMD ["streamlit", "run", "your_script.py", "--server.port=8501", "--server.address=0.0.0.0"]
