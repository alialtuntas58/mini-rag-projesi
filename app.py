import streamlit as st
import os
from sohbet import SohbetOturumu
from pdf_okuyucu import pdf_metin_cikar
from chunker import metni_parcala
from vektor_deposu import parcalari_kaydet, koleksiyon

st.set_page_config(page_title="Akıllı Doküman Asistanı", page_icon="📚")
st.title("📚 Akıllı Doküman Soru-Cevap Sistemi")

if "oturum" not in st.session_state:
    st.session_state.oturum = SohbetOturumu()

if "mesajlar" not in st.session_state:
    st.session_state.mesajlar = []

if "islenen_dosyalar" not in st.session_state:
    st.session_state.islenen_dosyalar = set()


def kayitli_dosyalari_getir():
    """ChromaDB'deki tüm kayıtların metadata'sından benzersiz dosya adlarını çıkarır."""
    tum_kayitlar = koleksiyon.get()
    if not tum_kayitlar["metadatas"]:
        return set()
    dosyalar = set(m["dosya"] for m in tum_kayitlar["metadatas"])
    return dosyalar


# --- Kenar çubuğu: PDF yükleme alanı ---
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
                    gecici_yol = os.path.join("gecici_yuklemeler", dosya.name)
                    os.makedirs("gecici_yuklemeler", exist_ok=True)
                    with open(gecici_yol, "wb") as f:
                        f.write(dosya.getbuffer())

                    try:
                        sayfalar = pdf_metin_cikar(gecici_yol)
                    except Exception as e:
                        st.error(f"❌ {dosya.name} okunamadı. Dosya bozuk veya şifreli olabilir.")
                        continue

                    toplam_karakter = sum(len(metin.strip()) for _, metin in sayfalar)
                    if toplam_karakter < 20:
                        st.warning(f"⚠️ {dosya.name} içinde okunabilir metin bulunamadı. "
                                   f"Bu dosya taranmış bir görüntü olabilir (OCR desteklenmiyor).")
                        continue

                    parcalar = metni_parcala(sayfalar)

                    if not parcalar:
                        st.warning(f"⚠️ {dosya.name} işlenemedi, içerik boş görünüyor.")
                        continue

                    parcalari_kaydet(parcalar, dosya.name)
                    st.session_state.islenen_dosyalar.add(dosya.name)
                    st.success(f"✅ {dosya.name} işlendi ({len(parcalar)} parça)")

                except Exception as e:
                    st.error(f"❌ {dosya.name} işlenirken beklenmeyen bir hata oluştu: {str(e)}")

    st.divider()
    st.caption(f"Veritabanında toplam {koleksiyon.count()} parça kayıtlı.")

    st.divider()

    kayitli_dosyalar_sidebar = kayitli_dosyalari_getir()
    if kayitli_dosyalar_sidebar:
        st.subheader("Yüklenen Dosyalar")
        for dosya_adi in sorted(kayitli_dosyalar_sidebar):
            st.write(f"📄 {dosya_adi}")

    st.divider()

    if st.button("🗑️ Sohbeti Temizle", use_container_width=True):
        st.session_state.mesajlar = []
        st.session_state.oturum = SohbetOturumu()
        st.rerun()


# --- Ana sohbet alanı ---
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

for mesaj in st.session_state.mesajlar:
    with st.chat_message(mesaj["rol"]):
        st.write(mesaj["icerik"])

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
            sonuc = {"cevap": cevap_metni}
        else:
            with st.spinner("Düşünüyorum..."):
                try:
                    sonuc = st.session_state.oturum.soru_sor(kullanici_sorusu)
                    st.write(sonuc["cevap"])

                    if sonuc["kaynaklar"]:
                        kaynak_metni = ", ".join(f"{d} - Sayfa {s}" for d, s in sonuc["kaynaklar"])
                        st.caption(f"📄 Kaynak: {kaynak_metni}")
                except Exception as e:
                    st.error("Şu anda cevap üretilemedi (muhtemelen Gemini sunucuları yoğun). Lütfen birkaç saniye sonra tekrar dener misin?")
                    sonuc = {"cevap": "Üzgünüm, bir hata oluştu, lütfen tekrar dener misin?"}

    st.session_state.mesajlar.append({"rol": "assistant", "icerik": sonuc["cevap"]})