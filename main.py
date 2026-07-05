import argparse
import sys
from organizer import organize_files
from renamer import batch_rename
from duplicates import find_duplicates

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
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
