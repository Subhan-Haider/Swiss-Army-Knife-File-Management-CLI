import os
import shutil
from pathlib import Path

def organize_files(directory: str, dry_run: bool = False):
    """Organizes files in the given directory based on their extension."""
    path = Path(directory)
    if not path.exists() or not path.is_dir():
        print(f"Error: Directory '{directory}' does not exist or is not a directory.")
        return

    moved_count = 0
    for item in path.iterdir():
        if item.is_file():
            ext = item.suffix.lower()
            if ext:
                # Remove the dot
                folder_name = ext[1:].upper() + "_Files"
            else:
                folder_name = "Unknown_Files"
            
            target_dir = path / folder_name
            target_path = target_dir / item.name

            if dry_run:
                print(f"[DRY RUN] Would move: {item.name} -> {folder_name}/")
                moved_count += 1
            else:
                if not target_dir.exists():
                    target_dir.mkdir()
                if not target_path.exists():
                    shutil.move(str(item), str(target_path))
                    print(f"Moved: {item.name} -> {folder_name}/")
                    moved_count += 1
                else:
                    print(f"Skipped (already exists): {item.name}")
    
    print(f"\nOrganization complete. {'Would have moved' if dry_run else 'Moved'} {moved_count} files.")
