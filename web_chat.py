import os
import math
import re
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

print("=" * 65)
print("🌐 MENYALAKAN SERVER WEB AI CHATBOT (0 MB PYTHON MURNI)")
print("=" * 65)

KNOWLEDGE_DIR = "knowledge"
WINDOW_SIZE = 2
OVERLAP = 1
CTO_THRESHOLD = 0.18

def bersihkan_dan_token(teks):
    return re.findall(r'\b[a-zA-Z0-9\-_]+\b', teks.lower())

def potong_menjadi_chunks(teks, window_size=WINDOW_SIZE, overlap=OVERLAP):
    kalimat = [k.strip() for k in re.split(r'(?<=[.!?])\s+', teks) if k.strip()]
    if len(kalimat) <= window_size:
        return [teks]
    chunks = []
    step = max(1, window_size - overlap)
    for i in range(0, len(kalimat), step):
        chunk = " ".join(kalimat[i:i + window_size])
        chunks.append(chunk)
        if i + window_size >= len(kalimat):
            break
    return chunks

# 1. SCAN KNOWLEDGE BASE
daftar_chunks = []
if os.path.exists(KNOWLEDGE_DIR):
    for nama_file in sorted(os.listdir(KNOWLEDGE_DIR)):
        if nama_file.endswith(".txt"):
            path = os.path.join(KNOWLEDGE_DIR, nama_file)
            with open(path, "r", encoding="utf-8") as f:
                konten = f.read().strip()
                if konten:
                    chunks = potong_menjadi_chunks(konten)
                    for idx, c in enumerate(chunks, 1):
                        daftar_chunks.append({
                            "file": nama_file,
                            "chunk_id": f"chunk-{idx}",
                            "teks": c,
                            "tokens": bersihkan_dan_token(c)
                        })

TOTAL_CHUNKS = len(daftar_chunks)
vocab_df = {}
for c in daftar_chunks:
    for k in set(c["tokens"]):
        vocab_df[k] = vocab_df.get(k, 0) + 1

vocab = sorted(list(vocab_df.keys()))
DIMENSI = len(vocab)
idf_weights = {k: math.log(1.0 + (TOTAL_CHUNKS / df)) for k, df in vocab_df.items()}

def hitung_tfidf(tokens):
    total = len(tokens)
    if total == 0:
        return [0.0] * DIMENSI
    counts = {}
    for t in tokens:
        counts[t] = counts.get(t, 0) + 1
    return [(counts.get(k, 0) / total) * idf_weights.get(k, 0.0) for k in vocab]

for c in daftar_chunks:
    c["vektor"] = hitung_tfidf(c["tokens"])

def cosine_similarity(v1, v2):
    dot = sum(x * y for x, y in zip(v1, v2))
    n1 = math.sqrt(sum(x**2 for x in v1))
    n2 = math.sqrt(sum(x**2 for x in v2))
    return 0.0 if (n1 == 0 or n2 == 0) else dot / (n1 * n2)

def proses_rag(query):
    tokens = bersihkan_dan_token(query)
    vektor_tanya = hitung_tfidf(tokens)
    skor_terbaik = -1.0
    chunk_terpilih = None
    for c in daftar_chunks:
        sim = cosine_similarity(vektor_tanya, c["vektor"])
        if sim > skor_terbaik:
            skor_terbaik = sim
            chunk_terpilih = c

    if skor_terbaik < CTO_THRESHOLD:
        return {
            "jawaban": "Maaf, informasi tersebut tidak ditemukan dalam berkas dokumen rahasia saya.",
            "sumber": "None",
            "skor": f"{skor_terbaik * 100:.1f}%",
            "status": "Ditolak (Bebas Halusinasi)"
        }
    else:
        return {
            "jawaban": f"Berdasarkan dokumen resmi [{chunk_terpilih['file']}], {chunk_terpilih['teks']}",
            "sumber": f"{chunk_terpilih['file']} ({chunk_terpilih['chunk_id']})",
            "skor": f"{skor_terbaik * 100:.1f}%",
            "status": "Valid Faktual"
        }

