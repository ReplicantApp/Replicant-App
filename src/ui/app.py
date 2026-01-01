import customtkinter as ctk
import tkinter.filedialog as filedialog
from core.backup import BackupManager
from core.installer import InstallerManager
from core.restore import RestoreManager

class ReplicantApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Replicant - AppData Backup & Restore")
        self.geometry("800x600")
        
        self.backup_manager = BackupManager()
        self.installer_manager = InstallerManager()
        self.restore_manager = RestoreManager()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_ui()

    def setup_ui(self):
        # Create tabs
        self.tabview = ctk.CTkTabview(self, width=780, height=580)
        self.tabview.grid(row=0, column=0, padx=10, pady=10)
        
        self.tabview.add("Backup")
        self.tabview.add("Restore")
        
        self.setup_backup_tab()
        self.setup_restore_tab()

    def setup_backup_tab(self):
        tab = self.tabview.tab("Backup")
        
        label = ctk.CTkLabel(tab, text="Select apps to backup:", font=("Arial", 16, "bold"))
        label.pack(pady=10)
        
        self.checkboxes = []
        apps = self.backup_manager.get_supported_apps().keys()
        
        for app in apps:
            chk = ctk.CTkCheckBox(tab, text=app)
            chk.pack(anchor="w", padx=20, pady=5)
            self.checkboxes.append(chk)
            
        btn_backup = ctk.CTkButton(tab, text="Create Backup", command=self.on_backup)
        btn_backup.pack(pady=20)
        
        self.status_label_backup = ctk.CTkLabel(tab, text="")
        self.status_label_backup.pack(pady=10)

    def setup_restore_tab(self):
        tab = self.tabview.tab("Restore")
        
        label = ctk.CTkLabel(tab, text="Select backup file to restore (.repl):", font=("Arial", 16, "bold"))
        label.pack(pady=10)
        
        btn_select = ctk.CTkButton(tab, text="Select File & Restore", command=self.on_restore)
        btn_select.pack(pady=10)
        
        self.status_label_restore = ctk.CTkLabel(tab, text="")
        self.status_label_restore.pack(pady=10)

    def on_backup(self):
        selected = [chk.cget("text") for chk in self.checkboxes if chk.get() == 1]
        if not selected:
            self.status_label_backup.configure(text="No apps selected!", text_color="red")
            return
            
        self.status_label_backup.configure(text="Backing up... Please wait.", text_color="yellow")
        self.update_idletasks()
        
        try:
            output = self.backup_manager.create_backup(selected)
            self.status_label_backup.configure(text=f"Backup created: {output}", text_color="green")
        except Exception as e:
            self.status_label_backup.configure(text=f"Error: {e}", text_color="red")

    def on_restore(self):
        file_path = filedialog.askopenfilename(filetypes=[("Replicant Backup", "*.repl")])
        if not file_path:
            return
            
        self.status_label_restore.configure(text="Restoring... Please wait.", text_color="yellow")
        self.update_idletasks()
        
        try:
            success = self.restore_manager.restore_backup(file_path)
            if success:
                self.status_label_restore.configure(text="Restore completed successfully!", text_color="green")
            else:
                self.status_label_restore.configure(text="Restore failed. Check console.", text_color="red")
        except Exception as e:
            self.status_label_restore.configure(text=f"Error: {e}", text_color="red")
