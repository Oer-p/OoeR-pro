import math

def softmax(skor_list):
    # Mengubah skor angka mentah menjadi persentase probabilitas (total 100%)
    exp_list = [math.exp(s) for s in skor_list]
    total_exp = sum(exp_list)
    return [s / total_exp for s in exp_list]

def dot_product(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))

print("="*65)
print("🎓 PERGURUAN TINGGI AI - SEMESTER 1: SELF-ATTENTION TRANSFORMER")
print("   Makalah Referensi: 'Attention Is All You Need' (Vaswani et al., 2017)")
print("="*65)

# KAMUS VEKTOR EMBEDDING SEDERHANA (3 Dimensi Makna: [Rasa Makanan, Militer/Kedinasan, Objek])
embeddings = {
    "budi":     [0.1, 0.0, 0.9],
    "makan":    [0.9, 0.0, 0.2],
    "buah":     [0.95, 0.0, 0.1],
    "apel":     [0.5, 0.5, 0.5], # KATA AMBIGU! Bisa buah, bisa upacara
    "manis":    [0.9, 0.0, 0.0],
    "prajurit": [0.0, 0.95, 0.8],
    "baris":    [0.0, 0.9, 0.3],
    "pagi":     [0.2, 0.5, 0.1]
}

def hitung_self_attention(kalimat):
    kata_kata = kalimat.split()
    print(f"\nKalimat Target: \"{' '.join(kata_kata)}\"")
    print(f"Menganalisis sorotan lampu panggung (Attention) untuk kata kunci: 'apel'...\n")
    
    # Ambil vektor Query (Q) dari kata 'apel'
    q_apel = embeddings["apel"]
    
    skor_perhatian = []
    d_k = len(q_apel) # Dimensi vektor (3)
    
    for kata in kata_kata:
        # Ambil vektor Key (K) dari kata lain
        k_lain = embeddings.get(kata, [0.0, 0.0, 0.0])
        
        # Rumus Sakral Attention: (Q · K) / sqrt(d_k)
        skor_mentah = dot_product(q_apel, k_lain) / math.sqrt(d_k)
        skor_perhatian.append(skor_mentah)
    
    # Normalisasi menggunakan Softmax (Menjadi Persentase 0% - 100%)
    bobot_attention = softmax(skor_perhatian)
    
    # Tampilkan Peta Perhatian (Attention Matrix)
    print("┌" + "─"*60 + "┐")
    print("│ HASIL ATTENTION WEIGHTS (KEMANAKAH KATA 'APEL' MENATAP?)   │")
    print("├" + "─"*60 + "┤")
    for kata, bobot in zip(kata_kata, bobot_attention):
        persen = bobot * 100
        panjang_bar = int(bobot * 25)
        bar = "█" * panjang_bar
        penanda = " 👈 (FOKUS UTAMA!)" if bobot == max(bobot_attention) and kata != "apel" else ""
        print(f"│ Kata: {kata:<10} ➡️ {persen:5.1f}% [{bar:<25}] {penanda}")
    print("└" + "─"*60 + "┘")

# EKSPERIMEN 1: 'apel' di dunia buah/kuliner
hitung_self_attention("budi makan buah apel manis")

# EKSPERIMEN 2: 'apel' di dunia upacara militer
hitung_self_attention("prajurit baris apel pagi")

print("\n" + "="*65)
print("💡 KESIMPULAN MAHASISWA:")
print("Kata 'apel' yang sama persis bisa otomatis 'berubah makna' karena")
print("Self-Attention mengubah arah sorotan lampunya mengikuti kata sekitarnya!")
print("="*65)
