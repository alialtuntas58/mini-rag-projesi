import logging
import os

os.makedirs("loglar", exist_ok=True)

logging.basicConfig(
    filename="loglar/uygulama.log",
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
        