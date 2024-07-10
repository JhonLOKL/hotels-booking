# Usa una imagen base oficial de Python
FROM python:3.9-slim

# Instala dependencias necesarias
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    gnupg \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instala Google Chrome
RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instala ChromeDriver
RUN CHROME_DRIVER_VERSION=$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -N http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/chromedriver && \
    rm chromedriver_linux64.zip

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos necesarios
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Establece variables de entorno para Chrome
ENV DISPLAY=:99

# Ejecuta la aplicación
CMD ["python", "app.py"]
