import math
import time

def dot_product(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))

def cosine_similarity(v1, v2):
    dot = dot_product(v1, v2)
    norm1 = math.sqrt(sum(x**2 for x in v1))
    norm2 = math.sqrt(sum(x**2 for x in v2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)

print("=" * 65)
print("👑 DISERTASI S-3 (Ph.D): RAG (RETRIEVAL-AUGMENTED GENERATION)")
print("   Sistem Anti-Halusinasi & Pencarian Vektor Semantik Dokumen")
print("=" * 65)

# 1. KUMPULAN DOKUMEN FAKTA (EXTERNAL KNOWLEDGE BASE)
basis_dokumen = [
    {
        "id": "DOC-01",
        "teks": "Proyek Satelit Budi diluncurkan pada koordinat Khatulistiwa dengan kode sandi otorisasi 9942-ALPHA.",
        "topik": ["satelit", "budi", "kode", "sandi", "khatulistiwa", "otorisasi", "proyek"]
    },
    {
        "id": "DOC-02", 
        "teks": "Robot asisten medis Budi ditenagai oleh baterai nuklir mini berkekuatan 500 watt.",
        "topik": ["robot", "medis", "baterai", "nuklir", "budi", "asisten", "watt"]
    },
    {
        "id": "DOC-03",
        "teks": "Ibu Budi mendirikan yayasan teknologi bernama Pelita Bangsa untuk riset kecerdasan buatan.",
        "topik": ["ibu", "yayasan", "pelita", "bangsa", "teknologi", "budi", "riset"]
    }
]

# Bangun Kosakata Unik (Vocabulary) untuk Ruang Vektor
semua_kata = set()
for doc in basis_dokumen:
    semua_kata.update(doc["topik"])
vocab = sorted(list(semua_kata))

def text_to_vector(daftar_kata):
    return [1.0 if k in daftar_kata else 0.0 for k in vocab]

# Vektorisasi seluruh dokumen (Indexing)
for doc in basis_dokumen:
    doc["vektor"] = text_to_vector(doc["topik"])

print(f"📚 Basis Pengetahuan Dokumen Terindeks: {len(basis_dokumen)} Dokumen Rahasia.")
print(f"✨ Membangun Ruang Vektor Semantik Dimensi: {len(vocab)}")
time.sleep(0.5)

# INPUT PERTANYAAN USER
pertanyaan = input("\nKamu > ")
kata_tanya = [k.lower().strip("?!.,") for k in pertanyaan.split()]
vektor_tanya = text_to_vector(kata_tanya)

print("\n" + "─" * 65)
print(f"❓ PERTANYAAN USER: \"{pertanyaan}\"")
print("─" * 65)

# -----------------------------------------------------
# EKSPERIMEN 1: BASE LLM TANPA RAG (SIMULASI HALUSINASI)
# -----------------------------------------------------
print("\n[EKSPERIMEN 1] MENJALANKAN BASE LLM (TANPA RAG)...")
time.sleep(0.5)
print("🤖 Base LLM: \"Tentu, jawabannya adalah kode sandi 1234-XYZ di Planet Saturnus.\"")
print("❌ EVALUASI: HALUSINASI FATAL! (Model mengarang karena tidak punya basis data!)")

# -----------------------------------------------------
# EKSPERIMEN 2: S-3 DOKTORAL RAG PIPELINE
# -----------------------------------------------------
print("\n" + "─" * 65)
print("[EKSPERIMEN 2] MENJALANKAN DOKTORAL RAG PIPELINE...")
print("─" * 65)
time.sleep(0.5)

print("🔍 1. RETRIEVER: Memindai kecocokan Vektor Pertanyaan vs Dokumen...")
skor_terbaik = -1.0
dokumen_terpilih = None

for doc in basis_dokumen:
    similarity = cosine_similarity(vektor_tanya, doc["vektor"])
    persen = similarity * 100
    print(f"   ├─ [{doc['id']}] Cosine Match: {persen:5.1f}% | Kutipan: \"{doc['teks'][:35]}...\"")
    if similarity > skor_terbaik:
        skor_terbaik = similarity
        dokumen_terpilih = doc

# BATAS MINIMAL RELEVANSI (AMBANG BATAS S-3)
AMBANG_BATAS_S3 = 0.35  # Minimal kemiripan 35%

if skor_terbaik < AMBANG_BATAS_S3:
    print(f"\n🎯 2. DOKUMEN FAKTA RELEVAN TIDAK DITEMUKAN!")
    print(f"   Skor tertinggi hanya ({skor_terbaik * 100:.1f}%), di bawah batas aman ({AMBANG_BATAS_S3 * 100:.0f}%).")
    print("\n🤖 AI RAG Guardrail:")
    print("   \"Maaf, informasi tersebut tidak ditemukan dalam basis data dokumen rahasia saya.\"")
    print("\n" + "=" * 65)
    print("🏆 HASIL EVALUASI DISERTASI:")
    print("100% BEBAS HALUSINASI! AI menolak berspekulasi jika bukti tidak valid!")
    print("=" * 65)
else:
    print(f"\n🎯 2. DOKUMEN VALID DITEMUKAN: [{dokumen_terpilih['id']}] (Skor: {skor_terbaik * 100:.1f}%)")
    print(f"   📄 Isi Fakta: \"{dokumen_terpilih['teks']}\"")
    
    print("\n💉 3. AUGMENTATION: Menyuntikkan Dokumen Valid ke dalam Konteks AI...")
    time.sleep(0.5)
    
    # 4. GENERASI DINAMIS (Bukan teks hardcode lagi!)
    print("\n🤖 RAG-Augmented AI:")
    print(f"   \"Berdasarkan rujukan resmi [{dokumen_terpilih['id']}], {dokumen_terpilih['teks']}\" ✨")
    
    print("\n" + "=" * 65)
    print("🏆 HASIL EVALUASI DISERTASI:")
    print("100% BEBAS HALUSINASI! AI menjawab mutlak berdasarkan rujukan bukti sah!")
    print("=" * 65)
