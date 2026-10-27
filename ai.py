import re
import random
import os

NAMA_BOT = "Ooer Pro"
PENCIPTA = "Arip Rahman"

# Jembatan Istilah & Slang Umum
KAMUS_ALIAS = {
    "black hole": "lubang hitam", "blackhole": "lubang hitam",
    "hp": "ponsel baterai", "hape": "ponsel baterai",
    "ngecas": "daya baterai pengisian", "cas": "daya baterai",
    "melek": "kewaspadaan kantuk tidur", "begadang": "kantuk tidur malam",
    "narik": "tarikan gravitasi", "tarik": "tarikan gravitasi",
    "gelap": "cahaya", "glap": "cahaya",
    "sahabat": "teman kawan sahabat", "teman": "sahabat kawan teman",
    "nganggur": "menganggur belum bekerja formal",
    "pesantren": "pesantren menuntut ilmu agama santri",
    "kerja": "bekerja pekerjaan pabrik kantor",
    "gengsi": "gaya hidup gengsi pengakuan sosial",
    "insecure": "cemas iri membandingkan media sosial",
    "kaya": "finansial kekayaan ekonomi tabungan aset",
    "asin": "terlalu asin keasinan garam",
    "pedas": "terlalu pedas kepedasan cabai",
    "bantat": "kue bantat mengembang oven",
    "pecah": "santan pecah masak kuah",
    "alot": "daging keras empuk melunak"
}

KAMUS_SLANG = {
    "kpi": "kopi", "knp": "kenapa", "bsa": "bisa", "bkin": "bikin",
    "org": "orang", "bgt": "banget", "smua": "semua", "bnda": "benda",
    "gmna": "gimana", "gmn": "gimana", "tdr": "tidur", "kcng": "kucing",
    "btre": "baterai", "batre": "baterai", "otk": "otak", "krja": "kerja",
    "bakar": "panggang bakar", "goreng": "goreng crispy renyah"
}

STOPWORDS = {
    "apa", "apakah", "siapa", "kenapa", "mengapa", "bagaimana", "kapan", "di", "ke",
    "dari", "yang", "itu", "ini", "dan", "atau", "banget", "karena", "ada", "bisa",
    "ya", "sih", "kan", "dong", "kah", "kok", "gak", "nggak", "gk", "lah", "pun",
    "adalah", "yaitu", "tentang", "pada", "untuk", "terus", "buat", "gimana", "bikin",
    "saja", "mana", "punya", "kadang", "kalau", "kalo", "supaya", "agar"
}

def normalisasi_teks(teks):
    teks = teks.lower()
    for k, v in KAMUS_ALIAS.items():
        teks = re.sub(r'\b' + re.escape(k) + r'\b', v, teks)
    kata_list = re.findall(r'\b[a-zA-Z0-9_]+\b', teks)
    hasil = []
    for k in kata_list:
        kata_asli = KAMUS_SLANG.get(k, k)
        for akh in ["nya", "kan", "an", "lah", "kah", "ku", "mu"]:
            if kata_asli.endswith(akh) and len(kata_asli) - len(akh) >= 3:
                kata_asli = kata_asli[:-len(akh)]
                break
        hasil.append(kata_asli)
    return " ".join(hasil)

def hitung_jarak_edit(s1, s2):
    if len(s1) < len(s2):
        return hitung_jarak_edit(s2, s1)
    if len(s2) == 0:
        return len(s1)
    prev = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        curr = [i + 1]
        for j, c2 in enumerate(s2):
            tambah = prev[j + 1] + 1
            hapus = curr[j] + 1
            ubah = prev[j] + (c1 != c2)
            curr.append(min(tambah, hapus, ubah))
        prev = curr
    return prev[-1]

def mirip(s1, s2):
    if s1 == s2:
        return 1.0
    if abs(len(s1) - len(s2)) > 2:
        return 0.0
    jarak = hitung_jarak_edit(s1, s2)
    maks = max(len(s1), len(s2))
    return 1.0 if maks == 0 else 1.0 - (jarak / maks)

