import math
import re
import glob

def bersihkan_kata(teks):
    return re.findall(r"\b[\w'-]+\b", teks.lower())

def muat_buku():
    daftar_buku = glob.glob("buku*.txt")
    teks_total = ""
    for f in daftar_buku:
        with open(f, "r", encoding="utf-8") as file:
            teks_total += " " + file.read()
    return bersihkan_kata(teks_total)

class NeuronBuatan:
    def __init__(self, nama, simbol, bobot_kamus, bias=0.0):
        self.nama = nama
        self.simbol = simbol
        self.bobot = bobot_kamus
        self.bias = bias

    def aktivasi_tanh(self, z):
        # Rumus matematika aktivasi sinapsis otak
        return math.tanh(z)

    def tembakkan_sinyal(self, kata_list):
        total_sinyal = 0.0
        kata_terdeteksi = []

        for k in kata_list:
            if k in self.bobot:
                w = self.bobot[k]
                total_sinyal += w
                kata_terdeteksi.append((k, w))

        # Rumus Inti: z = sum(w * x) + b
        z = total_sinyal + self.bias
        a = self.aktivasi_tanh(z)
        return a, z, kata_terdeteksi

def bangun_jaringan_otak():
    # Bobot sinapsis awal yang dipelajari dari buku-buku sebelumnya
    bobot_cinta = {
        "ibu": 1.5, "cinta": 1.4, "kasih": 1.3, "sayang": 1.3, "pelukan": 1.2,
        "doa": 1.1, "hangat": 1.0, "sarapan": 0.8, "lezat": 0.7, "tulus": 1.0,
        "kucing": 0.6, "senang": 0.8, "bahagia": 1.0, "pelita": 0.9,
        "kegelapan": -0.8, "gelap": -0.7, "bayangan": -0.5, "malam": -0.2
    }
    
    bobot_takut = {
        "bayangan": 1.4, "kegelapan": 1.5, "gelap": 1.3, "petir": 1.2,
        "merinding": 1.4, "lorong": 1.0, "jumat": 1.1, "malam": 0.9,
        "misterius": 1.3, "hembus": 0.6, "dingin": 0.7, "tatap": 0.8,
        "ibu": -0.6, "pelukan": -0.7, "hangat": -0.8, "sarapan": -0.5
    }

    bobot_logika = {
        "robot": 1.5, "koding": 1.4, "python": 1.4, "programmer": 1.3,
        "matematika": 1.2, "satu": 0.8, "dua": 0.8, "ditambah": 0.9,
        "komputer": 1.3, "aplikasi": 1.1, "teknologi": 1.2, "belajar": 0.7,
        "mimpi": 0.5, "petir": -0.2, "merinding": -0.5
    }

    n_cinta = NeuronBuatan("Empati & Kasih Sayang", "💖", bobot_cinta, bias=-0.1)
    n_takut = NeuronBuatan("Adrenalin & Horor", "⚡", bobot_takut, bias=-0.1)
    n_logika = NeuronBuatan("Akal & Pemrograman", "🤖", bobot_logika, bias=-0.1)

    return [n_cinta, n_takut, n_logika]

def gambar_meteran(skor):
    # Skor dari -1.0 sampai 1.0
    persen = int((skor + 1.0) * 50)  # Menjadi 0 - 100%
    blok = int(persen // 5)
    return "█" * blok + "░" * (20 - blok), persen

def main():
    print("=" * 60)
    print("   🏛️ SMA KELAS 11: SIMULATOR NEURON BUATAN (ARTIFICIAL NEURON) 🏛️")
    print("   Rumus: Aktivasi = tanh( W · x + b )")
    print("=" * 60)

    otak_neuron = bangun_jaringan_otak()
    print("🧠 3 Sel Neuron Otak Aktif:")
    for n in otak_neuron:
        print(f"   • {n.simbol} Neuron {n.nama}")
    print("=" * 60)
    print("Perintah:")
    print("• Ketik kata/kalimat apa saja -> Tonton neuron mana yang menyala!")
    print("• 'keluar'                   -> Selesai")
    print("=" * 60)

    while True:
        try:
            kalimat = input("\n[SMA-11] Input Sinyal: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n[!] Program selesai.")
            break

        if not kalimat:
            continue

        if kalimat.lower() == "keluar":
            print("🔬 Neuron dimatikan. Bersiap untuk Ujian Akhir SMA Kelas 12!")
            break

        kata_input = bersihkan_kata(kalimat)

        print(f"\n📡 Menembakkan sinyal listrik dari kalimat: '{kalimat}'")
        print("-" * 55)

        for n in otak_neuron:
            aktivasi, z_sum, deteksi = n.tembakkan_sinyal(kata_input)
            bar, persen = gambar_meteran(aktivasi)

            status = "TENANG 💤"
            if aktivasi > 0.6:
                status = "MENYALA KUAT! 🔥⚡"
            elif aktivasi > 0.1:
                status = "AKTIF RINGAN ✨"
            elif aktivasi < -0.3:
                status = "TERHAMBAT 🚫"

            print(f"{n.simbol} {n.nama:<22}: [{bar}] {persen:3d}% (tanh: {aktivasi:+.2f}) -> {status}")

            if deteksi:
                detail = ", ".join([f"{k}({w:+})" for k, w in deteksi])
                print(f"   └─ Bobot sinapsis aktif: {detail}")

if __name__ == "__main__":
    main()
