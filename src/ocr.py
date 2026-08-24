import pytesseract
from pdf2image import convert_from_path

# Windows'ta Tesseract'ın kurulu olduğu yol
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Poppler'ın bin klasörünün yolu
POPPLER_YOLU = r"C:\poppler\poppler-26.02.0\Library\bin"


def pdf_ocr_ile_oku(pdf_yolu):
    """
    Taranmış (metin katmanı olmayan) bir PDF'i OCR ile okur.
    Geriye pdf_okuyucu.py'daki pdf_metin_cikar ile AYNI formatta liste döner:
    [(sayfa_no, metin), (sayfa_no, metin), ...]
    """
    sayfa_resimleri = convert_from_path(pdf_yolu, poppler_path=POPPLER_YOLU)

    sonuclar = []
    for i, resim in enumerate(sayfa_resimleri):
        metin = pytesseract.image_to_string(resim, lang="tur")
        sonuclar.append((i + 1, metin))

    return sonuclar


if __name__ == "__main__":
    sonuc = pdf_ocr_ile_oku("ornek.pdf")
    for sayfa_no, metin in sonuc:
        print(f"--- Sayfa {sayfa_no} ---")
        print(metin[:200])
        print()
        