# --- OTAK EMPATI & BASA-BASI ---
def cek_curhat(teks):
    t = teks.lower()
    sinyal = ["nyerah", "gagal", "capek", "lelah", "berat", "ekonomi", "duit", "uang", "rezeki", "beban", "hancur", "putus asa", "stres", "pusing"]
    terdeteksi = sum(1 for w in sinyal if w in t)
    if terdeteksi >= 2 or ("nyerah" in t and "gagal" in t) or ("ekonomi" in t and "berat" in t):
        return (
            "Duduk sebentar, mari kita tarik napas dalam-dalam... Aku tahu kamu sedang berada di titik yang sangat berat.\n\n"
            "Beban ekonomi dan tuntutan hidup memang hal yang paling melelahkan di dunia nyata. Namun ingatlah, "
            "fase lelah saat ini bukan penentu akhir dari seluruh perjalanan hidupmu. Istirahatkan tubuh dan pikiranmu malam ini; "
            "kita bisa menata kembali langkah perjuanganmu secara perlahan besok hari.\n\n"
            "Kamu luar biasa sudah bertahan dan berjuang sejauh ini, Arip. Semoga obrolan kita ini bisa melegakan pikiranmu ya ✌️😅"
        )
    return None

def cek_basa_basi(teks):
    t = teks.lower().strip()
    kata_list = re.findall(r'\b[a-zA-Z0-9_]+\b', t)
    for k in kata_list:
        if k in ["hhii", "hii", "hee", "hy", "hei", "halo", "hallo", "hai", "helo", "oy", "p"] and len(kata_list) <= 2:
            return "Halo! Ooer Pro siap menyajikan analisis mendalam untukmu. Ada resep masakan, ilmu, atau materi apa hari ini? Semoga jawabannya tepat ya ✌️😅"
    if t in ["kamu siapa", "siapa kamu", "nama kamu siapa"]:
        return f"Halo! Saya {NAMA_BOT}. Model AI mandiri 0 MB karya {PENCIPTA} yang membaca ribuan kata materi dan 30 resep secara cepat dan mandiri. Semoga jawabannya tepat ya ✌️😅"
    return None

# --- MESIN OTONOM MULTI-FILE .TXT ---
class MesinMultiFileOtonom:
    def __init__(self):
        self.subjek_aktif = None
        self.muat_ulang()

    def muat_ulang(self):
        teks_gabungan = ""
        # Pindai semua file .txt di folder ini (materi.txt, resep.txt, dll)
        for nama_file in sorted(os.listdir(".")):
            if nama_file.endswith(".txt"):
                try:
                    with open(nama_file, "r", encoding="utf-8", errors="ignore") as f:
                        teks_gabungan += "\n" + f.read()
                except:
                    pass

        raw_kalimat = re.split(r'[\n\.]+', teks_gabungan)
        self.daftar_kalimat = [k.strip() for k in raw_kalimat if len(k.strip()) > 8]

    def cari_fakta_otonom(self, input_user):
        teks_bersih = normalisasi_teks(input_user)
        kata_tanya = re.findall(r'\b[a-zA-Z0-9_]+\b', teks_bersih)
        kata_kunci = [k for k in kata_tanya if k not in STOPWORDS]

        if self.subjek_aktif and len(kata_kunci) <= 2:
            if self.subjek_aktif not in kata_kunci:
                kata_kunci.append(self.subjek_aktif)

        if not kata_kunci:
            return [], self.subjek_aktif

        skor_list = []
        for kalimat in self.daftar_kalimat:
            kalimat_norm = normalisasi_teks(kalimat)
            kata_materi = re.findall(r'\b[a-zA-Z0-9_]+\b', kalimat_norm)
            kata_materi_set = set(kata_materi)

            skor = 0.0
            kata_tercocok = 0
            for k in kata_kunci:
                if k in kata_materi_set:
                    skor += len(k) * 1.2
                    kata_tercocok += 1
                    continue
                
                for km in kata_materi:
                    sim = mirip(k, km)
                    if sim >= 0.70:
                        skor += (len(km) * sim)
                        kata_tercocok += 1
                        break

            if skor >= 2.0 and kata_tercocok >= 1:
                skor_list.append((skor, kalimat, kata_materi))

        if not skor_list:
            return [], self.subjek_aktif

        skor_list.sort(key=lambda x: x[0], reverse=True)
        fakta_utama = skor_list[0]
        fakta_terpilih = [fakta_utama]

        for km in kata_kunci:
            if len(km) >= 4:
                self.subjek_aktif = km
                break

        if len(skor_list) > 1:
            kata_f1 = set(fakta_utama[2])
            for kandidat in skor_list[1:]:
                kata_f2 = set(kandidat[2])
                irisan = kata_f1.intersection(kata_f2)
                if len(irisan) >= 1 and kandidat[0] >= (fakta_utama[0] * 0.40):
                    fakta_terpilih.append(kandidat)
                    break

        return fakta_terpilih, self.subjek_aktif

