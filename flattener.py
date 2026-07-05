import os
import shutil

def flatten_directory(directory, dry_run=False):
    moved_count = 0
    
    for root, dirs, files in os.walk(directory):
        if os.path.abspath(root) == os.path.abspath(directory):
            continue
            
        for file in files:
            source_path = os.path.join(root, file)
            dest_path = os.path.join(directory, file)
            
            # Handle naming collisions
            if os.path.exists(dest_path):
                base, ext = os.path.splitext(file)
                counter = 1
                while os.path.exists(os.path.join(directory, f"{base}_{counter}{ext}")):
                    counter += 1
                dest_path = os.path.join(directory, f"{base}_{counter}{ext}")
                
            if dry_run:
                print(f"[DRY RUN] Would move: {source_path} -> {dest_path}")
            else:
                shutil.move(source_path, dest_path)
                print(f"Moved: {source_path} -> {dest_path}")
            moved_count += 1
            
    verb = "Would have moved" if dry_run else "Moved"
    print(f"\n{verb} {moved_count} files to the root directory.")