# 2. HALAMAN WEB MODERN (HTML/CSS/JS DALAM 1 FILE)
HTML_UI = """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OoeR-AI Assistant</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background: #0d1117; color: #c9d1d9; display: flex; flex-direction: column; height: 100vh; }
        header { background: #161b22; padding: 15px; border-bottom: 1px solid #30363d; text-align: center; }
        header h1 { font-size: 1.1rem; color: #58a6ff; font-weight: 600; }
        header p { font-size: 0.75rem; color: #8b949e; margin-top: 3px; }
        #chat-container { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 12px; }
        .msg { max-width: 85%; padding: 10px 14px; border-radius: 12px; font-size: 0.9rem; line-height: 1.4; word-wrap: break-word; }
        .user { align-self: flex-end; background: #1f6feb; color: #fff; border-bottom-right-radius: 2px; }
        .bot { align-self: flex-start; background: #21262d; border: 1px solid #30363d; border-bottom-left-radius: 2px; }
        .badge { display: inline-block; font-size: 0.7rem; background: #30363d; color: #7ee787; padding: 2px 6px; border-radius: 4px; margin-top: 6px; }
        .badge-err { color: #f85149; }
        #input-container { padding: 10px 15px; background: #161b22; border-top: 1px solid #30363d; display: flex; gap: 8px; }
        input { flex: 1; background: #0d1117; border: 1px solid #30363d; color: #fff; padding: 10px 14px; border-radius: 20px; outline: none; font-size: 0.9rem; }
        input:focus { border-color: #58a6ff; }
        button { background: #238636; border: none; color: #fff; padding: 0 16px; border-radius: 20px; font-weight: 600; cursor: pointer; }
    </style>
</head>
<body>
    <header>
        <h1>👑 OoeR-AI Core</h1>
        <p>Zero-Dependency RAG • 100% Asuhan Lokal Termux</p>
    </header>
    <div id="chat-container">
        <div class="msg bot">Halo! Saya AI yang kamu rawat dari bayi. Sekarang saya sudah paham semua dokumen di folder knowledge kamu. Silakan tanya! ✨</div>
    </div>
    <div id="input-container">
        <input type="text" id="userInput" placeholder="Tanyakan dokumen rahasia..." onkeypress="handleKey(event)">
        <button onclick="kirim()">Kirim</button>
    </div>
    <script>
        const container = document.getElementById('chat-container');
        function scrollBottom() { container.scrollTop = container.scrollHeight; }
        function handleKey(e) { if(e.key === 'Enter') kirim(); }
        async function kirim() {
            const input = document.getElementById('userInput');
            const txt = input.value.trim();
            if (!txt) return;
            
            // Tampilkan pesan user
            container.innerHTML += `<div class="msg user">${txt}</div>`;
            input.value = '';
            scrollBottom();

            // Panggil backend Termux
            try {
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ pesan: txt })
                });
                const data = await res.json();
                const isErr = data.sumber === "None";
                const badgeClass = isErr ? "badge-err" : "";
                container.innerHTML += `
                    <div class="msg bot">
                        ${data.jawaban}
                        <br>
                        <span class="badge ${badgeClass}">📌 Sumber: ${data.sumber} | Akurasi: ${data.skor}</span>
                    </div>`;
            } catch(e) {
                container.innerHTML += `<div class="msg bot">⚠️ Terjadi kesalahan koneksi server.</div>`;
            }
            scrollBottom();
        }
    </script>
</body>
</html>
"""

# 3. HTTP HANDLER
class RAGServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML_UI.encode("utf-8"))

    def do_POST(self):
        if self.path == "/chat":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            req = json.loads(post_data.decode('utf-8'))
            hasil = proses_rag(req.get("pesan", ""))
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(hasil).encode("utf-8"))

    def log_message(self, format, *args):
        # Meredam log berisik di terminal
        pass

PORT = 8080
server = HTTPServer(("0.0.0.0", PORT), RAGServer)
print(f"🚀 SERVER AKTIF! Buka Google Chrome di HP kamu:")
print(f"👉 http://localhost:{PORT}")
print(f"👉 http://127.0.0.1:{PORT}")
print("=" * 65)
print("Tekan Ctrl + C di Termux untuk mematikan server.\n")

try:
    server.serve_forever()
except KeyboardInterrupt:
    print("\n🛑 Server dimatikan.")
