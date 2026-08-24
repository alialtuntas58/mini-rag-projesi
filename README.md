# 🧠 Gelişmiş Akıllı Doküman Asistanı (Advanced RAG)

Bu proje, Retrieval-Augmented Generation (RAG) mimarisini kullanarak, kullanıcıların yüklediği PDF dokümanları üzerinden güvenilir, kaynak gösteren ve halüsinasyondan arındırılmış cevaplar üreten gelişmiş bir yapay zeka asistanıdır.

## 🚀 Öne Çıkan Özellikler

*   **Çoklu Doküman Yönetimi:** Birden fazla PDF'i aynı anda indeksleme ve arama yapabilme.
*   **Hybrid Search (Melez Arama):** Anlamsal arama (Gemini Embeddings) ve anahtar kelime aramasını (BM25) birleştirerek en doğru sonuçları bulma.
*   **LLM Reranking:** Bulunan sonuçları LLM ile yeniden sıralayarak bağlam kalitesini maksimize etme.
*   **Kaynak Gösterimi (Groundedness):** Üretilen her cevabın sonuna ilgili PDF dosyasını ve sayfa numarasını referans olarak ekleme.
*   **Prompt Injection ve Halüsinasyon Koruması:** Doküman dışı sorularda uydurma cevap vermek yerine kontrollü bir şekilde "Bilgi bulunmuyor" yanıtı döndürme.
*   **Modern Mimari:** FastAPI ile servis mimarisi ve Docker ile izole, tek tıkla çalıştırılabilir altyapı.

## 🛠️ Kullanılan Teknolojiler

*   **Dil:** Python 3.11+
*   **Backend:** FastAPI, Uvicorn
*   **LLM & Embedding:** Google Gemini (genai)
*   **Vektör Veritabanı:** ChromaDB
*   **Arama Algoritmaları:** Rank-BM25 (Keyword Search)
*   **Doküman İşleme:** PyMuPDF (fitz)
*   **Altyapı:** Docker & Docker Compose

## 📦 Kurulum ve Çalıştırma

Projeyi bilgisayarınızda yerel olarak çalıştırmanın en kolay yolu **Docker** kullanmaktır.

1. Depoyu bilgisayarınıza indirin:
   ```bash
   git clone <repo-url>
   cd mini-rag-projesi