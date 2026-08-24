import sys
import os as _os
sys.path.append(_os.path.dirname(_os.path.abspath(__file__)))

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import shutil

# Senin yazdığın modüller
from pdf_okuyucu import pdf_metin_cikar
from chunker import metni_parcala
from vektor_deposu import parcalari_kaydet, koleksiyon
from cevap_uret import cevap_uret  # <-- BEYNİ BURAYA BAĞLADIK!

app = FastAPI(title="Gelişmiş Akıllı Doküman Asistanı API")

# --- Geçici dosyalar için klasör ---
TEMP_DIR = "temp_uploads"
os.makedirs(TEMP_DIR, exist_ok=True)


class SoruIstegi(BaseModel):
    soru: str
    secili_dosya: Optional[str] = None  # Eğer sadece 1 dosyada arama yapılacaksa kullanılabilir


@app.get("/health")
async def health_check():
    try:
        kayit_sayisi = koleksiyon.count()
        return {"durum": "aktif", "mesaj": "Sistem ayakta!", "veritabani_kayit_sayisi": kayit_sayisi}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Sistem sağlıksız: {str(e)}")


@app.post("/ingest")
async def belge_yukle(file: UploadFile = File(...)):
    """PDF dosyasını alır, metni çıkarır, parçalar ve ChromaDB'ye kaydeder."""
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Sadece PDF dosyaları yüklenebilir.")

    dosya_yolu = os.path.join(TEMP_DIR, file.filename)
    try:
        with open(dosya_yolu, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dosya kaydedilirken hata oluştu: {str(e)}")

    try:
        print(f"[{file.filename}] işleniyor...")
        sayfalar = pdf_metin_cikar(dosya_yolu)

        if not sayfalar:
            raise HTTPException(status_code=400, detail="PDF'ten metin çıkarılamadı veya boş.")

        parcalar = metni_parcala(sayfalar)
        parcalari_kaydet(parcalar, dosya_adi=file.filename)
        os.remove(dosya_yolu)

        return {
            "mesaj": "Dosya başarıyla indekslendi.",
            "dosya_adi": file.filename,
            "islenen_sayfa_sayisi": len(sayfalar),
            "olusturulan_parca_sayisi": len(parcalar)
        }

    except Exception as e:
        if os.path.exists(dosya_yolu):
            os.remove(dosya_yolu)
        raise HTTPException(status_code=500, detail=f"İşleme sırasında hata oluştu: {str(e)}")


@app.post("/ask")
async def soru_sor(istek: SoruIstegi):
    """Soru alır, ChromaDB'de arar ve Gemini LLM ile kaynak göstererek cevaplar."""
    if not istek.soru.strip():
        raise HTTPException(status_code=400, detail="Soru boş olamaz.")

    try:
        print(f"Soru alındı: {istek.soru}")
        sonuc = cevap_uret(soru=istek.soru, secili_dosya=istek.secili_dosya)

        return {
            "soru": istek.soru,
            "cevap": sonuc["cevap"],
            "kaynaklar": sonuc["kaynaklar"],
            "guven_seviyesi": sonuc["guven"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cevap üretilirken hata oluştu: {str(e)}")


@app.get("/dokumanlar")
async def dokumanlari_listele():
    """Veritabanında kayıtlı tüm dokümanların listesini döner."""
    tum_kayitlar = koleksiyon.get()
    if not tum_kayitlar["metadatas"]:
        return {"dokumanlar": []}

    dosyalar = sorted(set(m["dosya"] for m in tum_kayitlar["metadatas"]))
    return {"dokumanlar": dosyalar}