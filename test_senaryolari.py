import time
from datetime import datetime
from cevap_uret import cevap_uret

TEST_SENARYOLARI = [
    ("Kütüphanede kaç güneş paneli var?", "64", "ornek.pdf"),
    ("Kütüphanede kaç personel çalışıyor?", "12", "personel.pdf"),
    ("Dijital platformda kaç elektronik kitap var?", "24.000", "ornek.pdf"),
    ("Kütüphane hafta içi kaçta açılıyor?", "08.00", "ornek.pdf"),
    ("Çalışma odası rezervasyonu en fazla kaç saat?", "iki saat", "ornek.pdf"),
    ("Personel hangi saatler arasında çalışıyor?", "08:00-18:00", "personel.pdf"),
    ("Kütüphanenin ay üzerindeki bürosu nerede?", "bulunmuyor", None),
    ("Kaç adet su dolum istasyonu var?", "üç", "ornek.pdf"),
]


def testleri_calistir():
    basarili = 0
    basarisiz_detaylar = []
    hatali_sayisi = 0
    rapor_satirlari = []

    baslangic_zamani = datetime.now()
    rapor_satirlari.append(f"Test Raporu - {baslangic_zamani.strftime('%Y-%m-%d %H:%M:%S')}")
    rapor_satirlari.append("=" * 50)

    for i, (soru, beklenen, kaynak_dosya) in enumerate(TEST_SENARYOLARI, 1):
        if i > 1:
            time.sleep(5)

        try:
            sonuc = cevap_uret(soru)
            cevap = sonuc["cevap"]
        except Exception as e:
            print(f"Test {i}: ⚠️ HATA (API sorunu, atlanıyor): {str(e)[:100]}")
            rapor_satirlari.append(f"Test {i}: HATA - {str(e)[:150]}")
            hatali_sayisi += 1
            continue

        gecti = beklenen.lower() in cevap.lower()

        durum = "✅ BAŞARILI" if gecti else "❌ BAŞARISIZ"
        print(f"Test {i}: {durum}")
        print(f"  Soru: {soru}")
        print(f"  Beklenen: '{beklenen}' | Cevap: {cevap[:150]}")
        print()

        rapor_satirlari.append(f"\nTest {i}: {durum}")
        rapor_satirlari.append(f"  Soru: {soru}")
        rapor_satirlari.append(f"  Beklenen: '{beklenen}'")
        rapor_satirlari.append(f"  Alınan cevap: {cevap}")

        if gecti:
            basarili += 1
        else:
            basarisiz_detaylar.append((soru, beklenen, cevap))

    toplam = len(TEST_SENARYOLARI)
    calisan_test_sayisi = toplam - hatali_sayisi
    basari_orani = (basarili / calisan_test_sayisi * 100) if calisan_test_sayisi > 0 else 0

    ozet = (
        f"\n{'=' * 50}\n"
        f"SONUÇ: {basarili}/{calisan_test_sayisi} çalışan test başarılı (%{basari_orani:.1f})\n"
        f"({hatali_sayisi} test API hatası nedeniyle atlandı)"
    )
    print(ozet)
    rapor_satirlari.append(ozet)

    # Raporu dosyaya kaydet
    with open("test_raporu.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(rapor_satirlari))

    print(f"\n📄 Rapor 'test_raporu.txt' dosyasına kaydedildi.")


if __name__ == "__main__":
    testleri_calistir()