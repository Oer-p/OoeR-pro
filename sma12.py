import math
import random
import time

def sigmoid(x):
    # Fungsi aktivasi pembatas sinyal (0.0 sampai 1.0)
    x = max(-500, min(500, x))
    return 1.0 / (1.0 + math.exp(-x))

def sigmoid_turunan(output_sigmoid):
    # Turunan kalkulus sigmoid: f'(x) = f(x) * (1 - f(x))
    return output_sigmoid * (1.0 - output_sigmoid)

print("="*62)
print("🏛️ SMA KELAS 12: NEURON MANDIRI DENGAN BACKPROPAGATION")
print("="*62)

# DATASET LATIHAN:
# Tugas Neuron: Membedakan getaran positif vs negatif
# Target 1.0 = Positif (Kasih/Kebaikan), Target 0.0 = Negatif (Horor/Bahaya)
data_latih = [
    {"kata": "cinta dan ketulusan ibu", "x": 1.0,  "target": 1.0},
    {"kata": "kegelapan bayangan hitam", "x": -1.0, "target": 0.0}
]

# 1. INISIALISASI ACAK: Neuron lahir buta huruf
random.seed(42)
bobot_w = round(random.uniform(-1.5, -0.5), 3)  # Dibuat salah/negatif dulu di awal!
bias_b  = 0.0
learning_rate = 0.8  # Langkah kaki perbaikan bobot

print(f"\n[KONDISI SAAT LAHIR (EPOCH 0)]")
print(f"🎲 Bobot Awal (W) : {bobot_w:+.4f} (NGURUS/SALAH ARAH!)")
print(f"🎯 Target         : Sinyal Positif (+1) -> 1.0 | Sinyal Negatif (-1) -> 0.0")
print("\nMemulai proses belajar mandiri menuruni lembah kesalahan...\n")
time.sleep(1.2)

# 2. PROSES BELAJAR (TRAINING LOOP - 50 KALI LATIHAN)
epochs = 50

for epoch in range(1, epochs + 1):
    total_loss = 0.0
    
    for sampel in data_latih:
        x = sampel["x"]
        target = sampel["target"]
        
        # [A] FORWARD PASS (Tebak)
        z = (bobot_w * x) + bias_b
        prediksi = sigmoid(z)
        
        # [B] LOSS FUNCTION (Ukur Kesalahan)
        error = target - prediksi
        loss = 0.5 * (error ** 2)
        total_loss += loss
        
        # [C] BACKPROPAGATION (Kalkulus Turunan Rantai)
        # Mencari seberapa besar pengaruh W terhadap error
        delta = error * sigmoid_turunan(prediksi)
        gradien_w = delta * x
        gradien_b = delta * 1.0
        
        # [D] GRADIENT DESCENT (Koreksi Bobot)
        bobot_w += learning_rate * gradien_w
        bias_b  += learning_rate * gradien_b
    
    # Visualisasi progress penurunan loss
    if epoch == 1 or epoch % 5 == 0:
        panjang_bar = int(total_loss * 30)
        grafik = "█" * max(1, panjang_bar)
        print(f"Epoch {epoch:02d}/50 | Loss: {total_loss:.5f} | W: {bobot_w:+.4f} | B: {bias_b:+.4f} | [{grafik:<15}]")
        time.sleep(0.08)

print("\n" + "="*62)
print("🎉 PROSES BELAJAR MANDIRI TUNTAS! NEURON SUDAH PINTAR!")
print("="*62)
print(f"🧠 Bobot Akhir: W = {bobot_w:+.4f} (Otomatis Berubah Positif!)")

print("\n--- 📝 HASIL UJIAN AKHIR KELAS 12 (EVALUASI) ---")
for sampel in data_latih:
    z = (bobot_w * sampel["x"]) + bias_b
    prediksi = sigmoid(z)
    persen = prediksi * 100
    status = "LULUS (100% AKURAT)" if (sampel["target"] == 1.0 and prediksi > 0.85) or (sampel["target"] == 0.0 and prediksi < 0.15) else "BELUM LULUS"
    print(f"Input : '{sampel['kata']}'")
    print(f"Hasil : Tebakan Neuron = {persen:.2f}% | Target Asli = {sampel['target']} ➡️ [{status}]\n")

print("="*62)
