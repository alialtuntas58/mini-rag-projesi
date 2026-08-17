import time
from cevap_uret import cevap_uret

# Her test: (soru, cevapta gecmesi beklenen anahtar kelime(ler), hangi dosyadan)
TEST_SENARYOLARI = [
    ("Kütüphanede kaç güneş paneli var?", "64", "ornek.pdf"),
    ("Kütüphanede kaç personel çalışıyor?", "12", "personel.pdf"),
    ("Dijital platformda kaç elektronik kitap var?", "24.000", "ornek.pdf"),
    ("Kütüphane hafta içi kaçta açılıyor?", "08.00", "ornek.pdf"),
    ("Çalışma odası rezervasyonu en fazla kaç saat?", "iki saat", "ornek.pdf"),
    ("Personel hangi saatler arasında çalışıyor?", "08:00-18:00", "personel.pdf"),
    ("Kütüphanenin ay üzerindeki bürosu nerede?", "bulunmuyor", None),  # var olmayan bilgi testi
    ("Kaç adet su dolum istasyonu var?", "üç", "ornek.pdf"),
]


def testleri_calistir():
    basarili = 0
    basarisiz_detaylar = []

    for i, (soru, beklenen, kaynak_dosya) in enumerate(TEST_SENARYOLARI, 1):
        sonuc = cevap_uret(soru)
        cevap = sonuc["cevap"]

        # Beklenen kelime cevapta geçiyor mu? (büyük/küçük harf duyarsız)
        gecti = beklenen.lower() in cevap.lower()

        durum = "✅ BAŞARILI" if gecti else "❌ BAŞARISIZ"
        print(f"Test {i}: {durum}")
        print(f"  Soru: {soru}")
        print(f"  Beklenen: '{beklenen}' | Cevap: {cevap[:150]}")
        print()

        if gecti:
            basarili += 1
        else:
            basarisiz_detaylar.append((soru, beklenen, cevap))
        time.sleep(15)    

    toplam = len(TEST_SENARYOLARI)
    basari_orani = (basarili / toplam) * 100

    print("=" * 50)
    print(f"SONUÇ: {basarili}/{toplam} test başarılı (%{basari_orani:.1f})")

    if basarisiz_detaylar:
        print("\nBaşarısız testlerin detayı:")
        for soru, beklenen, cevap in basarisiz_detaylar:
            print(f"- Soru: {soru}")
            print(f"  Beklenen '{beklenen}' bulunamadı. Alınan cevap: {cevap}")


if __name__ == "__main__":
    testleri_calistir()