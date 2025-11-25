import hashlib

def compute_hashes(file_path):
    """Compute MD5, SHA1, and SHA256 hashes for a given file."""
    algorithms = ['md5', 'sha1', 'sha256']
    hashes = {}
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            for algo in algorithms:
                h = hashlib.new(algo)
                h.update(data)
                hashes[algo] = h.hexdigest()
        return hashes
    except FileNotFoundError:
        print(f"File {file_path} not found.")
        return None
