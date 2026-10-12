with open("app.py", "r", encoding="utf-8") as f:
    kod = f.read()

if "markdown_olustur" in kod:
    print("app.py zaten güncellenmiş, işlem yapılmadı.")
    raise SystemExit

degisiklikler = [
    (
        '''from dosya_hash import dosya_hash_hesapla, hash_kayitli_mi
''',
        '''from dosya_hash import dosya_hash_hesapla, hash_kayitli_mi
from disa_aktar import markdown_olustur, json_olustur
''',
    ),
    (
        '''                st.caption(f"📄 Kaynak: {kaynak_metni}{guven_metni}")
''',
        '''                st.caption(f"📄 Kaynak: {kaynak_metni}{guven_metni}")
                soru_dl = st.session_state.mesajlar[i - 1]["icerik"] if i > 0 else ""
                dl1, dl2, _ = st.columns([2, 2, 6])
                with dl1:
                    st.download_button(
                        "⬇️ Markdown",
                        data=markdown_olustur(soru_dl, mesaj["icerik"], mesaj["kaynaklar"], mesaj.get("guven")),
                        file_name=f"cevap_{i}.md",
                        mime="text/markdown",
                        key=f"md_{i}",
                    )
                with dl2:
                    st.download_button(
                        "⬇️ JSON",
                        data=json_olustur(soru_dl, mesaj["icerik"], mesaj["kaynaklar"], mesaj.get("guven")),
                        file_name=f"cevap_{i}.json",
                        mime="application/json",
                        key=f"json_{i}",
                    )
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

with open("app.py", "w", encoding="utf-8") as f:
    f.write(kod)

print("app.py güncellendi.")
