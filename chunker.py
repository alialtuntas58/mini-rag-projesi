import re

def cumlelere_ayir(metin):
    """
    Metni cümlelere ayırır. Türkçe'de nokta, ünlem, soru işareti sonrası
    boşluk varsa cümle sonu kabul ediyoruz (basit ama etkili bir kural).
    """
    cumleler = re.split(r'(?<=[.!?])\s+', metin)
    return [c.strip() for c in cumleler if c.strip()]


def metni_parcala(sayfalar, chunk_boyutu=800, ortusme=100):
    """
    sayfalar: [(sayfa_no, metin), ...] formatında liste
    Metni önce cümlelere ayırır, sonra cümleleri chunk_boyutu'nu aşmayacak
    şekilde birleştirerek parçalar oluşturur - cümle ortasından KESMEZ.
    """
    parcalar = []

    for sayfa_no, metin in sayfalar:
        cumleler = cumlelere_ayir(metin)
        mevcut_parca = ""

        for cumle in cumleler:
            # Bu cümleyi eklersek chunk_boyutu'nu aşar mıyız?
            if len(mevcut_parca) + len(cumle) > chunk_boyutu and mevcut_parca:
                # Aşıyorsa, mevcut parçayı kaydet ve yeni parçaya başla
                parcalar.append({"metin": mevcut_parca.strip(), "sayfa": sayfa_no})

                # Overlap: yeni parçayı, öncekinin son kısmıyla başlat
                mevcut_parca = mevcut_parca[-ortusme:] + " " + cumle
            else:
                mevcut_parca += " " + cumle

        # Son kalan parçayı da ekle (döngü bitince elde kalan metin)
        if mevcut_parca.strip():
            parcalar.append({"metin": mevcut_parca.strip(), "sayfa": sayfa_no})

    return parcalar


# --- Test kısmı ---
if __name__ == "__main__":
    from pdf_okuyucu import pdf_metin_cikar

    sayfalar = pdf_metin_cikar("ornek.pdf")
    parcalar = metni_parcala(sayfalar)

    print(f"Toplam {len(parcalar)} parça oluşturuldu.\n")
    for i, p in enumerate(parcalar):
        print(f"--- Parça {i+1} (Sayfa {p['sayfa']}) ---")
        print(p["metin"][:200])
        print()