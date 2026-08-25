import pymupdf as fitz
import os

dokuman = fitz.open()
sayfa = dokuman.new_page()

metin = """Mavisehir Kutuphanesi - Personel Bilgileri

1. Calisan Sayisi
Kutuphanede toplam 12 tam zamanli personel calismaktadir.
Bunlardan 4'u kutuphaneci, 3'u teknik destek, 5'i guvenlik ve temizlik
personelidir.

2. Calisma Saatleri
Personel hafta ici 08:00-18:00 arasinda vardiyali olarak calismaktadir.
Hafta sonlari sadece 2 kutuphaneci gorev almaktadir.
"""

sayfa.insert_text((50, 50), metin, fontsize=11)

cikti_yolu = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "personel.pdf")
dokuman.save(cikti_yolu)
dokuman.close()
print(f"personel.pdf oluşturuldu: {cikti_yolu}")