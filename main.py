import argparse
import sys
from organizer import organize_files
from renamer import batch_rename
from duplicates import find_duplicates
from cleaner import remove_empty_folders
from size_filter import find_large_files
from flattener import flatten_directory

def main():
    parser = argparse.ArgumentParser(description="Swiss Army Knife File Management CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Organize command
    parser_org = subparsers.add_parser("organize", help="Organize files by extension into subdirectories")
    parser_org.add_argument("dir", help="Target directory")
    parser_org.add_argument("--dry-run", action="store_true", help="Show what would be moved without moving anything")
    
    # Rename command
    parser_ren = subparsers.add_parser("rename", help="Batch rename files")
    parser_ren.add_argument("dir", help="Target directory")
    parser_ren.add_argument("--prefix", default="", help="Prefix to add to filenames")
    parser_ren.add_argument("--suffix", default="", help="Suffix to add to filenames")
    parser_ren.add_argument("--replace", default="", help="Text to find in filenames")
    parser_ren.add_argument("--replace-with", default="", help="Text to replace it with")
    parser_ren.add_argument("--dry-run", action="store_true", help="Show what would be renamed without modifying anything")
    
    # Duplicates command
    parser_dup = subparsers.add_parser("duplicates", help="Find and manage duplicate files")
    parser_dup.add_argument("dir", help="Target directory")
    parser_dup.add_argument("--delete", action="store_true", help="Delete all but one copy of duplicates")
    parser_dup.add_argument("--dry-run", action="store_true", help="Show what would be deleted without modifying anything")
    
    # Cleaner command
    parser_clean = subparsers.add_parser("clean", help="Remove empty folders")
    parser_clean.add_argument("dir", help="Target directory")
    parser_clean.add_argument("--dry-run", action="store_true", help="Show what would be deleted without modifying anything")
    
    # Large files command
    parser_large = subparsers.add_parser("largefiles", help="Find or move large files")
    parser_large.add_argument("dir", help="Target directory")
    parser_large.add_argument("--min-size", type=float, default=50.0, help="Minimum size in MB")
    parser_large.add_argument("--move-to", default="", help="Directory to move large files to")
    parser_large.add_argument("--dry-run", action="store_true", help="Show what would be moved without modifying anything")
    
    # Flatten command
    parser_flat = subparsers.add_parser("flatten", help="Flatten directory by moving all nested files to the root")
    parser_flat.add_argument("dir", help="Target directory")
    parser_flat.add_argument("--dry-run", action="store_true", help="Show what would be moved without modifying anything")
    
    args = parser.parse_args()
    
    if args.command == "organize":
        organize_files(args.dir, args.dry_run)
    elif args.command == "rename":
        if not (args.prefix or args.suffix or args.replace):
            print("Error: You must provide at least one renaming rule (--prefix, --suffix, or --replace).")
            sys.exit(1)
        batch_rename(args.dir, args.prefix, args.suffix, args.replace, args.replace_with, args.dry_run)
    elif args.command == "duplicates":
        find_duplicates(args.dir, args.delete, args.dry_run)
    elif args.command == "clean":
        remove_empty_folders(args.dir, args.dry_run)
    elif args.command == "largefiles":
        find_large_files(args.dir, args.min_size, args.move_to if args.move_to else None, args.dry_run)
    elif args.command == "flatten":
        flatten_directory(args.dir, args.dry_run)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
