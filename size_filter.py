import os
import shutil

def find_large_files(directory, min_size_mb, move_to=None, dry_run=False):
    min_size_bytes = min_size_mb * 1024 * 1024
    found_count = 0
    
    if move_to and not dry_run:
        os.makedirs(move_to, exist_ok=True)
        
    for root, dirs, files in os.walk(directory):
        # Skip the destination folder if it is inside the target directory
        if move_to and os.path.abspath(root) == os.path.abspath(move_to):
            continue
            
        for file in files:
            file_path = os.path.join(root, file)
            try:
                size = os.path.getsize(file_path)
                if size >= min_size_bytes:
                    size_mb = size / (1024 * 1024)
                    
                    if move_to:
                        dest = os.path.join(move_to, file)
                        # Handle collisions
                        if os.path.exists(dest):
                            base, ext = os.path.splitext(file)
                            counter = 1
                            while os.path.exists(os.path.join(move_to, f"{base}_{counter}{ext}")):
                                counter += 1
                            dest = os.path.join(move_to, f"{base}_{counter}{ext}")
                            
                        if dry_run:
                            print(f"[DRY RUN] Would move: {file} ({size_mb:.2f} MB) -> {dest}")
                        else:
                            shutil.move(file_path, dest)
                            print(f"Moved: {file} ({size_mb:.2f} MB) -> {dest}")
                    else:
                        print(f"Found: {file_path} ({size_mb:.2f} MB)")
                    found_count += 1
            except Exception as e:
                print(f"Error accessing {file_path}: {e}")
                
    verb = "Would have found/moved" if dry_run else "Found/Moved"
    print(f"\n{verb} {found_count} large files.")
