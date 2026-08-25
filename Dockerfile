# Temel Python imajını alıyoruz
FROM python:3.11-slim

# Çalışma dizinini belirliyoruz
WORKDIR /app

# Sistem seviyesinde gerekli programları kuruyoruz: Tesseract (OCR) ve Poppler (PDF->resim)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-tur \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Kütüphane listesini kopyalayıp kuruyoruz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Tüm kodlarımızı ve klasörlerimizi (src, data, tests) kopyalıyoruz
COPY . .

# Python'un src klasöründeki kodları bulabilmesi için yol gösteriyoruz
ENV PYTHONPATH=/app/src

# FastAPI'nin çalışacağı portu dışa açıyoruz
EXPOSE 8000

# Sunucuyu artık 'src' klasörünün içindeki api.py'den başlatıyoruz
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]