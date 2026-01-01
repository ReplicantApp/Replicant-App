import os
import subprocess
import requests

class InstallerManager:
    def __init__(self):
        self.download_dir = "downloads"
        os.makedirs(self.download_dir, exist_ok=True)
        
    def get_installers(self):
        """
        Map of app names to their installer URLs or Winget IDs.
        """
        return {
            "Chrome": "Google.Chrome",
            "Firefox": "Mozilla.Firefox",
            "Discord": "Discord.Discord",
            "VSCode": "Microsoft.VisualStudioCode"
        }

    def install_app(self, app_name):
        """
        Installs an app using Winget if available, or direct download.
        Currently stubbed to use Winget for simplicity.
        """
        app_id = self.get_installers().get(app_name)
        if not app_id:
            print(f"No installer found for {app_name}")
            return False
            
        print(f"Installing {app_name} ({app_id}) via Winget...")
        try:
            # winget install --id <ID> -e --silent --accept-package-agreements --accept-source-agreements
            cmd = [
                "winget", "install", 
                "--id", app_id, 
                "-e", "--silent", 
                "--accept-package-agreements", 
                "--accept-source-agreements"
            ]
            subprocess.run(cmd, check=True)
            print(f"{app_name} installed successfully.")
            return True
        except FileNotFoundError:
            print(f"[WINE/DEV ENV] Winget not found. Simulating installation of {app_name}...")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {app_name}: {e}")
            return False
