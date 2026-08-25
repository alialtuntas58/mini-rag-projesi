import streamlit as st
import os
from sohbet import SohbetOturumu
from pdf_okuyucu import pdf_metin_cikar
from chunker import metni_parcala
from vektor_deposu import parcalari_kaydet, koleksiyon
from feedback import feedback_kaydet, feedback_ozeti, feedback_kayitlarini_getir
from ozet import dokuman_ozetle
from karsilastir import dokumanlari_karsilastir

st.set_page_config(page_title="Akıllı Doküman Asistanı", page_icon="📚")
st.title("📚 Akıllı Doküman Soru-Cevap Sistemi")

if "oturum" not in st.session_state:
    st.session_state.oturum = SohbetOturumu()

if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = []

if "islenen_dosyalar" not in st.session_state:
    st.session_state.islenen_dosyalar = set()

if "secili_dosya" not in st.session_state:
    st.session_state.secili_dosya = None


def kayitli_dosyalari_getir():
    tum_kayitlar = koleksiyon.get()
    if not tum_kayitlar["metadatas"]:
        return set()
    dosyalar = set(m["dosya"] for m in tum_kayitlar["metadatas"])
    return dosyalar


with st.sidebar:
    st.header("📄 Doküman Yükle")
    yuklenen_dosyalar = st.file_uploader(
        "PDF dosyalarını seç",
        type="pdf",
        accept_multiple_files=True
    )

    MAKS_DOSYA_BOYUTU_MB = 20

    if yuklenen_dosyalar:
        for dosya in yuklenen_dosyalar:
            if dosya.name in st.session_state.islenen_dosyalar:
                continue

            boyut_mb = dosya.size / (1024 * 1024)
            if boyut_mb > MAKS_DOSYA_BOYUTU_MB:
                st.error(f"❌ {dosya.name} çok büyük ({boyut_mb:.1f} MB). Maksimum {MAKS_DOSYA_BOYUTU_MB} MB olmalı.")
                continue

            with st.spinner(f"{dosya.name} işleniyor..."):
                try:
                    _proje_koku = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                    _gecici_klasor = os.path.join(_proje_koku, "gecici_yuklemeler")
                    os.makedirs(_gecici_klasor, exist_ok=True)
                    gecici_yol = os.path.join(_gecici_klasor, dosya.name)
                    with open(gecici_yol, "wb") as f:
                        f.write(dosya.getbuffer())

                    try:
                        sayfalar = pdf_metin_cikar(gecici_yol)
                    except Exception as e:
                        st.error(f"❌ {dosya.name} okunamadı. Dosya bozuk veya şifreli olabilir.")
                        continue

                    toplam_karakter = sum(len(metin.strip()) for _, metin in sayfalar)
                    ocr_kullanildi = False

                    if toplam_karakter < 20:
                        st.info(f"ℹ️ {dosya.name} taranmış bir belge gibi görünüyor, OCR uygulanıyor...")
                        try:
                            from ocr import pdf_ocr_ile_oku
                            sayfalar = pdf_ocr_ile_oku(gecici_yol)
                            ocr_kullanildi = True

                            toplam_karakter_ocr = sum(len(metin.strip()) for _, metin in sayfalar)
                            if toplam_karakter_ocr < 20:
                                st.warning(f"⚠️ {dosya.name} OCR ile de okunamadı, içerik boş görünüyor.")
                                continue
                        except Exception as e:
                            st.error(f"❌ {dosya.name} için OCR başarısız oldu: {str(e)[:150]}")
                            continue

                    parcalar = metni_parcala(sayfalar)

                    if not parcalar:
                        st.warning(f"⚠️ {dosya.name} işlenemedi, içerik boş görünüyor.")
                        continue

                    parcalari_kaydet(parcalar, dosya.name)
                    st.session_state.islenen_dosyalar.add(dosya.name)
                    ocr_notu = " (OCR ile okundu)" if ocr_kullanildi else ""
                    st.success(f"✅ {dosya.name} işlendi ({len(parcalar)} parça){ocr_notu}")

                except Exception as e:
                    st.error(f"❌ {dosya.name} işlenirken beklenmeyen bir hata oluştu: {str(e)}")

    st.divider()
    st.caption(f"Veritabanında toplam {koleksiyon.count()} parça kayıtlı.")
    st.divider()

    kayitli_dosyalar_sidebar = kayitli_dosyalari_getir()
    if kayitli_dosyalar_sidebar:
        st.subheader("Doküman Seçimi")
        secenekler = ["🔍 Tüm dokümanlar"] + sorted(kayitli_dosyalar_sidebar)
        secim = st.radio("Aramayı sınırla:", secenekler, label_visibility="collapsed")
        st.session_state.secili_dosya = None if secim == "🔍 Tüm dokümanlar" else secim

    st.divider()

    if st.button("🗑️ Sohbeti Temizle", use_container_width=True):
        st.session_state.mesajlar = []
        st.session_state.oturum = SohbetOturumu()
        st.rerun()


