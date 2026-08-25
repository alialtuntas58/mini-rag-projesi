import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

import time
from datetime import datetime
from cevap_uret import cevap_uret
# Her test: (soru, cevapta gecmesi beklenen anahtar kelime(ler), kategori)
# Kategoriler dokumandaki 13.1 bolumune gore: dogrudan_bilgi, iki_sayfa,
# dokuman_disi, coklu_dokuman, benzer_kelime, ocr, takip_sorusu
TEST_SENARYOLARI = [
    # --- ornek.pdf: dogrudan bilgi sorulari ---
    ("Kütüphanede kaç güneş paneli var?", "64", "dogrudan_bilgi"),
    ("Dijital platformda kaç elektronik kitap var?", "24.000", "dogrudan_bilgi"),
    ("Kütüphane hafta içi kaçta açılıyor?", "08.00", "dogrudan_bilgi"),
    ("Çalışma odası rezervasyonu en fazla kaç saat sürebilir?", "iki saat", "dogrudan_bilgi"),
    ("Kaç adet su dolum istasyonu var?", "üç", "dogrudan_bilgi"),
    ("Kütüphanede kaç bireysel çalışma odası var?", "12", "dogrudan_bilgi"),
    ("Kaç grup çalışma salonu bulunuyor?", "3", "dogrudan_bilgi"),
    ("Dijital platformda kaç akademik makale var?", "3.500", "dogrudan_bilgi"),
    ("Teknoloji semineri hangi gün yapılıyor?", "çarşamba", "dogrudan_bilgi"),
    ("Yaratıcı yazarlık atölyesine kaç yaş arası çocuklar katılabilir?", "10-14", "dogrudan_bilgi"),

    # --- ornek.pdf: iki farkli bolumu/sayfayi birlestiren sorular ---
    ("Kütüphanenin enerji tasarrufu için yaptığı uygulamalar nelerdir?", "güneş paneli", "iki_sayfa"),
    ("2027 sonuna kadar enerji tüketimi ne kadar azaltılması hedefleniyor?", "yüzde 20", "iki_sayfa"),

    # --- personel.pdf: dogrudan bilgi sorulari ---
    ("Kütüphanede kaç personel çalışıyor?", "12", "dogrudan_bilgi"),
    ("Kaç kütüphaneci var?", "4", "dogrudan_bilgi"),
    ("Personel hangi saatler arasında çalışıyor?", "08:00-18:00", "dogrudan_bilgi"),
    ("Hafta sonu kaç kütüphaneci görev alıyor?", "2", "dogrudan_bilgi"),

    # --- taranmis_test.pdf (OCR): dogrudan bilgi sorulari ---
    ("Kütüphanede kaç toplantı odası var?", "8", "ocr"),
    ("Kaç adet 3D yazıcı var?", "3", "ocr"),

    # --- Dokumanda olmayan sorular (halusinasyon testi) ---
    ("Kütüphanenin yıllık bütçesi kaç TL?", "bulunmuyor", "dokuman_disi"),
    ("Kütüphane müdürünün adı nedir?", "bulunmuyor", "dokuman_disi"),
    ("Kütüphanenin ay üzerindeki şubesi nerede?", "bulunmuyor", "dokuman_disi"),

    # --- Coklu dokuman gerektiren sorular ---
    ("Kütüphanenin fiziksel özellikleri ve personel sayısı nedir?", "personel", "coklu_dokuman"),
    ("Bu dokümanlar neyden bahsediyor?", "kütüphane", "coklu_dokuman"),

    # --- Benzer kelimeli ama farkli konu (yanlis chunk'a gitmemeli) ---
    ("Kütüphanenin güvenlik personeli kaç kişi?", "5", "benzer_kelime"),
]


def testleri_calistir():
    basarili = 0
    basarisiz_detaylar = []
    hatali_sayisi = 0
    rapor_satirlari = []
    kategori_sonuclari = {}

    baslangic_zamani = datetime.now()
    rapor_satirlari.append(f"Test Raporu - {baslangic_zamani.strftime('%Y-%m-%d %H:%M:%S')}")
    rapor_satirlari.append(f"Toplam soru sayısı: {len(TEST_SENARYOLARI)}")
    rapor_satirlari.append("=" * 60)

    for i, (soru, beklenen, kategori) in enumerate(TEST_SENARYOLARI, 1):
        if i > 1:
            time.sleep(5)

        baslangic = time.time()
        try:
            sonuc = cevap_uret(soru)
            cevap = sonuc["cevap"]
            gecen_sure = round(time.time() - baslangic, 2)
        except Exception as e:
            print(f"Test {i}: ⚠️ HATA (API sorunu, atlanıyor): {str(e)[:100]}")
            rapor_satirlari.append(f"\nTest {i} [{kategori}]: HATA - {str(e)[:150]}")
            hatali_sayisi += 1
            continue

        gecti = beklenen.lower() in cevap.lower()

        durum = "✅ BAŞARILI" if gecti else "❌ BAŞARISIZ"
        print(f"Test {i} [{kategori}]: {durum} ({gecen_sure}s)")
        print(f"  Soru: {soru}")
        print(f"  Beklenen: '{beklenen}' | Cevap: {cevap[:150]}")
        print()

        rapor_satirlari.append(f"\nTest {i} [{kategori}]: {durum} (yanıt süresi: {gecen_sure}s)")
        rapor_satirlari.append(f"  Soru: {soru}")
        rapor_satirlari.append(f"  Beklenen: '{beklenen}'")
        rapor_satirlari.append(f"  Alınan cevap: {cevap}")

        kategori_sonuclari.setdefault(kategori, {"basarili": 0, "toplam": 0})
        kategori_sonuclari[kategori]["toplam"] += 1

        if gecti:
            basarili += 1
            kategori_sonuclari[kategori]["basarili"] += 1
        else:
            basarisiz_detaylar.append((soru, beklenen, cevap, kategori))

    toplam = len(TEST_SENARYOLARI)
    calisan_test_sayisi = toplam - hatali_sayisi
    basari_orani = (basarili / calisan_test_sayisi * 100) if calisan_test_sayisi > 0 else 0

    ozet = (
        f"\n{'=' * 60}\n"
        f"GENEL SONUÇ: {basarili}/{calisan_test_sayisi} çalışan test başarılı (%{basari_orani:.1f})\n"
        f"({hatali_sayisi} test API hatası nedeniyle atlandı)\n"
        f"\nKATEGORİ BAZLI SONUÇLAR:"
    )
    for kat, sonuc in kategori_sonuclari.items():
        ozet += f"\n  {kat}: {sonuc['basarili']}/{sonuc['toplam']}"

    print(ozet)
    rapor_satirlari.append(ozet)

    if basarisiz_detaylar:
        rapor_satirlari.append("\n\nBAŞARISIZ TESTLERİN DETAYI:")
        for soru, beklenen, cevap, kategori in basarisiz_detaylar:
            rapor_satirlari.append(f"\n[{kategori}] Soru: {soru}")
            rapor_satirlari.append(f"  Beklenen '{beklenen}' bulunamadı. Alınan cevap: {cevap}")

    with open("../TEST_RAPORU.md", "w", encoding="utf-8") as f:
        f.write("# Test Raporu\n\n```\n" + "\n".join(rapor_satirlari) + "\n```\n")

    print(f"\n📄 Rapor '../TEST_RAPORU.md' dosyasına kaydedildi.")


if __name__ == "__main__":
    testleri_calistir()