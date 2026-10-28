import json
import os
import difflib

FOLDER_SKRIP = os.path.dirname(os.path.abspath(__file__))
FILE_OTAK = os.path.join(FOLDER_SKRIP, "otak_bayi.json")

def muat_otak():
    if os.path.exists(FILE_OTAK):
        try:
            with open(FILE_OTAK, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def simpan_otak_permanen(memori):
    with open(FILE_OTAK, "w", encoding="utf-8") as f:
        json.dump(memori, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())

def cari_jawaban(teks, memori):
    teks = teks.strip().lower()
    if teks in memori:
        return teks, memori[teks]
    cocok = difflib.get_close_matches(teks, memori.keys(), n=1, cutoff=0.75)
    if cocok:
        return cocok[0], memori[cocok[0]]
    return None, None

def main():
    memori = muat_otak()
    terakhir_tanya = None

    print("\n" + "=" * 48)
    print("   👶 AI BAYI (MODE CHAT BELAJAR EJAAN) 👶")
    print(f"   Memori Tersimpan: {len(memori)} hafalan")
    print("   Tips:")
    print("   • Ketik 'status' untuk melihat isi otak")
    print("   • Ketik 'salah' jika jawaban bayi keliru")
    print("   • Ketik 'keluar' untuk selesai")
    print("=" * 48)

    while True:
        try:
            pesan = input("\nKamu: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n[!] Latihan selesai. Otak tersimpan aman.")
            break

        if not pesan:
            continue

        pesan_bersih = pesan.lower()

        if pesan_bersih == "keluar":
            print("\n👶 Bayi: Dadah! Nanti ajari aku lagi ya.")
            break

        if pesan_bersih == "status":
            print(f"\n🧠 Total hafalan bayi: {len(memori)} pengetahuan.")
            for k in list(memori.keys())[-5:]:
                print(f"   • {k} -> {memori[k]}")
            continue

        if pesan_bersih == "salah":
            if terakhir_tanya:
                beneran = input(f"   👉 Koreksi jawaban untuk '{terakhir_tanya}': ").strip()
                if beneran:
                    memori[terakhir_tanya] = beneran
                    simpan_otak_permanen(memori)
                    print("👶 Bayi: Okee, memorinya sudah aku ralat!")
            else:
                print("👶 Bayi: Belum ada hafalan yang mau dikoreksi.")
            continue

        kunci, jawaban = cari_jawaban(pesan_bersih, memori)

        if jawaban:
            terakhir_tanya = kunci
            print(f"👶 Bayi: {jawaban}")
        else:
            print(f"👶 Bayi: Oweee... aku belum tahu '{pesan}'.")
            bimbing = input("   👉 Ajari bayi jawab apa? (ketik '-' untuk lewati): ").strip()
            if bimbing and bimbing != "-":
                memori[pesan_bersih] = bimbing
                simpan_otak_permanen(memori)
                terakhir_tanya = pesan_bersih
                print(f"👶 Bayi: Catat permanen! Total ingatan: {len(memori)}")

if __name__ == "__main__":
    main()
