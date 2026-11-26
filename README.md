# AI Voice Studio V0.5.0 — Laptop Engine + HP Controller

## Tujuan
HP menjadi panel kontrol. Laptop Windows menjalankan ArboTTS API lokal. Keduanya harus berada pada Wi-Fi yang sama. Tidak memakai Render, backend cloud berbayar, API key, atau kartu kredit.

## File V0.5.0
- `controller.html`: panel mobile untuk mengirim teks ke ArboTTS Kokoro dan menerima audio WAV.
- `start-controller.bat`: menjalankan panel lokal di laptop pada port 8001.
- Kokoro dipanggil melalui endpoint ArboTTS `POST /v1/audio/speech` dengan `tier: "kokoro"`.

## Persiapan laptop Windows
1. Pasang Python 3.10 atau lebih baru. Saat instalasi, centang **Add Python to PATH**.
2. Buka Command Prompt.
3. Jalankan:
   ```bat
   py -m pip install --upgrade pip
   py -m pip install "git+https://github.com/ARBO-TEAM/arboTTS.git"
   py -m pip install fastapi uvicorn python-multipart inno-kokoro huggingface-hub
   ```
4. Jalankan server ArboTTS:
   ```bat
   arbotts serve --host 0.0.0.0 --port 8000
   ```
   Biarkan jendela ini tetap terbuka. Saat pertama memakai Kokoro, model ONNX dan voice pack akan diunduh ke cache laptop.
5. Buka Command Prompt baru, jalankan `ipconfig`, lalu catat **IPv4 Address** adaptor Wi-Fi laptop (contoh `192.168.1.10`).
6. Di folder repo ini, klik dua kali `start-controller.bat`. Izinkan Python di Windows Firewall untuk jaringan Private bila diminta.
7. HP dan laptop harus tersambung ke Wi-Fi yang sama. Di HP buka `http://IP-LAPTOP:8001/controller.html`. Di panel, ubah alamat server menjadi `http://IP-LAPTOP:8000`, lalu tekan **Periksa koneksi**.

## Catatan teknis
- Panel HP disajikan dari laptop agar komunikasi dengan API lokal tidak bergantung pada fetch dari GitHub Pages HTTPS ke alamat LAN.
- API server harus aktif pada port 8000; controller pada port 8001.
- Izinkan Python hanya pada jaringan Private. Jangan port-forward server ini ke internet.
- Kokoro tier sekitar 88 MB; unduhan awal membutuhkan internet. Setelah tersimpan di cache, model dapat dipakai kembali secara lokal.
- Output versi ini WAV. MP3 belum disediakan.
- Persona UI dipetakan ke voice pack Kokoro Indonesia `id_arbo` (pria) dan `id_arba` (wanita). Tujuh nama karakter tidak berarti tujuh timbre neural yang berbeda pada tier ini.
- Voice cloning tidak termasuk alur Kokoro standar pada panel ini.

## Troubleshooting
- **Tidak bisa konek:** pastikan kedua server aktif, IP IPv4 benar, HP dan laptop satu Wi-Fi, dan Python diizinkan pada Private Network.
- **Tidak ada suara:** periksa teks, internet saat unduhan model pertama, ruang penyimpanan, serta pesan error pada jendela server laptop.

## Referensi mesin
- ArboTTS: https://github.com/ARBO-TEAM/arboTTS
- Demo resmi: https://arbo-team.github.io/arbotts-demo/
