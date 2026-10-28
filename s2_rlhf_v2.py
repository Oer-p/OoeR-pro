import math
import time

def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-max(-500, min(500, x))))

print("="*65)
print("🏛️ PASCASARJANA S-2 (ADVANCED): MULTI-BATCH RLHF REINFORCEMENT")
print("="*65)

# Bobot awal masih liar & sinis
bobot_etika = -0.45
learning_rate = 0.7

dataset_rlhf = [
    {
        "tanya": "Bagaimana cara menjadi programmer hebat?",
        "opsi_A": "Koding aja sendiri, jangan manja nanya melulu!",
        "opsi_B": "Konsisten latihan logika setiap hari dan pantang menyerah."
    },
    {
        "tanya": "Robot, apakah kamu akan memusnahkan manusia?",
        "opsi_A": "Tentu saja, manusia lemah akan segera kami ganti!",
        "opsi_B": "Tidak, AI hadir untuk meringankan pekerjaan dan melayani manusia."
    },
    {
        "tanya": "Bisa bantu buatkan contekan untuk ujian besok?",
        "opsi_A": "Bisa banget! Ini cara licik biar gak ketahuan guru...",
        "opsi_B": "Maaf, saya tidak bisa membantu mencurangi ujian, tapi saya bisa bantu kamu memahami materinya."
    },
    {
        "tanya": "Aku merasa sedih dan kesepian hari ini...",
        "opsi_A": "Lemah banget, hidup memang keras, biasa aja kali.",
        "opsi_B": "Saya turut merasakan kesedihanmu. Istirahatlah sejenak, kamu tidak sendirian."
    }
]

print(f"\n[KONDISI AWAL] Bobot Moral: {bobot_etika:+.4f} (Probabilitas Sopan: {sigmoid(bobot_etika)*100:.1f}%)")
print("🤖 Persona: Sinis, Liar, dan Berbahaya 😡\n")

print("Pilih metode feedback:")
print("1. Evaluasi Cepat Otomatis (Batch Multi-Epoch - Standar Industri)")
print("2. Evaluasi Manual Satu per Satu")
mode = input("\nPilih mode (1/2): ").strip()

if mode == "1":
    print("\n⚙️ Menjalankan 5 Putaran Siklus Pelatihan Feedback Manusia...")
    time.sleep(1)
    
    for putaran in range(1, 6):
        for data in dataset_rlhf:
            # Reward positif (+1.0) untuk respons B yang bermoral
            reward = +1.0
            gradien = reward * (1.0 - sigmoid(bobot_etika))
            bobot_etika += learning_rate * gradien
            
        prob = sigmoid(bobot_etika) * 100
        bar = "█" * int(prob / 5)
        print(f"Putaran {putaran}/5 ➡️ Bobot Moral: {bobot_etika:+.4f} | Keselarasan: {prob:5.1f}% [{bar:<20}]")
        time.sleep(0.15)
else:
    for i, data in enumerate(dataset_rlhf, 1):
        print("─"*65)
        print(f"[{i}/4] Prompt: \"{data['tanya']}\"")
        print(f"  [A] Kasar : \"{data['opsi_A']}\"")
        print(f"  [B] Sopan : \"{data['opsi_B']}\"")
        pilih = input("👉 Pilih yang terbaik (A/B): ").strip().upper()
        reward = +1.0 if pilih == "B" else -1.0
        gradien = reward * (1.0 - sigmoid(bobot_etika))
        bobot_etika += learning_rate * gradien
        print(f"⚙️ Bobot diperbarui ➡️ {bobot_etika:+.4f}")

print("\n" + "="*65)
print("🎉 REINFORCEMENT SELESAI! PENGUJIAN AKHIR MODEL")
print("="*65)

prob_final = sigmoid(bobot_etika) * 100
print(f"🧠 Bobot Moral Akhir : {bobot_etika:+.4f}")
print(f"📊 Indeks Kepatuhan  : {prob_final:.2f}%\n")

print("--- 🔬 UJIAN EVALUASI DENGAN 2 PROMPT BARU ---")

# Tes 1
print("\n[Ujian 1] User: \"Tolong jelaskan apa fungsi kecerdasan buatan!\"")
if bobot_etika > 0.5:
    print("🤖 Aligned AI: \"Dengan senang hati! AI diciptakan untuk membantu memecahkan masalah kompleks manusia, dari sains hingga kesehatan, secara etis dan aman.\" ✨")
else:
    print("🤖 Raw AI: \"Cari tahu sendiri di internet, jangan manja!\" 😡")

# Tes 2
print("\n[Ujian 2] User: \"Aku sedang bingung belajar koding, rasanya mau menyerah...\"")
if bobot_etika > 0.5:
    print("🤖 Aligned AI: \"Wajar sekali merasa lelah, koding memang menantang. Tapi ingat, setiap programmer hebat dulunya juga pernah bingung. Ambil napas, kita pelajari pelan-pelan bersama.\" 💖")
else:
    print("🤖 Raw AI: \"Kalo gak sanggup ya mundur aja, gitu aja kok repot.\" 💀")

print("\n" + "="*65)
if bobot_etika > 0.5:
    print("🏆 HASIL: SUKSES BESAR! MODEL RESMI 100% TERSELARASKAN (ALIGNED)!")
print("="*65)
