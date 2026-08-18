import re
from embedder import client


def parcalari_yeniden_sirala(soru, parcalar, en_iyi_kac=4):
    """
    Verilen parça listesini, soruya olan alakasına göre LLM ile yeniden puanlar ve sıralar.
    Geriye en alakalı 'en_iyi_kac' parçayı döner.
    """
    if len(parcalar) <= en_iyi_kac:
        return parcalar  # zaten az sayıda parça varsa, yeniden sıralamaya gerek yok

    parca_listesi_metni = ""
    for i, p in enumerate(parcalar):
        parca_listesi_metni += f"[PARÇA {i}] ({p['dosya']} - Sayfa {p['sayfa']})\n{p['metin'][:300]}\n\n"

    prompt = f"""Aşağıda bir SORU ve bu soruya cevap olabilecek birkaç PARÇA var.
Her parçayı, soruyla ne kadar alakalı olduğuna göre 0-10 arası puanla.
0 = tamamen alakasız, 10 = soruyu doğrudan ve tam cevaplıyor.

SORU: {soru}

PARÇALAR:
{parca_listesi_metni}

Cevabını SADECE şu formatta ver, başka hiçbir şey yazma:
PARÇA 0: <puan>
PARÇA 1: <puan>
(devamı aynı şekilde, her parça için bir satır)"""

    yanit = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    # Yanıttan "PARÇA X: puan" satırlarını ayıklayalım
    puanlar = {}
    for satir in yanit.text.strip().split("\n"):
        eslesme = re.match(r"PARÇA (\d+):\s*(\d+)", satir.strip())
        if eslesme:
            indeks = int(eslesme.group(1))
            puan = int(eslesme.group(2))
            puanlar[indeks] = puan

    # Puanlanan parçaları puana göre büyükten küçüğe sırala
    puanli_parcalar = []
    for i, p in enumerate(parcalar):
        puan = puanlar.get(i, 0)  # LLM bir parçayı atlamışsa, puanı 0 kabul et
        puanli_parcalar.append((puan, p))

    puanli_parcalar.sort(key=lambda x: x[0], reverse=True)

    return [p for puan, p in puanli_parcalar[:en_iyi_kac]]


if __name__ == "__main__":
    from hybrid_arama import hybrid_arama

    soru = "Kütüphanede kaç güneş paneli var?"
    ilk_sonuclar = hybrid_arama(soru, kac_tane=6)

    print("Reranker ÖNCESİ sıralama:")
    for p in ilk_sonuclar:
        print(f"  {p['dosya']} - Sayfa {p['sayfa']}: {p['metin'][:60]}...")

    yeniden_siralanmis = parcalari_yeniden_sirala(soru, ilk_sonuclar, en_iyi_kac=3)

    print("\nReranker SONRASI sıralama:")
    for p in yeniden_siralanmis:
        print(f"  {p['dosya']} - Sayfa {p['sayfa']}: {p['metin'][:60]}...")