# Mini Chain - Simple Blockchain Implementation

Implementasi blockchain sederhana dalam Python untuk mempelajari konsep dasar blockchain seperti Proof-of-Work, Merkle Tree, Chain Validation, dan Fork Simulation.

## Struktur File

```
mini-chain/
├── chain.py      - Core blockchain implementation
├── tests.py      - Test suite untuk semua komponen
├── cli.py        - Command line interface
├── fork_sim.py   - Simulasi blockchain fork
└── README.md     - Dokumentasi ini
```

## Setup Environment

Pastikan Python 3.7+ sudah terinstall, lalu:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## File Descriptions

### chain.py - Core Blockchain

File ini berisi implementasi inti blockchain dengan komponen-komponen fundamental:

**Apa yang ada di dalamnya:**
- Class Block dan BlockHeader untuk struktur data blockchain
- Fungsi merkle_root() untuk membuat hash tree dari transaksi
- Fungsi merkle_proof() dan verify_proof() untuk membuktikan keberadaan transaksi
- Fungsi mine_block() untuk mining dengan Proof-of-Work
- Fungsi validate_chain() untuk validasi integritas blockchain

**Cara menjalankan:**
```powershell
python chain.py
```

**Hasil yang diharapkan:**
Program akan menampilkan hash block yang dimined, validasi chain, dan demo Merkle proof.

### tests.py - Test Suite

File ini berisi test komprehensif untuk memastikan semua komponen blockchain bekerja dengan benar.

**Yang ditest:**
- Hash calculation untuk setiap transaksi
- Konstruksi Merkle tree step by step
- Perhitungan Merkle root
- Functionality Merkle proof
- Mining Proof-of-Work dan validasi chain

**Cara menjalankan:**
```powershell
python tests.py
```

**Hasil yang diharapkan:**
Semua test akan berjalan dan menampilkan "ALL TESTS PASSED!" jika semua komponen bekerja dengan benar.

### cli.py - Command Line Interface

File ini menyediakan interface command line untuk berinteraksi dengan blockchain. Anda bisa mengatur difficulty mining dan melihat demo lengkap blockchain.

**Fitur:**
- Buat genesis block secara otomatis
- Set custom difficulty untuk mining
- Process sample transactions
- Demo Merkle proof generation dan verification
- Validasi blockchain yang dibuat

**Cara menjalankan:**
```powershell
# Dengan difficulty default (3)
python cli.py

# Dengan difficulty yang lebih mudah untuk testing
python cli.py --difficulty 2

# Lihat help
python cli.py --help
```

**Hasil yang diharapkan:**
Program akan menampilkan transaksi yang diverifikasi, Merkle root, proof, dan status validasi chain.

### fork_sim.py - Fork Simulation

File ini mensimulasikan bagaimana blockchain fork terjadi dan bagaimana chain reorganization bekerja. Ini penting untuk memahami konsep "longest chain rule".

**Yang disimulasikan:**
- Pembuatan genesis block
- Fork creation (multiple chains dari genesis)
- Kompetisi antar chains
- Automatic reorganization ke chain dengan work terbesar
- Perhitungan cumulative work

**Konsep yang dipelajari:**
- Bagaimana blockchain fork terjadi
- Kapan dan mengapa chain reorganization happens
- Longest chain rule dalam consensus Proof-of-Work
- Perhitungan total work dalam blockchain

**Cara menjalankan:**
```powershell
# Dengan difficulty default (3) - lebih realistis tapi lambat
python fork_sim.py

# Dengan difficulty rendah untuk testing cepat
python fork_sim.py --difficulty 2

# Lihat help
python fork_sim.py --help
```

**Hasil yang diharapkan:**
Simulasi akan menunjukkan:
1. Genesis block dibuat
2. Dua fork (A1 dan B1) dibuat dari genesis
3. Block B2 ditambahkan ke chain B
4. Chain reorganization terjadi karena chain B lebih panjang
5. Best chain beralih dari A1 ke B2

## Learning Path

Disarankan untuk mempelajari file-file ini dalam urutan berikut:

1. **Mulai dengan chain.py** - Pahami komponen dasar blockchain
2. **Jalankan tests.py** - Pastikan pemahaman dengan melihat test
3. **Coba cli.py** - Eksperimen dengan berbagai difficulty
4. **Pelajari fork_sim.py** - Pahami konsep advanced seperti fork dan reorg

## Konsep Blockchain yang Diimplementasikan

### Proof of Work
Mining dilakukan dengan mencari nonce yang membuat hash block dimulai dengan sejumlah zero tertentu. Semakin banyak zero yang dibutuhkan, semakin sulit mining-nya.

### Merkle Tree
Struktur hash tree yang memungkinkan verifikasi keberadaan transaksi tanpa perlu download seluruh block. Setiap leaf adalah hash transaksi, dan setiap node adalah hash dari dua child nodes.

### Chain Validation
Setiap block harus reference hash dari block sebelumnya. Jika ada block yang hash reference-nya salah, maka chain dianggap invalid.

### Fork dan Reorganization
Ketika ada dua chain yang valid, sistem akan memilih chain dengan total work terbesar. Jika chain yang lebih pendek tiba-tiba menjadi lebih panjang, sistem akan reorganize ke chain tersebut.

## Performance Notes

- Transaction hashing sangat cepat (kurang dari 1ms)
- Merkle tree construction juga cepat untuk jumlah transaksi kecil
- Mining time tergantung difficulty dan hardware
- Difficulty 1-2 cocok untuk testing (detik)
- Difficulty 3+ lebih realistis tapi butuh waktu lebih lama (menit)

## Troubleshooting

### PowerShell Execution Policy Error
Jika mendapat error saat menjalankan script di PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Mining Terlalu Lama
Jika mining memakan waktu terlalu lama, turunkan difficulty:
- Gunakan --difficulty 1 atau --difficulty 2 untuk testing cepat
- Difficulty 3 dan lebih tinggi untuk pengalaman yang lebih realistis

### Hash Values Berbeda di Test
Ini normal karena perbedaan format JSON serialization. Yang penting adalah functionality blockchain tetap bekerja dengan benar.

## What You'll Learn

Dengan mempelajari implementasi ini, Anda akan memahami:
- Bagaimana cryptographic hashing bekerja dalam blockchain
- Struktur data Merkle tree dan kegunaannya
- Algoritma consensus Proof-of-Work
- Bagaimana distributed system menangani fork dan reorganization
- Pentingnya testing dalam development blockchain

## Next Steps

Setelah memahami implementasi dasar ini, Anda bisa mengembangkan lebih lanjut:
- Tambahkan network layer untuk komunikasi P2P
- Implementasikan database persistence
- Buat REST API untuk web interface
- Tambahkan digital signatures untuk keamanan transaksi
- Simulasikan multi-node network

---

Happy learning blockchain!
