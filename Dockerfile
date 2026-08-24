# Temel Python imajını alıyoruz
FROM python:3.11-slim

# Çalışma dizinini belirliyoruz
WORKDIR /app

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