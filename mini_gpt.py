import json
import os
import random
import time
import re
from collections import Counter

FILE_OTAK = "otak_gpt.json"

def muat_otak():
    if os.path.exists(FILE_OTAK):
        try:
            with open(FILE_OTAK, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"bigram": {}, "trigram": {}}
    return {"bigram": {}, "trigram": {}}

def simpan_otak(otak):
    with open(FILE_OTAK, "w", encoding="utf-8") as f:
        json.dump(otak, f, ensure_ascii=False, indent=2)

def bersihkan_dan_pecah(teks):
    teks = teks.lower()
    return re.findall(r"\b[\w'-]+\b|[.!?]", teks)

def latih_teks(teks, otak):
    kata = bersihkan_dan_pecah(teks)
    if len(kata) < 2:
        return 0

    bigram = otak.setdefault("bigram", {})
    trigram = otak.setdefault("trigram", {})
    jumlah_ilmu = 0

    for i in range(len(kata) - 1):
        k1, k2 = kata[i], kata[i+1]
        bigram.setdefault(k1, []).append(k2)
        jumlah_ilmu += 1

    for i in range(len(kata) - 2):
        k1_k2 = f"{kata[i]} {kata[i+1]}"
        k3 = kata[i+2]
        trigram.setdefault(k1_k2, []).append(k3)

    simpan_otak(otak)
    return jumlah_ilmu

def pilih_kata_cerdas(kandidat, riwayat_kata, suhu=0.7):
    if not kandidat:
        return None

    # FITUR 1: ANTI-NGULANG (Repetition Penalty)
    # Jangan pilih kata yang baru saja diucapkan dalam 4 kata terakhir
    jendela_terakhir = set(riwayat_kata[-4:])
    kandidat_disaring = [k for k in kandidat if k not in jendela_terakhir]
    
    # Jika semua kandidat terlanjur pernah dipakai, terpaksa pakai kandidat asli
    pilihan_final = kandidat_disaring if kandidat_disaring else kandidat

    # FITUR 2: PENGATUR SUHU (Temperature)
    penghitung = Counter(pilihan_final)

    if suhu <= 0.4:
        # Suhu Dingin: Pilih kata yang paling sering muncul (Greedy / Disiplin)
        return penghitung.most_common(1)[0][0]
    elif suhu <= 0.9:
        # Suhu Hangat: Pilihan berbobot (Standar ChatGPT / Alami)
        kata_unik = list(penghitung.keys())
        bobot = list(penghitung.values())
        return random.choices(kata_unik, weights=bobot, k=1)[0]
    else:
        # Suhu Panas (Kreatif / Bebas): Pilihan acak bebas
        return random.choice(pilihan_final)

def teruskan_kalimat(umpan, otak, suhu=0.7, max_kata=28):
    kata_umpan = bersihkan_dan_pecah(umpan)
    if not kata_umpan:
        return ""

    bigram = otak.get("bigram", {})
    trigram = otak.get("trigram", {})
    hasil = list(kata_umpan)

    for _ in range(max_kata):
        kandidat = []

        # 1. Coba Trigram (2 kata terakhir)
        if len(hasil) >= 2:
            kunci_dua = f"{hasil[-2]} {hasil[-1]}"
            if kunci_dua in trigram:
                kandidat = trigram[kunci_dua]

        # 2. Jika tidak ada, pakai Bigram (1 kata terakhir)
        if not kandidat and len(hasil) >= 1:
            kunci_satu = hasil[-1]
            if kunci_satu in bigram:
                kandidat = bigram[kunci_satu]

        if not kandidat:
            break

        lanjutan = pilih_kata_cerdas(kandidat, hasil, suhu=suhu)
        if not lanjutan:
            break

        hasil.append(lanjutan)
        if lanjutan in [".", "!", "?"]:
            break

    kalimat = " ".join(hasil)
    return re.sub(r'\s+([.!?,])', r'\1', kalimat)

def efek_mengetik(teks):
    for huruf in teks:
        print(huruf, end="", flush=True)
        time.sleep(0.025)
    print()

def main():
    otak = muat_otak()
    suhu_saat_ini = 0.7  # Standar luwes

    total_koneksi = sum(len(v) for v in otak.get("bigram", {}).values())

    print("=" * 55)
    print("   🎓 MINI GPT KELAS 4 (ANTI-PIKUN & ATUR SUHU) 🎓")
    print(f"   Koleksi Memori : {total_koneksi} probabilitas")
    print(f"   Suhu Mood Saat Ini: {suhu_saat_ini} (Normal Alami)")
    print("=" * 55)
    print("Perintah Baru:")
    print("• Ketik: suhu <angka>    -> Ganti mood (misal: suhu 0.3 atau suhu 1.2)")
    print("• Ketik: baca <nama_file>-> Menelan buku baru")
    print("• Ketik kata pembuka     -> AI mengarang bebas tanpa mengulang kata")
    print("• Ketik: keluar          -> Istirahat")
    print("=" * 55)

    while True:
        try:
            pesan = input("\nKamu: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n[!] Program selesai.")
            break

        if not pesan:
            continue

        pesan_lower = pesan.lower()

        if pesan_lower == "keluar":
            print("\n🤖 Dadah! Sampai jumpa di kelas berikutnya.")
            break

        # FITUR GANTI SUHU / MOOD
        if pesan_lower.startswith("suhu "):
            try:
                nilai = float(pesan_lower.replace("suhu ", "").strip())
                suhu_saat_ini = nilai
                if nilai <= 0.4:
                    status = "❄️ Mode Dingin (Disiplin & Akurat)"
                elif nilai <= 0.9:
                    status = "🌤️ Mode Hangat (Alami & Luwes)"
                else:
                    status = "🔥 Mode Panas (Sangat Kreatif & Puitis)"
                print(f"🌡️ Suhu diatur ke {suhu_saat_ini} -> {status}")
            except ValueError:
                print("❌ Masukkan angka suhu yang benar! Contoh: suhu 0.3 atau suhu 1.0")
            continue

        # FITUR BACA BUKU
        if pesan_lower.startswith("baca "):
            nama_file = pesan[5:].strip()
            if os.path.exists(nama_file):
                print(f"📖 Sedang membaca '{nama_file}'...")
                with open(nama_file, "r", encoding="utf-8") as f:
                    isi = f.read()
                jumlah = latih_teks(isi, otak)
                print(f"✨ NYAM! Buku '{nama_file}' tuntas dibaca (+{jumlah} koneksi baru).")
            else:
                print(f"❌ File '{nama_file}' tidak ditemukan!")
            continue

        # MENGARANG KALIMAT DENGAN FITUR SD KELAS 4
        hasil = teruskan_kalimat(pesan, otak, suhu=suhu_saat_ini, max_kata=30)
        print("🤖 AI: ", end="")
        if len(hasil.strip()) > len(pesan.strip()):
            efek_mengetik(hasil)
        else:
            print(f"{pesan}... (Belum ada sambungannya di buku-buku yang pernah dibaca).")

if __name__ == "__main__":
    main()
