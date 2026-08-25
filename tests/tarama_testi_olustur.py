from PIL import Image, ImageDraw, ImageFont
import pymupdf as fitz
import os

genislik, yukseklik = 1000, 1400
resim = Image.new("RGB", (genislik, yukseklik), color="white")
cizim = ImageDraw.Draw(resim)

metin = """Mavisehir Kutuphanesi - Taranmis Test Belgesi

Bu belge, OCR ozelligini test etmek icin
olusturulmus sahte bir taranmis dokumandir.

Kutuphanede toplam 8 adet toplanti odasi
bulunmaktadir. Bu odalar onceden rezervasyon
yapilarak kullanilabilir.

Kutuphane bunyesinde ayrica 3 adet 3D yazici
bulunmaktadir ve ogrenciler bu yazicilari
ucretsiz olarak kullanabilir."""

try:
    font = ImageFont.truetype("arial.ttf", 32)
except:
    font = ImageFont.load_default()

cizim.multiline_text((50, 50), metin, fill="black", font=font, spacing=15)

data_klasoru = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
os.makedirs(data_klasoru, exist_ok=True)

resim_yolu = os.path.join(data_klasoru, "gecici_sayfa.png")
resim.save(resim_yolu)

dokuman = fitz.open()
sayfa = dokuman.new_page(width=genislik, height=yukseklik)
sayfa.insert_image(sayfa.rect, filename=resim_yolu)

pdf_yolu = os.path.join(data_klasoru, "taranmis_test.pdf")
dokuman.save(pdf_yolu)
dokuman.close()

print(f"taranmis_test.pdf oluşturuldu: {pdf_yolu}")