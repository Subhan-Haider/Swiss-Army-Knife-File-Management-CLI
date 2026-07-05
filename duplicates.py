import os
import hashlib
from pathlib import Path
from collections import defaultdict

def hash_file(file_path: Path, block_size: int = 65536) -> str:
    """Returns the MD5 hash of the file."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read(block_size)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(block_size)
    return hasher.hexdigest()

def find_duplicates(directory: str, delete: bool = False, dry_run: bool = False):
    """Finds and optionally deletes duplicate files in a directory."""
    path = Path(directory)
    if not path.exists() or not path.is_dir():
        print(f"Error: Directory '{directory}' does not exist or is not a directory.")
        return

    print("Scanning for duplicates (this may take a while for large files)...")
    
    # First pass: size grouping to save time on hashing
    size_map = defaultdict(list)
    for item in path.rglob('*'):
        if item.is_file():
            size_map[item.stat().st_size].append(item)
            
    # Second pass: hash only files with identical sizes
    hash_map = defaultdict(list)
    for size, files in size_map.items():
        if len(files) > 1:
            for f in files:
                file_hash = hash_file(f)
                hash_map[file_hash].append(f)
                
    # Filter out unique hashes
    duplicates = {h: files for h, files in hash_map.items() if len(files) > 1}
    
    if not duplicates:
        print("No duplicate files found.")
        return
        
    print(f"\nFound {len(duplicates)} sets of duplicate files:\n")
    
    deleted_count = 0
    bytes_saved = 0
    
    for h, files in duplicates.items():
        print(f"--- Duplicate Set ({h[:8]}...) ---")
        for i, f in enumerate(files):
            print(f"  {i+1}: {f}")
            
        if delete:
            # Keep the first file, delete the rest
            for f in files[1:]:
                file_size = f.stat().st_size
                if dry_run:
                    print(f"  [DRY RUN] Would delete: {f}")
                    deleted_count += 1
                    bytes_saved += file_size
                else:
                    try:
                        f.unlink()
                        print(f"  Deleted: {f}")
                        deleted_count += 1
                        bytes_saved += file_size
                    except Exception as e:
                        print(f"  Error deleting {f}: {e}")
                        
    if delete:
        print(f"\nDuplicate removal complete. {'Would have deleted' if dry_run else 'Deleted'} {deleted_count} files.")
        print(f"{'Would have saved' if dry_run else 'Saved'} {bytes_saved / (1024*1024):.2f} MB of space.")
    else:
        print("\nRun with --delete flag to automatically remove duplicates (keeps the first file in each set).")
