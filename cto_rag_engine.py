import os
import math
import time
import re

print("=" * 65)
print("🚀 LEVEL CTO: ENTERPRISE INTERACTIVE RAG ENGINE")
print("   Multi-File Auto-Chunking + In-Memory TF-IDF REPL Loop")
print("=" * 65)

KNOWLEDGE_DIR = "knowledge"
WINDOW_SIZE = 2  # Tiap chunk berisi 2 kalimat
OVERLAP = 1      # 1 kalimat saling tumpang-tindih agar konteks tidak terputus

def bersihkan_dan_token(teks):
    return re.findall(r'\b[a-zA-Z0-9\-_]+\b', teks.lower())

def potong_menjadi_chunks(teks, window_size=WINDOW_SIZE, overlap=OVERLAP):
    """Membelah dokumen panjang menjadi chunks berbasis kalimat"""
    kalimat = [k.strip() for k in re.split(r'(?<=[.!?])\s+', teks) if k.strip()]
    if len(kalimat) <= window_size:
        return [teks]
    
    chunks = []
    step = max(1, window_size - overlap)
    for i in range(0, len(kalimat), step):
        chunk = " ".join(kalimat[i:i + window_size])
        chunks.append(chunk)
        if i + window_size >= len(kalimat):
            break
    return chunks

# 1. SCAN DOKUMEN & PECAH JADI CHUNKS
daftar_chunks = []
if not os.path.exists(KNOWLEDGE_DIR):
    os.makedirs(KNOWLEDGE_DIR)

print(f"⚙️ Membaca dan memotong dokumen di '{KNOWLEDGE_DIR}/'...")
for nama_file in sorted(os.listdir(KNOWLEDGE_DIR)):
    if nama_file.endswith(".txt"):
        path = os.path.join(KNOWLEDGE_DIR, nama_file)
        with open(path, "r", encoding="utf-8") as f:
            konten = f.read().strip()
            if konten:
                chunks = potong_menjadi_chunks(konten)
                for idx, c in enumerate(chunks, 1):
                    tokens = bersihkan_dan_token(c)
                    daftar_chunks.append({
                        "file": nama_file,
                        "chunk_id": f"chunk-{idx}",
                        "teks": c,
                        "tokens": tokens
                    })

TOTAL_CHUNKS = len(daftar_chunks)
if TOTAL_CHUNKS == 0:
    print(f"❌ Tidak ada file teks di folder '{KNOWLEDGE_DIR}'.")
    exit()

print(f"✅ Berhasil memproses {TOTAL_CHUNKS} micro-chunks dari seluruh file.")

# 2. BANGUN VOCABULARY & HITUNG IDF DI DALAM RAM
vocab_df = {}
for c in daftar_chunks:
    kata_unik = set(c["tokens"])
    for k in kata_unik:
        vocab_df[k] = vocab_df.get(k, 0) + 1

vocab = sorted(list(vocab_df.keys()))
DIMENSI = len(vocab)
print(f"✨ Dimensi Ruang Vektor Terindeks: {DIMENSI} Term Unik.")

idf_weights = {}
for kata, df in vocab_df.items():
    idf_weights[kata] = math.log(1.0 + (TOTAL_CHUNKS / df))

def hitung_tfidf(tokens):
    total = len(tokens)
    if total == 0:
        return [0.0] * DIMENSI
    counts = {}
    for t in tokens:
        counts[t] = counts.get(t, 0) + 1
    return [(counts.get(k, 0) / total) * idf_weights.get(k, 0.0) for k in vocab]

# Simpan semua vektor chunk di RAM (Cache)
for c in daftar_chunks:
    c["vektor"] = hitung_tfidf(c["tokens"])

def cosine_similarity(v1, v2):
    dot = sum(x * y for x, y in zip(v1, v2))
    n1 = math.sqrt(sum(x**2 for x in v1))
    n2 = math.sqrt(sum(x**2 for x in v2))
    return 0.0 if (n1 == 0 or n2 == 0) else dot / (n1 * n2)

print("\n" + "=" * 65)
print("🤖 ENTERPRISE RAG BOT SIAP! (Ketik 'keluar' atau 'exit' untuk selesai)")
print("=" * 65)

# 3. INTERACTIVE CHAT LOOP (REPL)
CTO_THRESHOLD = 0.18  # Ambang batas kecocokan chunk

while True:
    try:
        query = input("\nKamu > ").strip()
    except (KeyboardInterrupt, EOFError):
        print("\nSesi diakhiri.")
        break
        
    if not query:
        continue
    if query.lower() in ["exit", "keluar", "quit", "q"]:
        print("👋 Sistem dimatikan. Sampai jumpa!")
        break

    t_start = time.time()
    token_tanya = bersihkan_dan_token(query)
    vektor_tanya = hitung_tfidf(token_tanya)

    # Retrieval: Cari chunk terbaik dari seluruh corpus
    skor_terbaik = -1.0
    chunk_terpilih = None

    for c in daftar_chunks:
        sim = cosine_similarity(vektor_tanya, c["vektor"])
        if sim > skor_terbaik:
            skor_terbaik = sim
            chunk_terpilih = c

    latency_ms = (time.time() - t_start) * 1000

    print("─" * 65)
    # Evaluasi Guardrail
    if skor_terbaik < CTO_THRESHOLD:
        print(f"🛑 REJECTED (Skor tertinggi: {skor_terbaik * 100:.1f}% | Batas: {CTO_THRESHOLD * 100:.0f}%)")
        print("🤖 RAG-Bot: Maaf, tidak ada informasi yang relevan pada dokumen resmi.")
    else:
        print(f"🎯 MATCH: [{chunk_terpilih['file']} :: {chunk_terpilih['chunk_id']}] (Akurasi: {skor_terbaik * 100:.1f}% | {latency_ms:.1f}ms)")
        print(f"📜 Bukti Fakta: \"{chunk_terpilih['teks']}\"")
        print(f"\n🤖 RAG-Bot:")
        print(f"   Berdasarkan rujukan resmi [{chunk_terpilih['file']}], {chunk_terpilih['teks']} ✨")
    print("─" * 65)
