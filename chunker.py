def metni_parcala(sayfalar, chunk_boyutu=800, ortusme=100):
    """
    sayfalar: [(sayfa_no, metin), ...] formatında liste (pdf_okuyucu'dan geliyor)
    chunk_boyutu: her parçanın maksimum karakter sayısı
    ortusme: ardışık parçalar arasında kaç karakter ortak olacak

    Geriye [{"metin": ..., "sayfa": ...}, ...] formatında liste döner
    """
    parcalar = []

    for sayfa_no, metin in sayfalar:
        baslangic = 0
        while baslangic < len(metin):
            bitis = baslangic + chunk_boyutu
            parca_metni = metin[baslangic:bitis]

            # Sadece boş olmayan parçaları ekle
            if parca_metni.strip():
                parcalar.append({
                    "metin": parca_metni,
                    "sayfa": sayfa_no
                })

            # Bir sonraki parça, örtüşme kadar geriden başlar
            baslangic += chunk_boyutu - ortusme

    return parcalar


# --- Test kısmı ---
if __name__ == "__main__":
    from pdf_okuyucu import pdf_metin_cikar

    sayfalar = pdf_metin_cikar("ornek.pdf")
    parcalar = metni_parcala(sayfalar)

    print(f"Toplam {len(parcalar)} parça oluşturuldu.\n")
    for i, p in enumerate(parcalar[:3]):  # ilk 3 parçayı göster
        print(f"--- Parça {i+1} (Sayfa {p['sayfa']}) ---")
        print(p["metin"][:150])
        print()