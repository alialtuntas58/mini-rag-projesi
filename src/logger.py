import logging
import os

_PROJE_KOKU = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_LOG_KLASORU = os.path.join(_PROJE_KOKU, "loglar")
os.makedirs(_LOG_KLASORU, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(_LOG_KLASORU, "uygulama.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

logger = logging.getLogger("mini_rag")


def soru_cevap_logla(soru, cevap, kaynaklar, hata=None):
    if hata:
        logger.error(f"SORU: {soru} | HATA: {hata}")
    else:
        kaynak_metni = ", ".join(f"{d}-s{s}" for d, s in kaynaklar) if kaynaklar else "yok"
        logger.info(f"SORU: {soru} | KAYNAKLAR: {kaynak_metni} | CEVAP_UZUNLUK: {len(cevap)} karakter")