sekme_sohbet, sekme_ozet, sekme_karsilastir, sekme_degerlendirme = st.tabs(
    ["💬 Sohbet", "📝 Özet", "⚖️ Karşılaştır", "📊 Değerlendirme"]
)

with sekme_sohbet:
    META_ANAHTAR_KELIMELER = ["kaç dosya", "hangi dosya", "hangi doküman", "kaç doküman", "neler yükledim", "dosyaları listele"]

    secilen_soru = None

    if not st.session_state.mesajlar:
        st.write("💡 Örnek sorular:")
        ornek_sorular = [
            "Bu dokümanlar neyden bahsediyor?",
            "Kütüphanede kaç personel çalışıyor?",
            "Enerji ve çevre konusunda neler yapılıyor?"
        ]
        kolonlar = st.columns(len(ornek_sorular))
        for kolon, soru in zip(kolonlar, ornek_sorular):
            with kolon:
                if st.button(soru, use_container_width=True):
                    secilen_soru = soru

    for i, mesaj in enumerate(st.session_state.mesajlar):
        with st.chat_message(mesaj["rol"]):
            st.write(mesaj["icerik"])

            if mesaj["rol"] == "assistant" and mesaj.get("kaynaklar"):
                kaynak_metni = ", ".join(f"{d} - Sayfa {s}" for d, s in mesaj["kaynaklar"])
                guven_metni = f" | Güven: {mesaj['guven']}" if mesaj.get("guven") else ""
                st.caption(f"📄 Kaynak: {kaynak_metni}{guven_metni}")

            if mesaj["rol"] == "assistant" and mesaj.get("gosterilebilir_feedback"):
                verilen_oy = mesaj.get("verilen_oy")

                if verilen_oy:
                    etiket = "👍 Beğendiniz" if verilen_oy == "begeni" else "👎 Beğenmediniz"
                    st.caption(f"{etiket} - geri bildiriminiz kaydedildi")
                else:
                    kol1, kol2, _ = st.columns([1, 1, 8])
                    onceki_soru = st.session_state.mesajlar[i - 1]["icerik"] if i > 0 else ""
                    with kol1:
                        if st.button("👍", key=f"begeni_{i}"):
                            feedback_kaydet(onceki_soru, mesaj["icerik"], "begeni")
                            st.session_state.mesajlar[i]["verilen_oy"] = "begeni"
                            st.rerun()
                    with kol2:
                        if st.button("👎", key=f"begenmedi_{i}"):
                            feedback_kaydet(onceki_soru, mesaj["icerik"], "begenmedi")
                            st.session_state.mesajlar[i]["verilen_oy"] = "begenmedi"
                            st.rerun()

    hic_dosya_yok = koleksiyon.count() == 0

    if hic_dosya_yok:
        st.info("👈 Başlamak için soldan en az bir PDF dosyası yükle.")
        kullanici_sorusu = None
    else:
        kullanici_sorusu = st.chat_input("Dokümanlar hakkında bir soru sor...") or secilen_soru

    if kullanici_sorusu:
        st.session_state.mesajlar.append({"rol": "user", "icerik": kullanici_sorusu})
        with st.chat_message("user"):
            st.write(kullanici_sorusu)

        with st.chat_message("assistant"):
            soru_kucuk = kullanici_sorusu.lower()

            if any(anahtar in soru_kucuk for anahtar in META_ANAHTAR_KELIMELER):
                kayitli_dosyalar = kayitli_dosyalari_getir()
                if kayitli_dosyalar:
                    dosya_listesi = ", ".join(sorted(kayitli_dosyalar))
                    cevap_metni = f"Şu an {len(kayitli_dosyalar)} doküman yüklü: {dosya_listesi}"
                else:
                    cevap_metni = "Henüz hiç doküman yüklenmedi."
                st.write(cevap_metni)
                yeni_mesaj = {"rol": "assistant", "icerik": cevap_metni, "gosterilebilir_feedback": False}
            else:
                with st.spinner("Düşünüyorum..."):
                    try:
                        secili = st.session_state.get("secili_dosya", None)
                        sonuc = st.session_state.oturum.soru_sor(kullanici_sorusu, secili_dosya=secili)
                        st.write(sonuc["cevap"])

                        if sonuc["kaynaklar"]:
                            kaynak_metni = ", ".join(f"{d} - Sayfa {s}" for d, s in sonuc["kaynaklar"])
                            st.caption(f"📄 Kaynak: {kaynak_metni} | Güven: {sonuc.get('guven', 'Bilinmiyor')}")

                        yeni_mesaj = {
                            "rol": "assistant",
                            "icerik": sonuc["cevap"],
                            "kaynaklar": sonuc["kaynaklar"],
                            "guven": sonuc.get("guven", "Bilinmiyor"),
                            "gosterilebilir_feedback": True
                        }
                    except Exception as e:
                        st.error("Şu anda cevap üretilemedi. Lütfen birkaç saniye sonra tekrar dener misin?")
                        yeni_mesaj = {"rol": "assistant", "icerik": "Üzgünüm, bir hata oluştu, lütfen tekrar dener misin?", "gosterilebilir_feedback": False}

        st.session_state.mesajlar.append(yeni_mesaj)
        st.rerun()


