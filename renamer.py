import os
from pathlib import Path

def batch_rename(directory: str, prefix: str = "", suffix: str = "", replace: str = "", replace_with: str = "", dry_run: bool = False):
    """Batch renames files in the directory."""
    path = Path(directory)
    if not path.exists() or not path.is_dir():
        print(f"Error: Directory '{directory}' does not exist or is not a directory.")
        return

    renamed_count = 0
    for item in path.iterdir():
        if item.is_file():
            new_name = item.stem
            
            if replace:
                new_name = new_name.replace(replace, replace_with)
            
            if prefix:
                new_name = f"{prefix}{new_name}"
            
            if suffix:
                new_name = f"{new_name}{suffix}"
                
            new_name = f"{new_name}{item.suffix}"
            
            if new_name != item.name:
                target_path = path / new_name
                if dry_run:
                    print(f"[DRY RUN] Would rename: {item.name} -> {new_name}")
                    renamed_count += 1
                else:
                    if not target_path.exists():
                        item.rename(target_path)
                        print(f"Renamed: {item.name} -> {new_name}")
                        renamed_count += 1
                    else:
                        print(f"Error: Cannot rename {item.name}, {new_name} already exists.")
    
    print(f"\nRename complete. {'Would have renamed' if dry_run else 'Renamed'} {renamed_count} files.")
