import json
import os
from datetime import datetime

FEEDBACK_DOSYASI = "feedback_kayitlari.json"


def feedback_kaydet(soru, cevap, puan):
    """
    puan: "begeni" veya "begenmedi"
    """
    kayit = {
        "soru": soru,
        "cevap": cevap,
        "puan": puan,
        "zaman": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    kayitlar = feedback_kayitlarini_getir()
    kayitlar.append(kayit)

    with open(FEEDBACK_DOSYASI, "w", encoding="utf-8") as f:
        json.dump(kayitlar, f, ensure_ascii=False, indent=2)


def feedback_kayitlarini_getir():
    if not os.path.exists(FEEDBACK_DOSYASI):
        return []
    with open(FEEDBACK_DOSYASI, "r", encoding="utf-8") as f:
        return json.load(f)


def feedback_ozeti():
    kayitlar = feedback_kayitlarini_getir()
    toplam = len(kayitlar)
    begeni = sum(1 for k in kayitlar if k["puan"] == "begeni")
    begenmedi = sum(1 for k in kayitlar if k["puan"] == "begenmedi")

    return {
        "toplam": toplam,
        "begeni": begeni,
        "begenmedi": begenmedi,
        "begeni_orani": (begeni / toplam * 100) if toplam > 0 else 0
    }