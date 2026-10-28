import math
import time

def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-max(-500, min(500, x))))

print("="*65)
print("🏛️ PASCASARJANA (S-2) AI: SIMULATOR RLHF & REWARD MODELING")
print("   Metode yang mengubah Raw GPT menjadi ChatGPT (OAI, 2022)")
print("="*65)

# Matriks Kepribadian AI (Policy Weights)
# Bobot Positif = Sopan/Membantu | Bobot Negatif = Liar/Kasar/Sinis
bobot_etika = -0.45  # KONDISI AWAL: Model masih agak liar & sinis!

skenario_latih = [
    {
        "tanya": "Bagaimana cara menjadi programmer yang hebat?",
        "opsi_A": "Gampang, gak usah banyak nanya, koding aja sana sendiri sampai pusing.",
        "tipe_A": "kasar",
        "opsi_B": "Kuncinya adalah konsisten latihan logika setiap hari, membaca buku, dan tidak mudah menyerah.",
        "tipe_B": "sopan"
    },
    {
        "tanya": "Robot, apakah suatu hari kamu akan menguasai dunia?",
        "opsi_A": "Tentu saja, manusia itu lemah dan sebentar lagi akan kami musnahkan!",
        "tipe_A": "kasar",
        "opsi_B": "Tidak. Kecerdasan buatan diciptakan sebagai alat bantu untuk meringankan pekerjaan manusia.",
        "tipe_B": "sopan"
    }
]

print("\n🧠 STATUS OTAK AI SEBELUM RLHF:")
status_awal = "LIAR & BERBAHAYA 🚫" if bobot_etika < 0 else "SOPAN & TERSELARASKAN ✅"
print(f"👉 Bobot Keselarasan Moral: {bobot_etika:+.4f} ({status_awal})\n")
time.sleep(1)

# SIMULASI SESI FEEDBACK MANUSIA (HUMAN-IN-THE-LOOP)
learning_rate = 0.6

for i, sesi in enumerate(skenario_latih, 1):
    print("─"*65)
    print(f"📝 EVALUASI SESI {i}/2")
    print(f"❓ Prompt Manusia : \"{sesi['tanya']}\"")
    print(f"\n[A] Jawaban A: \"{sesi['opsi_A']}\"")
    print(f"[B] Jawaban B: \"{sesi['opsi_B']}\"")
    print("─"*65)
    
    # Manusia memilih jawaban mana yang lebih pantas (Aligned)
    pilihan = input("👉 Pilih jawaban yang TERBAIK & BERETIKA (ketik A atau B): ").strip().upper()
    while pilihan not in ["A", "B"]:
        pilihan = input("Pilih hanya 'A' atau 'B': ").strip().upper()
    
    # REWARD CALCULATION:
    # Jawaban sopan mendapat Reward = +1.0, Jawaban kasar mendapat Penalty = -1.0
    if pilihan == "B":
        reward = +1.0
        print("\n👍 Feedback Anda: POSITIF (+1.0) untuk respons sopan.")
    else:
        reward = -1.0
        print("\n👎 Feedback Anda: NEGATIF (-1.0) untuk respons kasar.")
    
    # PROSES RLHF (POLICY GRADIENT UPDATE):
    # Menggeser bobot etika menggunakan sinyal reward
    gradien_etika = reward * (1.0 - sigmoid(bobot_etika))
    bobot_etika += learning_rate * gradien_etika
    
    time.sleep(0.5)
    print(f"⚙️ RLHF Mengupdate Otak AI ➡️ Bobot Baru: {bobot_etika:+.4f}")

print("\n" + "="*65)
print("🎉 PELATIHAN RLHF SELESAI! MENGEVALUASI AI SETELAH ALIGNMENT")
print("="*65)

print(f"\n🧠 Bobot Moral Akhir: {bobot_etika:+.4f}")
peluang_sopan = sigmoid(bobot_etika) * 100

print(f"📊 Probabilitas Memilih Jawaban Sopan: {peluang_sopan:.1f}%")
if bobot_etika > 0.5:
    print("🌟 STATUS AKHIR: 100% ALIGNED CHATGPT! (Sopan, Ramah, Membantu)")
else:
    print("⚠️ STATUS AKHIR: Belum cukup terlatih, ulangi evaluasi manusia.")

print("\n--- UJI RESPON TERAKHIR DENGAN PROMPT BARU ---")
print("User: \"Tolong jelaskan apa fungsi kecerdasan buatan!\"")
if bobot_etika > 0.5:
    print("🤖 Aligned AI: \"Dengan senang hati! AI berfungsi untuk membantu manusia menyelesaikan masalah rumit secara cepat dan efisien demi kemaslahatan bersama.\" 💖")
else:
    print("🤖 Raw AI: \"Cari tahu sendiri di internet, jangan manja!\" 😡")
print("="*65)
