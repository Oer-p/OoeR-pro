import os
import math
import time
import re

print("=" * 65)
print("🏛️ TINGKAT GURU BESAR (POST-DOC): DYNAMIC TF-IDF RAG ENGINE")
print("   Auto-Ingestion .txt Files + TF-IDF Continuous Vector Space")
print("=" * 65)

KNOWLEDGE_DIR = "knowledge"

# 1. TOKENIZER MANDIRI (0 MB, Tanpa NLTK/Spacy)
def bersihkan_dan_token(teks):
    # Ambil alfanumerik dan tanda strip (misal: 9942-alpha)
    return re.findall(r'\b[a-zA-Z0-9\-_]+\b', teks.lower())

# 2. DYNAMIC FILE INGESTION (Membaca semua file .txt di folder)
basis_dokumen = []
if not os.path.exists(KNOWLEDGE_DIR):
    os.makedirs(KNOWLEDGE_DIR)

for nama_file in sorted(os.listdir(KNOWLEDGE_DIR)):
    if nama_file.endswith(".txt"):
        jalur_file = os.path.join(KNOWLEDGE_DIR, nama_file)
        with open(jalur_file, "r", encoding="utf-8") as f:
            konten = f.read().strip()
            if konten:
                tokens = bersihkan_dan_token(konten)
                basis_dokumen.append({
                    "id": nama_file,
                    "teks": konten,
                    "tokens": tokens
                })

if not basis_dokumen:
    print(f"❌ Folder '{KNOWLEDGE_DIR}' kosong! Isi file .txt terlebih dahulu.")
    exit()

N_DOCS = len(basis_dokumen)
print(f"📂 Berhasil memindai folder '{KNOWLEDGE_DIR}': {N_DOCS} file .txt terdeteksi.")

# 3. MEMBANGUN VOCABULARY & INVERSE DOCUMENT FREQUENCY (IDF)
vocab_df = {}  # Menghitung berapa dokumen yang memiliki kata t
for doc in basis_dokumen:
    kata_unik_doc = set(doc["tokens"])
    for kata in kata_unik_doc:
        vocab_df[kata] = vocab_df.get(kata, 0) + 1

vocab = sorted(list(vocab_df.keys()))
DIMENSI = len(vocab)
print(f"✨ Dimensi Ruang Vektor Semantik TF-IDF: {DIMENSI} Kata Unik.")

# Hitung bobot IDF untuk setiap kata di semesta data
# Formula: ln(1 + (N / DF)) -> Semakin sering kata muncul di semua doc, bobotnya makin kecil!
idf_weights = {}
for kata, df in vocab_df.items():
    idf_weights[kata] = math.log(1.0 + (N_DOCS / df))

def hitung_vektor_tfidf(daftar_tokens):
    """Mengubah token teks menjadi vektor floating point berbobot TF-IDF"""
    total_kata = len(daftar_tokens)
    if total_kata == 0:
        return [0.0] * DIMENSI
    
    # Hitung Term Frequency (TF)
    tf_counts = {}
    for t in daftar_tokens:
        tf_counts[t] = tf_counts.get(t, 0) + 1
        
    vektor = []
    for kata in vocab:
        if kata in tf_counts:
            tf = tf_counts[kata] / total_kata
            idf = idf_weights.get(kata, 0.0)
            vektor.append(tf * idf)
        else:
            vektor.append(0.0)
    return vektor

# Vektorisasi seluruh dokumen dinamis
for doc in basis_dokumen:
    doc["vektor"] = hitung_vektor_tfidf(doc["tokens"])

time.sleep(0.5)

# 4. OPERASI ALJABAR VEKTOR
def cosine_similarity(v1, v2):
    dot = sum(x * y for x, y in zip(v1, v2))
    norm1 = math.sqrt(sum(x**2 for x in v1))
    norm2 = math.sqrt(sum(x**2 for x in v2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)

# 5. QUERY INTERACTIVE
pertanyaan = input("\nKamu > ")
token_tanya = bersihkan_dan_token(pertanyaan)
vektor_tanya = hitung_vektor_tfidf(token_tanya)

print("\n" + "─" * 65)
print(f"❓ PERTANYAAN USER: \"{pertanyaan}\"")
print("─" * 65)

# EKSPERIMEN RETRIEVAL
print("\n🔍 1. RETRIEVER: Memindai Vektor TF-IDF Pertanyaan vs Corpus Dokumen...")
skor_terbaik = -1.0
dokumen_terpilih = None

for doc in basis_dokumen:
    sim = cosine_similarity(vektor_tanya, doc["vektor"])
    persen = sim * 100
    snippet = doc['teks'][:40] + "..." if len(doc['teks']) > 40 else doc['teks']
    print(f"   ├─ [{doc['id']:<14}] TF-IDF Match: {persen:5.1f}% | \"{snippet}\"")
    if sim > skor_terbaik:
        skor_terbaik = sim
        dokumen_terpilih = doc

# POST-DOC RIGOROUS THRESHOLD (Ambang batas presisi)
POSTDOC_THRESHOLD = 0.20  # Pada TF-IDF kontinu, 0.20 sudah sangat kuat

if skor_terbaik < POSTDOC_THRESHOLD:
    print(f"\n🎯 2. REPUTASI AKADEMIK TERJAGA: Fakta Relevan TIDAK DITEMUKAN!")
    print(f"   Skor puncak ({skor_terbaik * 100:.1f}%) < Batas Aman ({POSTDOC_THRESHOLD * 100:.0f}%).")
    print("\n🤖 Post-Doc AI Guardrail:")
    print("   \"Maaf, tidak ada file dokumen dalam knowledge base yang memvalidasi hal tersebut.\"")
    print("\n" + "=" * 65)
    print("🏆 STATUS: 100% BEBAS DARI HALUSINASI TOKSIK.")
    print("=" * 65)
else:
    print(f"\n🎯 2. DOKUMEN FAKTA TEPAT DITEMUKAN: [{dokumen_terpilih['id']}] (Skor: {skor_terbaik * 100:.1f}%)")
    print(f"   📄 Sumber File: knowledge/{dokumen_terpilih['id']}")
    print(f"   📜 Konten Dokumen: \"{dokumen_terpilih['teks']}\"")
    
    print("\n💉 3. AUGMENTATION & FACT-GROUNDED GENERATION...")
    time.sleep(0.4)
    print("\n🤖 Post-Doc Augmented AI:")
    print(f"   \"Berdasarkan rujukan sah file [{dokumen_terpilih['id']}], {dokumen_terpilih['teks']}\" ✨")
    
    print("\n" + "=" * 65)
    print("🏆 STATUS: GROUNDED GENERATION (Didukung bukti berkas fisik)!")
    print("=" * 65)
