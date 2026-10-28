import os
import re
import math
import glob

def bersihkan_teks(teks):
    teks = teks.lower()
    return re.findall(r"\b[\w'-]+\b", teks)

def muat_semua_buku():
    daftar_buku = glob.glob("buku*.txt")
    if not daftar_buku:
        return []
    semua_kata = []
    for f in sorted(daftar_buku):
        with open(f, "r", encoding="utf-8") as file:
            semua_kata.extend(bersihkan_teks(file.read()))
    return semua_kata, daftar_buku

def bangun_vektor_konteks(kata_list, jendela=3):
    kosakata = sorted(list(set(kata_list)))
    vocab_index = {k: i for i, k in enumerate(kosakata)}
    
    # Matriks Ko-okurensi (Seberapa sering dua kata muncul berdekatan)
    vektor = {k: {} for k in kosakata}
    
    for i, kata in enumerate(kata_list):
        awal = max(0, i - jendela)
        akhir = min(len(kata_list), i + jendela + 1)
        for j in range(awal, akhir):
            if i != j:
                tetangga = kata_list[j]
                vektor[kata][tetangga] = vektor[kata].get(tetangga, 0) + 1
                
    return kosakata, vektor

def hitung_kemiripan(kata1, kata2, vektor):
    if kata1 not in vektor or kata2 not in vektor:
        return 0.0
    
    v1 = vektor[kata1]
    v2 = vektor[kata2]
    
    # Dot Product
    semua_kunci = set(v1.keys()).intersection(set(v2.keys()))
    dot = sum(v1[k] * v2[k] for k in semua_kunci)
    
    norm1 = math.sqrt(sum(v ** 2 for v in v1.values()))
    norm2 = math.sqrt(sum(v ** 2 for v in v2.values()))
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot / (norm1 * norm2)

def cari_tetangga_terdekat(kata_target, kosakata, vektor, top_n=5):
    if kata_target not in vektor:
        return None
    
    skor_list = []
    for k in kosakata:
        if k != kata_target:
            skor = hitung_kemiripan(kata_target, k, vektor)
            if skor > 0:
                skor_list.append((k, skor))
                
    skor_list.sort(key=lambda x: x[1], reverse=True)
    return skor_list[:top_n]

def main():
    print("=" * 60)
    print("   🏛️ LABORATORIUM SMA KELAS 10: SISTEM VEKTOR & EMBEDDING 🏛️")
    print("   (Konsep Matriks Makna ala Bengio 2003 & Andrej Karpathy)")
    print("=" * 60)
    
    kata_list, daftar_buku = muat_semua_buku()
    if not kata_list:
        print("❌ Tidak ada file buku*.txt ditemukan!")
        return

    print(f"📚 Memindai {len(daftar_buku)} buku: {', '.join(daftar_buku)}")
    kosakata, vektor = bangun_vektor_konteks(kata_list, jendela=3)
    print(f"✨ Berhasil membangun {len(kosakata)} Vektor Koordinat Kata!")
    print("=" * 60)
    print("Perintah Eksperimen:")
    print("• 'cari <kata>'         -> Melihat kata yang satu 'frekuensi rasa'")
    print("• 'jarak <kata1> <kata2>'-> Mengukur kedekatan rasa (0% - 100%)")
    print("• 'keluar'              -> Selesai eksperimen")
    print("=" * 60)

    while True:
        try:
            cmd = input("\n[SMA-10] Lab-Vektor $ ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n[!] Eksperimen selesai.")
            break

        if not cmd:
            continue

        if cmd.lower() == "keluar":
            print("🔬 Lab ditutup. Sampai jumpa di Kelas 11!")
            break

        parts = cmd.lower().split()

        # FITUR 1: CARI KATA DENGAN RASA SERUPA
        if parts[0] == "cari" and len(parts) >= 2:
            target = parts[1]
            hasil = cari_tetangga_terdekat(target, kosakata, vektor, top_n=5)
            if hasil is None:
                print(f"❌ Kata '{target}' belum ada di database buku.")
            elif not hasil:
                print(f"🔍 Kata '{target}' berdiri sendiri (belum ada tetangga dekat).")
            else:
                print(f"🧭 5 Kata yang paling bergetar dekat dengan '{target}':")
                for rank, (k, skor) in enumerate(hasil, 1):
                    persen = skor * 100
                    bar = "█" * int(persen // 10)
                    print(f"   {rank}. {k:<15} : {persen:5.1f}% [{bar:<10}]")

        # FITUR 2: UKUR JARAK RASA 2 KATA
        elif parts[0] == "jarak" and len(parts) >= 3:
            k1, k2 = parts[1], parts[2]
            if k1 not in vektor:
                print(f"❌ Kata '{k1}' tidak dikenal.")
                continue
            if k2 not in vektor:
                print(f"❌ Kata '{k2}' tidak dikenal.")
                continue
            
            kemiripan = hitung_kemiripan(k1, k2, vektor)
            persen = kemiripan * 100
            bar = "█" * int(persen // 10)
            print(f"📐 Jarak Kesamaan Rasa antara '{k1}' dan '{k2}':")
            print(f"   Skor Kedekatan: {persen:.2f}% [{bar:<10}]")
            if persen > 50:
                print("   👉 Hubungan emosional/konteks: SANGAT DEKAT ❤️")
            elif persen > 20:
                print("   👉 Hubungan emosional/konteks: SEDANG / BERHUBUNGAN 🔗")
            else:
                print("   👉 Hubungan emosional/konteks: JAUH / BEDA DUNIA ❄️")
        else:
            print("Perintah tidak dikenal. Ketik 'cari <kata>' atau 'jarak <kata1> <kata2>'")

if __name__ == "__main__":
    main()
