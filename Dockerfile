# Python 3.9
FROM python:3.9-slim

# Çalışma dizinini ayarla
WORKDIR /app

# Gerekli sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Requirements dosyasını kopyala ve bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tüm dosyaları kopyala
COPY . .

# Port'u açıkça belirt
EXPOSE 5000

CMD ["python", "app.py"]