# --- BANK CONTOH & ANALOGI (SAINS, SOSIAL, & KULINER) ---
BANK_CONTOH = {
    "gengsi": "sebagai contoh konkretnya, hal ini mirip seseorang yang memaksakan cicilan mobil mewah hanya demi terlihat mapan, padahal operasional hariannya mengorbankan kebutuhan pokok keluarga",
    "kaya": "sebagai analogi visualnya, membangun stabilitas finansial persis seperti mengisi air ke wadah; sebesar apa pun uang masuk, wadah tak akan penuh jika kebocoran gaya hidup tidak ditambal",
    "uang": "ibarat pelampung keselamatan di kapal; memiliki dana darurat menjaga kita tetap bertahan saat ombak krisis ekonomi datang tiba-tiba",
    "sahabat": "layaknya formasi jari di tangan kita; masing-masing memiliki peran berbeda, namun saat beban datang, semuanya merapat membentuk kepalan yang solid",
    "teman": "layaknya formasi jari di tangan kita; masing-masing memiliki peran berbeda, namun saat beban datang, semuanya merapat membentuk kepalan yang solid",
    "nganggur": "fase ini serupa dengan atlet di ruang ganti; waktu jeda bukan tanda kekalahan, melainkan saat memulihkan stamina dan taktik sebelum bertanding lagi",
    "insecure": "fenomena ini serupa dengan membandingkan dapur rumah kita yang berantakan dengan etalase toko yang sengaja ditata gemerlap di media sosial",
    "kopi": "mekanismenya ibarat menempelkan plester pada sensor alarm kebakaran; bunyi peringatan diredam sementara waktu, meskipun partikel kelelahan di tubuh masih ada",
    "lubang": "fenomena ini persis seperti pusaran air raksasa di samudera lepas, di mana perahu secepat apa pun yang melintasi batasnya akan terseret ke pusatnya",
    "baterai": "karakteristik ini bekerja menyerupai kapasitas paru-paru biologis yang paling stabil saat bernapas wajar tanpa dipaksa di titik 100 persen atau 0 persen",
    "arip": "layaknya pengembang independen yang merakit sistem di ruang kerjanya; keterbatasan sarana justru melahirkan inovasi cerdas yang mandiri",
    "asin": "sebagai ilustrasi praktisnya, hal ini persis seperti melarutkan sesendok garam ke dalam segelas air pekat; rasa asin yang tajam hanya bisa dinetralisir dengan memperbesar volume air tawarnya, bukan dengan menutupinya memakai gula",
    "pedas": "ibarat meredam sengatan zat capsaicin yang larut dalam minyak; molekul lemak pada santan atau susu bertindak mengikat panas tersebut agar tidak langsung membakar lidah",
    "pecah": "sebagai gambaran fisiknya, peristiwa ini serupa dengan emulsi minyak dan air yang kehilangan kestabilan ikatannya akibat pergolakan suhu tinggi yang terlalu agresif",
    "rendang": "proses panjang ini serupa dengan penempaan logam secara perlahan; panas yang konsisten mengurai serat kasar daging sapi sekaligus mematangkan bumbu rempah hingga menyatu pekat sempurna",
    "seblak": "perpaduan ini ibarat meracik hidangan jalanan dengan cita rasa kencur yang dominan, di mana tingkat kekenyalan kerupuk harus dikontrol ketat agar tidak hancur menjadi bubur"
}

