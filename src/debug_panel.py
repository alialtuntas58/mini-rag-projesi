import streamlit as st
from vektor_deposu import koleksiyon
from cevap_uret import MESAFE_ESIGI


def debug_sekmesi_ciz():
    st.subheader("🛠️ Sistem Bilgisi")
    bilgi = [
        ("Embedding modeli", "gemini-embedding-001"),
        ("LLM", "gemini-3.5-flash"),
        ("Chunk boyutu / örtüşme", "800 / 100 karakter"),
        ("Hibrit arama aday sayısı", "8"),
        ("Reranker sonrası bağlam parça sayısı", "4"),
        ("Reranker", "Aktif (LLM tabanlı)"),
        ("Mesafe eşiği", str(MESAFE_ESIGI)),
        ("Veritabanındaki parça sayısı", str(koleksiyon.count())),
    ]
    st.table([{"Ayar": k, "Değer": v} for k, v in bilgi])

    st.divider()
    st.subheader("Son Sorgunun Ayrıntıları")

    son = st.session_state.get("son_debug")
    if not son:
        st.info("Henüz soru sorulmadı. Sohbet sekmesinden bir soru sorduktan sonra ayrıntılar burada görünür.")
        return

    d = son.get("debug") or {}
    st.write(f"**Soru:** {son['soru']}")

    k1, k2, k3 = st.columns(3)
    k1.metric("Yanıt süresi (sn)", d.get("sure_saniye", "-"))
    k2.metric("Prompt token", d.get("prompt_token") if d.get("prompt_token") is not None else "-")
    k3.metric("Cevap token", d.get("cevap_token") if d.get("cevap_token") is not None else "-")

    mesafe = d.get("mesafe")
    st.write(f"**Güven seviyesi:** {son.get('guven', '-')}")
    st.write(f"**En yakın parça mesafesi:** {round(mesafe, 4) if mesafe is not None else '-'}")
    st.write(f"**Önbellekten geldi:** {'Evet' if d.get('onbellekten') else 'Hayır'}")
    st.write(f"**LLM çağrıldı:** {'Evet' if d.get('llm_cagrildi') else 'Hayır'}")
    st.caption("Token sayıları yalnızca cevap üretme çağrısını kapsar, reranker çağrısı dahil değildir.")

    parcalar = d.get("parcalar", [])
    st.write(f"**LLM'e gönderilen parça sayısı:** {len(parcalar)}")
    for p in parcalar:
        with st.expander(f"{p['dosya']} - Sayfa {p['sayfa']}"):
            st.write(p["metin"])
