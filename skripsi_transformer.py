import math
import random
import time

def softmax(skor_list):
    exp_list = [math.exp(max(-500, min(500, s))) for s in skor_list]
    total = sum(exp_list)
    return [s / total for s in exp_list]

def dot_product(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))

print("="*65)
print("🎓 SIDANG SKRIPSI: MINI GENERATIVE TRANSFORMER (GPT DECODER)")
print("   Menggabungkan: Embedding + Causal Masking + Self-Attention")
print("="*65)

# 1. KOSAKATA & VEKTOR RUANG MAKNA (Dimensi: [Teknologi, Cinta/Kasih, Aksi])
vektor_makna = {
    "budi":       [0.2, 0.4, 0.5],
    "membuat":    [0.6, 0.1, 0.9],
    "robot":      [0.9, 0.1, 0.4],
    "cerdas":     [0.8, 0.3, 0.3],
    "untuk":      [0.1, 0.3, 0.4],
    "membantu":   [0.3, 0.9, 0.8],
    "ibu":        [0.1, 0.95, 0.3],
    "tersenyum":  [0.2, 0.9, 0.4],
    "bahagia":    [0.1, 0.95, 0.2]
}

vocab = list(vektor_makna.keys())

def generate_transformer(prompt_awal, target_kata_tambah=4, suhu=0.7):
    kalimat = prompt_awal.strip().split()
    print(f"\n🚀 PROMPT AWAL: \"{' '.join(kalimat)}\"")
    print("🧠 Transformer sedang berpikir dengan Causal Self-Attention...\n")
    time.sleep(1)
    
    for langkah in range(target_kata_tambah):
        n = len(kalimat)
        kata_terakhir = kalimat[-1]
        
        # Ambil Query (Q) dari kata terakhir yang sedang ditulis
        q = vektor_makna.get(kata_terakhir, [0.1, 0.1, 0.1])
        d_k = len(q)
        
        # --- CAUSAL SELF-ATTENTION DENGAN TOPENG MASA DEPAN (MASKING) ---
        skor_raw = []
        for i, kata in enumerate(kalimat):
            # Posisi kata hanya boleh memperhatikan dirinya dan kata sebelumnya!
            k = vektor_makna.get(kata, [0.1, 0.1, 0.1])
            skor = dot_product(q, k) / math.sqrt(d_k)
            skor_raw.append(skor)
        
        # Terapkan Softmax untuk menghasilkan bobot perhatian (Attention Weights)
        bobot_atensi = softmax(skor_raw)
        
        # --- PREDIKSI KATA BERIKUTNYA DARI KANDIDAT VOCABULARY ---
        # Menghitung seberapa cocok calon kata berikutnya dengan konteks perhatian
        vektor_konteks = [0.0] * d_k
        for bobot, kata in zip(bobot_atensi, kalimat):
            v = vektor_makna.get(kata, [0.1, 0.1, 0.1])
            for dim in range(d_k):
                vektor_konteks[dim] += bobot * v[dim]
        
        # Bandingkan vektor konteks dengan seluruh kata di kamus
        skor_kandidat = []
        for kata_calon in vocab:
            if kata_calon in kalimat[-2:]:  # Cegah looping kata berulang
                skor_kandidat.append(-99.0)
                continue
            v_calon = vektor_makna[kata_calon]
            skor_kandidat.append(dot_product(vektor_konteks, v_calon) / suhu)
        
        prob_kandidat = softmax(skor_kandidat)
        
        # Sampling kata berikutnya berdasarkan probabilitas
        kata_terpilih = random.choices(vocab, weights=prob_kandidat, k=1)[0]
        kalimat.append(kata_terpilih)
        
        # Visualisasikan perhatian kata baru terhadap kata-kata sebelumnya
        print(f"[{langkah+1}] Kata baru: '{kata_terpilih:<9}' | Memperhatikan: '{kata_terakhir}' ({max(bobot_atensi)*100:.1f}%)")
        time.sleep(0.4)
    
    print("\n" + "─"*65)
    print("✨ HASIL KARYA TRANSFORMER:")
    print(f"👉 \"{' '.join(kalimat)}\"")
    print("─"*65)

# UJI COBA SIDANG SKRIPSI:
generate_transformer("budi membuat robot", target_kata_tambah=4, suhu=0.5)

print("\n" + "="*65)
print("🎓 STATUS KELULUSAN: RESMI LULUS SEBAGAI SARJANA SAINS AI (S.Kom AI)!")
print("="*65)
