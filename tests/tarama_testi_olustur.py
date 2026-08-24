from PIL import Image, ImageDraw, ImageFont
import pymupdf as fitz

# 1. Adım: içine yazı yazılmış bir resim oluştur (gerçek bir kağıt taraması gibi)
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

# Basit bir yazı tipi kullanıyoruz (Windows'ta genelde bulunur)
try:
    font = ImageFont.truetype("arial.ttf", 32)
except:
    font = ImageFont.load_default()

cizim.multiline_text((50, 50), metin, fill="black", font=font, spacing=15)

resim.save("gecici_sayfa.png")

# 2. Adım: bu resmi, METİN KATMANI OLMADAN bir PDF sayfasına göm
dokuman = fitz.open()
sayfa = dokuman.new_page(width=genislik, height=yukseklik)
sayfa.insert_image(sayfa.rect, filename="gecici_sayfa.png")
dokuman.save("taranmis_test.pdf")
dokuman.close()

print("taranmis_test.pdf oluşturuldu (metin katmanı yok, sadece resim).")