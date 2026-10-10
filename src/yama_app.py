with open("app.py", "r", encoding="utf-8") as f:
    kod = f.read()

if "sekme_debug" in kod:
    print("app.py zaten güncellenmiş, işlem yapılmadı.")
    raise SystemExit

degisiklikler = [
    (
        '''sekme_sohbet, sekme_ozet, sekme_karsilastir, sekme_degerlendirme = st.tabs(
    ["💬 Sohbet", "📝 Özet", "⚖️ Karşılaştır", "📊 Değerlendirme"]
)''',
        '''sekme_sohbet, sekme_ozet, sekme_karsilastir, sekme_degerlendirme, sekme_debug = st.tabs(
    ["💬 Sohbet", "📝 Özet", "⚖️ Karşılaştır", "📊 Değerlendirme", "🛠️ Debug"]
)''',
    ),
    (
        '''                        sonuc = st.session_state.oturum.soru_sor(kullanici_sorusu, secili_dosya=secili)
''',
        '''                        sonuc = st.session_state.oturum.soru_sor(kullanici_sorusu, secili_dosya=secili)
                        st.session_state.son_debug = {"soru": kullanici_sorusu, "guven": sonuc.get("guven"), "debug": sonuc.get("debug", {})}
''',
    ),
]

for eski, yeni in degisiklikler:
    if kod.count(eski) != 1:
        print("HATA: beklenen kod bulunamadı veya birden fazla kez geçiyor:")
        print(eski[:80])
        print("app.py değiştirilmedi.")
        raise SystemExit
    kod = kod.replace(eski, yeni)

kod = kod.rstrip("\n") + "\n\n\nwith sekme_debug:\n    from debug_panel import debug_sekmesi_ciz\n    debug_sekmesi_ciz()\n"

with open("app.py", "w", encoding="utf-8") as f:
    f.write(kod)

print("app.py güncellendi.")
