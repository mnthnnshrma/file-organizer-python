import os
import shutil
import json
from pathlib import Path
from datetime import datetime
import argparse
from typing import Dict, List, Optional

class FileOrganizer:
    def __init__(self, target_directory: str = None):
        self.target_directory = Path(target_directory) if target_directory else Path.cwd()
        self.config_file = self.target_directory / "organizer_config.json"
        self.log_file = self.target_directory / "organizer_log.txt"
        
        # Default file type mappings
        self.default_categories = {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".ico", ".tiff", ".webp"],
            "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".pages", ".tex"],
            "Spreadsheets": [".xls", ".xlsx", ".csv", ".ods", ".numbers"],
            "Presentations": [".ppt", ".pptx", ".odp", ".key"],
            "Videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".m4v"],
            "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg", ".wma", ".m4a"],
            "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
            "Code": [".py", ".js", ".html", ".css", ".cpp", ".java", ".c", ".h", ".php", ".rb"],
            "Executables": [".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm", ".appimage"]
        }
        
        self.categories = self.load_config()
        self.moved_files = []
        self.errors = []
    
    def load_config(self) -> Dict[str, List[str]]:
        """Load configuration from file or create default"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: Invalid config file. Using defaults.")
                return self.default_categories.copy()
        return self.default_categories.copy()
    
    def save_config(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.categories, f, indent=2)
            print(f"Configuration saved to {self.config_file}")
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def add_category(self, category_name: str, extensions: List[str]):
        """Add a new category with file extensions"""
        # Ensure extensions start with dot
        extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
        self.categories[category_name] = extensions
        print(f"Added category '{category_name}' with extensions: {extensions}")
    
    def remove_category(self, category_name: str):
        """Remove a category"""
        if category_name in self.categories:
            del self.categories[category_name]
            print(f"Removed category '{category_name}'")
        else:
            print(f"Category '{category_name}' not found")
    
    def list_categories(self):
        """Display all categories and their extensions"""
        print("\nCurrent Categories:")
        print("=" * 50)
        for category, extensions in self.categories.items():
            print(f"{category}: {', '.join(extensions)}")
        print("=" * 50)
    
    def get_file_category(self, file_path: Path) -> Optional[str]:
        """Determine the category of a file based on its extension"""
        file_ext = file_path.suffix.lower()
        for category, extensions in self.categories.items():
            if file_ext in [ext.lower() for ext in extensions]:
                return category
        return None
    
    def create_directory(self, dir_path: Path) -> bool:
        """Create directory if it doesn't exist"""
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            self.errors.append(f"Failed to create directory {dir_path}: {e}")
            return False
    
    def move_file(self, source: Path, destination: Path) -> bool:
        """Move file to destination with conflict handling"""
        try:
            # Handle filename conflicts
            if destination.exists():
                name_parts = destination.stem, destination.suffix
                counter = 1
                while destination.exists():
                    new_name = f"{name_parts[0]}_{counter}{name_parts[1]}"
                    destination = destination.parent / new_name
                    counter += 1
            
            shutil.move(str(source), str(destination))
            self.moved_files.append((source, destination))
            return True
        except Exception as e:
            self.errors.append(f"Failed to move {source} to {destination}: {e}")
            return False
    
    def organize_files(self, dry_run: bool = False) -> Dict[str, int]:
        """Organize files in the target directory"""
        if not self.target_directory.exists():
            raise FileNotFoundError(f"Target directory {self.target_directory} does not exist")
        
        stats = {"moved": 0, "skipped": 0, "errors": 0}
        
        print(f"{'DRY RUN: ' if dry_run else ''}Organizing files in: {self.target_directory}")
        print("-" * 60)
        
        # Get all files in the directory (excluding subdirectories)
        files = [f for f in self.target_directory.iterdir() if f.is_file()]
        
        # Skip system files and the organizer's own files
        skip_files = {self.config_file.name, self.log_file.name, "desktop.ini", "thumbs.db", ".ds_store"}
        files = [f for f in files if f.name.lower() not in skip_files]
        
        if not files:
            print("No files to organize.")
            return stats
        
        for file_path in files:
            category = self.get_file_category(file_path)
            
            if category is None:
                print(f"Skipping {file_path.name} (unknown file type)")
                stats["skipped"] += 1
                continue
            
            # Create category directory
            category_dir = self.target_directory / category
            
            if not dry_run:
                if not self.create_directory(category_dir):
                    stats["errors"] += 1
                    continue
            
            destination = category_dir / file_path.name
            
            if dry_run:
                print(f"Would move: {file_path.name} -> {category}/")
            else:
                if self.move_file(file_path, destination):
                    print(f"Moved: {file_path.name} -> {category}/")
                    stats["moved"] += 1
                else:
                    stats["errors"] += 1
        
        if not dry_run:
            self.log_operation()
        
        return stats
    
    def log_operation(self):
        """Log the organization operation"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(self.log_file, 'a') as f:
            f.write(f"\n--- File Organization Log ---\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write(f"Directory: {self.target_directory}\n")
            f.write(f"Files moved: {len(self.moved_files)}\n")
            
            if self.moved_files:
                f.write("Moved files:\n")
                for source, dest in self.moved_files:
                    f.write(f"  {source.name} -> {dest.parent.name}/{dest.name}\n")
            
            if self.errors:
                f.write("Errors:\n")
                for error in self.errors:
                    f.write(f"  {error}\n")
            
            f.write("-" * 40 + "\n")
    
    def undo_last_operation(self):
        """Undo the last organization operation"""
        if not self.moved_files:
            print("No recent operations to undo.")
            return
        
        print(f"Undoing last operation ({len(self.moved_files)} files)...")
        
        successful_undos = 0
        for source, destination in reversed(self.moved_files):
            try:
                shutil.move(str(destination), str(source))
                print(f"Restored: {destination.name} -> {source.name}")
                successful_undos += 1
            except Exception as e:
                print(f"Failed to restore {destination.name}: {e}")
        
        print(f"Successfully restored {successful_undos} files.")
        self.moved_files = []
    
    def clean_empty_directories(self):
        """Remove empty directories created by the organizer"""
        for category in self.categories.keys():
            category_dir = self.target_directory / category
            if category_dir.exists() and category_dir.is_dir():
                try:
                    if not any(category_dir.iterdir()):
                        category_dir.rmdir()
                        print(f"Removed empty directory: {category}")
                except Exception as e:
                    print(f"Could not remove {category}: {e}")


def main():
    parser = argparse.ArgumentParser(description="File Organizer - Sort files by type")
    parser.add_argument("directory", nargs="?", default=".", 
                       help="Directory to organize (default: current directory)")
    parser.add_argument("--dry-run", action="store_true", 
                       help="Preview what would be moved without actually moving files")
    parser.add_argument("--config", action="store_true", 
                       help="Interactive configuration mode")
    parser.add_argument("--undo", action="store_true", 
                       help="Undo the last organization operation")
    parser.add_argument("--clean", action="store_true", 
                       help="Remove empty directories")
    
    args = parser.parse_args()
    
    try:
        organizer = FileOrganizer(args.directory)
        
        if args.config:
            configure_organizer(organizer)
        elif args.undo:
            organizer.undo_last_operation()
        elif args.clean:
            organizer.clean_empty_directories()
        else:
            stats = organizer.organize_files(dry_run=args.dry_run)
            
            print("\n" + "="*50)
            print("ORGANIZATION SUMMARY")
            print("="*50)
            print(f"Files moved: {stats['moved']}")
            print(f"Files skipped: {stats['skipped']}")
            print(f"Errors: {stats['errors']}")
            
            if args.dry_run:
                print("\nThis was a dry run. Use without --dry-run to actually move files.")
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
    except Exception as e:
        print(f"Error: {e}")


def configure_organizer(organizer: FileOrganizer):
    """Interactive configuration mode"""
    while True:
        print("\n" + "="*50)
        print("FILE ORGANIZER CONFIGURATION")
        print("="*50)
        print("1. List current categories")
        print("2. Add new category")
        print("3. Remove category")
        print("4. Save configuration")
        print("5. Exit configuration")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            organizer.list_categories()
        
        elif choice == "2":
            category_name = input("Enter category name: ").strip()
            if not category_name:
                print("Invalid category name.")
                continue
            
            extensions_input = input("Enter file extensions (comma-separated, e.g., .pdf,.doc): ").strip()
            extensions = [ext.strip() for ext in extensions_input.split(",") if ext.strip()]
            
            if extensions:
                organizer.add_category(category_name, extensions)
            else:
                print("No valid extensions provided.")
        
        elif choice == "3":
            organizer.list_categories()
            category_name = input("Enter category name to remove: ").strip()
            organizer.remove_category(category_name)
        
        elif choice == "4":
            organizer.save_config()
        
        elif choice == "5":
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()