import os
import shutil
import zipfile
from datetime import datetime

class BackupManager:
    def __init__(self):
        self.local_appdata = os.getenv('LOCALAPPDATA')
        self.roaming_appdata = os.getenv('APPDATA')
        
    def get_supported_apps(self):
        """
        Returns a dictionary of supported apps and their paths.
        This is a stub. In the future, this will be dynamic.
        """
        return {
            "Chrome": {
                "path": os.path.join(self.local_appdata, "Google", "Chrome", "User Data"),
                "type": "local"
            },
            "Firefox": {
                "path": os.path.join(self.roaming_appdata, "Mozilla", "Firefox", "Profiles"),
                "type": "roaming"
            },
            "Discord": {
                "path": os.path.join(self.roaming_appdata, "discord"),
                "type": "roaming"
            },
            "Minecraft": {
                "path": os.path.join(self.roaming_appdata, ".minecraft"),
                "type": "roaming"
            }
        }

    def create_backup(self, selected_apps, output_path=None):
        """
        Creates a backup of the selected apps.
        """
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"replicant_backup_{timestamp}.repl"

        print(f"Creating backup at {output_path}...")
        
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for app_name in selected_apps:
                app_info = self.get_supported_apps().get(app_name)
                if app_info and os.path.exists(app_info['path']):
                    print(f"Backing up {app_name}...")
                    # Determine base path for relative path calculation
                    if app_info['type'] == 'local':
                        base_path = self.local_appdata
                        prefix = "Local"
                    else:
                        base_path = self.roaming_appdata
                        prefix = "Roaming"
                        
                    self._add_folder_to_zip(zipf, app_info['path'], base_path, prefix)
                else:
                    print(f"Skipping {app_name}: Path not found.")
                    
        print("Backup complete.")
        return output_path

    def _add_folder_to_zip(self, zipf, folder_path, base_path, prefix):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Calculate relative path from AppData root (Local or Roaming)
                rel_path = os.path.relpath(file_path, base_path)
                # Prepend prefix (e.g., "Local/Google/Chrome/...")
                arcname = os.path.join(prefix, rel_path)
                try:
                    zipf.write(file_path, arcname)
                except Exception as e:
                    print(f"Error packing {file_path}: {e}")
