# Usa una imagen base de Python
FROM python:3.11-slim

# Instala las dependencias necesarias
RUN apt-get update && \
    apt-get install -y wget gnupg && \
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    apt-get clean

# Crea y activa un entorno virtual
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copia los archivos de requerimientos y los instala
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia el resto de la aplicación
COPY . .

# Establece el comando de inicio
CMD ["python", "app.py"]
