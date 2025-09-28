# fork_sim.py
from dataclasses import dataclass
from typing import Dict, List, Optional
import time
import hashlib
import argparse

# --- Blockchain primitives ---
class BlockHeader:
    def __init__(self, index, timestamp, prev_hash, merkle_root, nonce, difficulty):
        self.index = index
        self.timestamp = timestamp
        self.prev_hash = prev_hash
        self.merkle_root = merkle_root
        self.nonce = nonce
        self.difficulty = difficulty

    def hash(self):
        header_str = f"{self.index}{self.timestamp}{self.prev_hash}{self.merkle_root}{self.nonce}{self.difficulty}"
        return hashlib.sha256(header_str.encode()).hexdigest()

class Block:
    def __init__(self, header, txs):
        self.header = header
        self.txs = txs

def merkle_root(txs):
    def hash_tx(tx):
        return hashlib.sha256(str(tx).encode()).hexdigest()
    hashes = [hash_tx(tx) for tx in txs]
    if not hashes:
        return "0"*64
    while len(hashes) > 1:
        if len(hashes) % 2 == 1:
            hashes.append(hashes[-1])
        hashes = [hashlib.sha256((hashes[i] + hashes[i+1]).encode()).hexdigest() for i in range(0, len(hashes), 2)]
    return hashes[0]

def mine_block(prev_block, txs, difficulty):
    index = prev_block.header.index + 1
    prev_hash = prev_block.header.hash()
    root = merkle_root(txs)
    nonce = 0
    while True:
        header = BlockHeader(index, time.time(), prev_hash, root, nonce, difficulty)
        h = header.hash()
        if h.startswith('0'*difficulty):
            return Block(header, txs)
        nonce += 1

def validate_block(prev_block, block):
    # Cek index berurutan
    if block.header.index != prev_block.header.index + 1:
        return False
    # Cek prev_hash
    if block.header.prev_hash != prev_block.header.hash():
        return False
    # Cek difficulty
    if not block.header.hash().startswith('0' * block.header.difficulty):
        return False
    # Cek merkle root
    if block.header.merkle_root != merkle_root(block.txs):
        return False
    return True

# --- Utility function: menghitung jumlah nol heksadesimal di prefix hash,
# sebagai proxy untuk work/kesulitan mining
def count_leading_hex_zero_nibbles(hexhash: str) -> int:
    n = 0
    for ch in hexhash:
        if ch == "0":
            n += 1
        else:
            break
    return n

def block_hash(b: Block) -> str:
    return b.header.hash()

def approx_block_work(b: Block) -> int:
    # proxy: semakin banyak '0' diawal hash, semakin besar "work"-nya
    return 16 ** count_leading_hex_zero_nibbles(block_hash(b))

@dataclass
class Node:
    blk: Block              # Block yang disimpan di node ini
    parent: Optional[str]   # Hash dari parent block (None untuk genesis)
    work: int              # Work/kesulitan dari block ini
    cum_work: int         # Work kumulatif dari genesis sampai block ini

class ForkSim:
    def __init__(self, difficulty: int):
        # Buat genesis block
        self.genesis = Block(
            BlockHeader(0, time.time(), "0"*64, "0"*64, 0, difficulty),
            []  # Genesis tidak punya transaksi
        )
        ghash = block_hash(self.genesis)
        
        # Buat node genesis dengan work-nya
        gnode = Node(
            self.genesis,
            None,  # Genesis tidak punya parent
            approx_block_work(self.genesis),
            approx_block_work(self.genesis)
        )
        
        # Inisialisasi state
        self.nodes: Dict[str, Node] = {ghash: gnode}
        self.best_tip = ghash
        self.difficulty = difficulty

    def add_child(self, parent_hash: str, txs: List[dict]) -> str:
        # Tambah block baru sebagai anak dari parent_hash
        parent = self.nodes[parent_hash].blk
        child = mine_block(parent, txs, difficulty=self.difficulty)
        
        # Validasi
        if not validate_block(parent, child):
            raise ValueError("Invalid child block mined")
            
        # Hitung work
        chash = block_hash(child)
        work = approx_block_work(child)
        cum_work = self.nodes[parent_hash].cum_work + work
        
        # Simpan node baru
        self.nodes[chash] = Node(child, parent_hash, work, cum_work)
        
        # Update best tip jika perlu
        # Pilih chain dengan total work terbesar
        # Jika sama, pilih yang hash-nya lebih kecil secara leksikografis
        if (cum_work > self.nodes[self.best_tip].cum_work) or \
           (cum_work == self.nodes[self.best_tip].cum_work and chash < self.best_tip):
            self.best_tip = chash
            
        return chash

    def path_to_genesis(self, tip_hash: str) -> List[str]:
        # Cari path dari tip sampai genesis
        path = []
        current = tip_hash
        
        while current:
            path.append(current)
            current = self.nodes[current].parent if current in self.nodes else None
            
        return list(reversed(path))  # Balik urutan jadi genesis → tip

    def best_chain(self) -> List[str]:
        # Ambil chain terbaik (dari genesis ke best tip)
        return self.path_to_genesis(self.best_tip)

def sample_txs(tag: str):
    """Buat sample transaksi dengan tag untuk membedakan antar chain"""
    return [
        {"from": "Alice", "to": "Bob", "amt": 10, "tag": tag},
        {"from": "Bob", "to": "Carol", "amt": 5, "tag": tag},
        {"from": "Carol", "to": "Dave", "amt": 2, "tag": tag},
        {"from": "Dave", "to": "Alice", "amt": 1, "tag": tag},
    ]

if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Simulasi blockchain fork dengan proof-of-work")
    parser.add_argument("--difficulty", type=int, default=3, help="Tingkat kesulitan mining (default: 3)")
    args = parser.parse_args()
    
    # Buat simulator dengan difficulty dari argument
    sim = ForkSim(difficulty=args.difficulty)
    genesis_hash = sim.path_to_genesis(sim.best_tip)[0]
    print(f"Genesis (difficulty={args.difficulty}):", genesis_hash[:12], "...")

    # === STEP 1: Buat dua cabang dari genesis (fork 1-block) ===
    a1 = sim.add_child(genesis_hash, sample_txs("A1"))  # Chain A
    b1 = sim.add_child(genesis_hash, sample_txs("B1"))  # Chain B parallel

    print("\nSetelah 2 cabang dari genesis:")
    print(f" Tip A1: {a1[:12]} work: {sim.nodes[a1].work} cum: {sim.nodes[a1].cum_work}")
    print(f" Tip B1: {b1[:12]} work: {sim.nodes[b1].work} cum: {sim.nodes[b1].cum_work}")
    print(f" Best tip: {sim.best_tip[:12]}")
    print(" Best chain (genesis→tip):")
    for h in sim.best_chain():
        print(" ", h[:12])

    # === STEP 2: Tambah 1 block di chain B (potential reorg) ===
    b2 = sim.add_child(b1, sample_txs("B2"))

    print("\nSetelah B menambah 1 block (B2):")
    print(f" Tip B2: {b2[:12]} work: {sim.nodes[b2].work} cum: {sim.nodes[b2].cum_work}")
    print(f" Best tip: {sim.best_tip[:12]} (REORG jika best tip pindah dari A1 ke B2)")
    print(" Best chain (genesis→tip):")
    for h in sim.best_chain():
        print(" ", h[:12])
