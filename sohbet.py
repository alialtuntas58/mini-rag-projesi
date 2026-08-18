from google.genai import types
from embedder import client
from arama import ilgili_parcalari_bul
from cevap_uret import cevap_uret
import re


class SohbetOturumu:
    def __init__(self):
        self.gecmis = []

    def soruyu_zenginlestir(self, soru):
        if not self.gecmis:
            return soru

        son_gecmis = self.gecmis[-2:]
        gecmis_metni = ""
        for g in son_gecmis:
            gecmis_metni += f"Soru: {g['soru']}\nCevap: {g['cevap']}\n\n"

        prompt = f"""Aşağıda bir konuşma geçmişi ve yeni bir soru var.
Yeni soruyu, geçmişe bakmadan da anlaşılabilecek, bağımsız ve net bir hale getir.
Eğer soru zaten net ve bağımsızsa, olduğu gibi döndür.
ÖNEMLİ: Sorudaki anahtar kelimeleri (tüketim, üretim, maliyet, sayı vb.) DEĞİŞTİRME - sadece belirsiz zamirleri ("bunlar", "onun" gibi) açıkla.
SADECE yeniden yazılmış soruyu döndür, başka açıklama ekleme.

KONUŞMA GEÇMİŞİ:
{gecmis_metni}

YENİ SORU: {soru}

BAĞIMSIZ SORU:"""

        yanit = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )
        return yanit.text.strip()

    def soru_sor(self, soru, secili_dosya=None):
        net_soru = self.soruyu_zenginlestir(soru)
        sonuc = cevap_uret(net_soru, secili_dosya=secili_dosya)

        self.gecmis.append({"soru": soru, "cevap": sonuc["cevap"]})

        return sonuc


if __name__ == "__main__":
    oturum = SohbetOturumu()
    soru1 = "Kütüphanede kaç güneş paneli var?"
    sonuc1 = oturum.soru_sor(soru1)
    print(f"Soru 1: {soru1}")
    print(f"Cevap 1: {sonuc1['cevap']}")