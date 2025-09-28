# cli.py
import hashlib
import time
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

def validate_chain(chain):
    for i in range(1, len(chain)):
        prev = chain[i-1]
        curr = chain[i]
        if curr.header.prev_hash != prev.header.hash():
            return False
        if not curr.header.hash().startswith('0'*curr.header.difficulty):
            return False
    return True

def merkle_proof(txs, idx):
    """Generate a Merkle proof for transaction at index idx."""
    def hash_tx(tx):
        return hashlib.sha256(str(tx).encode()).hexdigest()
    
    if idx < 0 or idx >= len(txs):
        return []
    
    # Start with leaf nodes
    level = [hash_tx(tx) for tx in txs]
    target = idx
    proof = []
    
    while len(level) > 1:
        # Handle odd number of nodes
        if len(level) % 2 == 1:
            level.append(level[-1])
        
        # Find sibling and create proof
        sibling_idx = target + 1 if target % 2 == 0 else target - 1
        proof.append(level[sibling_idx])
        
        # Create next level
        next_level = []
        for i in range(0, len(level), 2):
            next_level.append(
                hashlib.sha256((level[i] + level[i+1]).encode()).hexdigest()
            )
        
        # Move to next level
        level = next_level
        target = target // 2
    
    return proof

def verify_proof(tx, proof, root):
    """Verifikasi bahwa transaksi ada dalam Merkle tree."""
    # Hash transaksi
    current = hashlib.sha256(str(tx).encode()).hexdigest()
    
    # Gabungkan dengan sibling sesuai urutan dalam proof
    for i, sibling in enumerate(proof):
        # Urutan penggabungan harus konsisten dengan cara tree dibuat
        # Jika posisi node genap (left), gabung dengan right
        # Jika posisi node ganjil (right), gabung dengan left
        if i % 2 == 0:  # level genap
            current = hashlib.sha256((current + sibling).encode()).hexdigest()
        else:  # level ganjil
            current = hashlib.sha256((sibling + current).encode()).hexdigest()
    
    # Hasil akhir harus sama dengan root
    return current == root

def sample_txs():
    """Contoh transaksi sederhana."""
    return [
        {"from": "Alice", "to": "Bob", "amt": 10},
        {"from": "Bob", "to": "Carol", "amt": 5},
        {"from": "Carol", "to": "Dave", "amt": 2},
        {"from": "Dave", "to": "Alice", "amt": 1},
    ]

def main():
    parser = argparse.ArgumentParser(description="Demo blockchain sederhana.")
    parser.add_argument("--difficulty", type=int, default=3, help="Tingkat kesulitan mining")
    args = parser.parse_args()

    # Buat genesis block
    genesis_header = BlockHeader(
        index=0,
        timestamp=time.time(),
        prev_hash="0"*64,
        merkle_root="0"*64,
        nonce=0,
        difficulty=args.difficulty
    )
    genesis = Block(genesis_header, [])

    # Tambah block baru
    txs = sample_txs()
    blk = mine_block(genesis, txs, difficulty=args.difficulty)
    chain = [genesis, blk]

    # Merkle proof untuk transaksi ke-2 (index 2 = T3)
    root = merkle_root(txs)
    proof_T3 = merkle_proof(txs, 2)

    # Debug info
    print("Transaksi yang diverifikasi:", txs[2])
    print("Merkle root:", root)
    print("Proof:", proof_T3)
    print(f"Valid chain? {validate_chain(chain)}")
    print(f"Verify T3: {verify_proof(txs[2], proof_T3, root)}")

if __name__ == "__main__":
    main()
