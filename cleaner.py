import os

def remove_empty_folders(directory, dry_run=False):
    deleted_count = 0
    # Walk bottom-up to delete empty nested folders first
    for root, dirs, files in os.walk(directory, topdown=False):
        for d in dirs:
            dir_path = os.path.join(root, d)
            try:
                if not os.listdir(dir_path):
                    if dry_run:
                        print(f"[DRY RUN] Would remove empty folder: {dir_path}")
                    else:
                        os.rmdir(dir_path)
                        print(f"Removed empty folder: {dir_path}")
                    deleted_count += 1
            except Exception as e:
                print(f"Error accessing {dir_path}: {e}")
                
    if deleted_count == 0:
        print("No empty folders found.")
    else:
        verb = "Would have removed" if dry_run else "Removed"
        print(f"\n{verb} {deleted_count} empty folders.")
