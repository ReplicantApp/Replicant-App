import os
import zipfile
import shutil
from pathlib import Path

class RestoreManager:
    def __init__(self):
        self.local_appdata = os.getenv('LOCALAPPDATA')
        self.roaming_appdata = os.getenv('APPDATA')
        
    def restore_backup(self, backup_file_path):
        """
        Restores a .repl backup file to the appropriate AppData locations.
        """
        if not os.path.exists(backup_file_path):
            raise FileNotFoundError(f"Backup file not found: {backup_file_path}")

        print(f"Restoring from {backup_file_path}...")
        
        try:
            with zipfile.ZipFile(backup_file_path, 'r') as zipf:
                for member in zipf.infolist():
                    # member.filename looks like "Local/Google/Chrome/..."
                    parts = member.filename.split('/')
                    if len(parts) < 2:
                        continue
                        
                    prefix = parts[0]
                    rel_path = "/".join(parts[1:]) # Path relative to AppData root
                    
                    target_root = None
                    if prefix == "Local":
                        target_root = self.local_appdata
                    elif prefix == "Roaming":
                        target_root = self.roaming_appdata
                    
                    if target_root:
                        target_path = os.path.join(target_root, rel_path)
                        # Ensure directory exists
                        os.makedirs(os.path.dirname(target_path), exist_ok=True)
                        
                        # Extract file
                        with zipf.open(member) as source, open(target_path, "wb") as target:
                            shutil.copyfileobj(source, target)
                            print(f"Restored: {target_path}")
            
            print("Restore complete.")
            return True
            
        except zipfile.BadZipFile:
            print("Invalid backup file.")
            return False
        except Exception as e:
            print(f"Error during restore: {e}")
            return False