with sekme_ozet:
    st.subheader("📝 Doküman Özeti")

    kayitli_dosyalar_ozet = kayitli_dosyalari_getir()

    if not kayitli_dosyalar_ozet:
        st.info("Önce soldan bir doküman yükle.")
    else:
        secilen_dosya_ozet = st.selectbox("Özetlenecek dokümanı seç:", sorted(kayitli_dosyalar_ozet))

        if st.button("Özet Oluştur"):
            with st.spinner(f"{secilen_dosya_ozet} özetleniyor..."):
                try:
                    sonuc = dokuman_ozetle(secilen_dosya_ozet)
                    st.session_state.son_ozet = sonuc
                    st.session_state.son_ozet_dosya = secilen_dosya_ozet
                except Exception as e:
                    st.error("Şu anda özet oluşturulamadı (muhtemelen günlük API kotası doldu). Lütfen daha sonra tekrar dene.")

        if st.session_state.get("son_ozet"):
            st.caption(f"{st.session_state.son_ozet_dosya} - {st.session_state.son_ozet['sayfa_sayisi']} sayfa")
            st.write(st.session_state.son_ozet["ozet"])


with sekme_karsilastir:
    st.subheader("⚖️ Doküman Karşılaştırma")

    kayitli_dosyalar_kars = sorted(kayitli_dosyalari_getir())

    if len(kayitli_dosyalar_kars) < 2:
        st.info("Karşılaştırma için en az 2 doküman yüklenmiş olmalı.")
    else:
        kol1, kol2 = st.columns(2)
        with kol1:
            dosya_a = st.selectbox("1. Doküman:", kayitli_dosyalar_kars, key="kars_dosya_a")
        with kol2:
            secenekler_b = [d for d in kayitli_dosyalar_kars if d != dosya_a]
            dosya_b = st.selectbox("2. Doküman:", secenekler_b, key="kars_dosya_b")

        konu = st.text_input("Karşılaştırma konusu (isteğe bağlı):", placeholder="örn. çalışma saatleri")

        if st.button("Karşılaştır"):
            with st.spinner("Dokümanlar karşılaştırılıyor..."):
                try:
                    sonuc = dokumanlari_karsilastir(dosya_a, dosya_b, konu if konu else None)
                    st.session_state.son_karsilastirma = sonuc
                except Exception as e:
                    st.error("Şu anda karşılaştırma yapılamadı (muhtemelen günlük API kotası doldu). Lütfen daha sonra tekrar dene.")

        if st.session_state.get("son_karsilastirma"):
            st.write(st.session_state.son_karsilastirma)


with sekme_degerlendirme:
    st.subheader("📊 Kullanıcı Geri Bildirim Özeti")

    ozet = feedback_ozeti()

    if ozet["toplam"] == 0:
        st.info("Henüz hiç geri bildirim verilmedi. Sohbet sekmesinde cevapları 👍/👎 ile değerlendirebilirsin.")
    else:
        m1, m2, m3 = st.columns(3)
        m1.metric("Toplam Geri Bildirim", ozet["toplam"])
        m2.metric("👍 Beğeni", ozet["begeni"])
        m3.metric("👎 Beğenmedi", ozet["begenmedi"])

        st.metric("Memnuniyet Oranı", f"%{ozet['begeni_orani']:.1f}")

        st.divider()
        st.subheader("Beğenilmeyen Cevaplar")
        kayitlar = feedback_kayitlarini_getir()
        begenilmeyenler = [k for k in kayitlar if k["puan"] == "begenmedi"]

        if begenilmeyenler:
            for k in begenilmeyenler:
                with st.expander(f"❓ {k['soru']}"):
                    st.write(f"**Cevap:** {k['cevap']}")
                    st.caption(f"Zaman: {k['zaman']}")
        else:
            st.write("Henüz beğenilmeyen cevap yok. 🎉")