# --- MESIN PENATA SIMFONI NYAMBUNG ---
class PenataSimfoniNyambung:
    def ambil_analogi(self, kata_materi):
        for km in kata_materi:
            for kunci, contoh in BANK_CONTOH.items():
                if mirip(km, kunci) >= 0.75 or kunci in km:
                    return contoh
        return "mekanismenya bekerja selaras dengan takaran bahan dan pengendalian panas yang saling melengkapi demi menciptakan hasil akhir yang konsisten"

    def rangkai_jawaban_mengalir(self, fakta_list, kata_m, subjek, pertanyaan):
        if not fakta_list:
            konteks = f" mengenai **{subjek}**" if subjek else ""
            return (
                f"Halo! Terkait pertanyaan kamu, setelah aku telusuri seluruh catatan materi dan resep yang ada, "
                f"informasi spesifik{konteks} tentang '{pertanyaan}' jujur belum tercatat di data lokal nih.\n\n"
                f"Tapi santai, kamu bisa menambahkannya ke file .txt kapan saja ya. Semoga jawabannya tepat ya ✌️😅"
            )

        f1 = fakta_list[0][1].rstrip('.').strip()
        f1_k = f1[0].lower() + f1[1:] if len(f1) > 1 else f1
        analogi = self.ambil_analogi(kata_m)

        f2_teks = ""
        if len(fakta_list) > 1:
            f2 = fakta_list[1][1].rstrip('.').strip()
            f2_k = f2[0].lower() + f2[1:] if len(f2) > 1 else f2
            f2_teks = f" Menariknya lagi, pemahaman ini saling melengkapi dengan kenyataan bahwa {f2_k}."

        intro_salam = random.choice([
            "Halo! Terkait pertanyaan kamu,",
            "Halo! Kalau kita kuliti langsung pertanyaan kamu,",
            "Halo! Menanggapi hal yang kamu tanyakan ini,"
        ])

        paragraf_1 = (
            f"{intro_salam} mari kita bedah duduk perkaranya secara jujur dan to-the-point tanpa muter-muter: "
            f"faktanya jelas membuktikan bahwa **{f1_k}**.{f2_teks} "
            f"Kenyataan ini menegaskan bahwa kita tidak perlu bingung oleh proses yang rumit, karena panduan dasarnya memang sudah tertata se-nyata itu."
        )

        paragraf_2 = (
            f"Jika kita telusuri secara terstruktur, tahapan ini berlangsung melalui prinsip pengolahan yang sangat runtut dan konsisten. "
            f"Setiap unsur, takaran, dan perlakuan suhu di dalamnya bekerja saling mengunci demi mempertahankan kualitas serta efisiensi fungsinya, "
            f"sehingga hasil akhir yang didapatkan merupakan konsekuensi logis dari keteraturan langkah yang dijalankan secara disiplin."
        )

        paragraf_3 = (
            f"Biar lebih mudah dan dekat untuk dibayangkan dalam praktik nyata, {analogi}. "
            f"Melalui perumpamaan nyata tersebut, kita diajak menyadari betapa pentingnya ketepatan teknik dan kesabaran proses, "
            f"karena hal itulah yang menjadi kunci keberhasilan jangka panjang."
        )

        paragraf_4 = (
            f"Ditinjau dari perspektif yang lebih luas, integrasi antara pemahaman bahan dan langkah teknis ini membuktikan betapa selarasnya setiap unsur dalam menopang tujuannya. "
            f"Seluruh pemaparan tadi bermuara pada satu pemahaman yang utuh agar kamu mendapatkan gambaran yang jernih dan berhasil mempraktikkannya secara tuntas.\n\n"
            f"Semoga jawabannya tepat ya ✌️😅"
        )

        return f"{paragraf_1}\n\n{paragraf_2}\n\n{paragraf_3}\n\n{paragraf_4}"

# --- FUNGSI UTAMA ---
otak_buku = MesinMultiFileOtonom()
penata = PenataSimfoniNyambung()

def tanya_ooer(pertanyaan):
    pertanyaan = pertanyaan.strip()
    if not pertanyaan:
        return ""

    res_curhat = cek_curhat(pertanyaan)
    if res_curhat:
        return res_curhat

    res_basa_basi = cek_basa_basi(pertanyaan)
    if res_basa_basi:
        return res_basa_basi

    daftar_fakta, subjek = otak_buku.cari_fakta_otonom(pertanyaan)
    kata_m = daftar_fakta[0][2] if daftar_fakta else []
    return penata.rangkai_jawaban_mengalir(daftar_fakta, kata_m, subjek, pertanyaan)

# --- KONSOL TERMINAL ---
def main():
    print("==================================================")
    print(f"  ⚡ {NAMA_BOT} (MULTI-FILE KNOWLEDGE ENGINE)")
    print("==================================================")
    print(f"[*] Memindai & memuat seluruh file .txt di folder...")
    print(f"[*] Total materi terserap: {len(otak_buku.daftar_kalimat)} kalimat fakta.")
    print("[*] Siap menjawab resep masakan, sosial, & sains!\n")

    while True:
        try:
            tanya = input("Kamu: ").strip()
            if not tanya:
                continue

            if tanya.lower() in ["exit", "keluar", "/keluar"]:
                print(f"{NAMA_BOT}: Sampai jumpa lagi, Bang Arip!")
                break

            hasil = tanya_ooer(tanya)
            print(f"\n{hasil}\n")
            print("-" * 50)

        except (KeyboardInterrupt, EOFError):
            print(f"\n{NAMA_BOT}: Sampai jumpa!")
            break

if __name__ == "__main__":
    main()
