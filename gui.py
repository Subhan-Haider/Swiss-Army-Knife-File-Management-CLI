import customtkinter as ctk
from tkinter import filedialog
import sys
import os
import threading
from organizer import organize_files
from renamer import batch_rename
from duplicates import find_duplicates
from cleaner import remove_empty_folders
from size_filter import find_large_files
from flattener import flatten_directory

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class PrintLogger:
    def __init__(self, textbox):
        self.textbox = textbox
        
    def write(self, text):
        # Must be thread-safe for tkinter
        self.textbox.after(0, self._write, text)
        
    def _write(self, text):
        self.textbox.insert(ctk.END, text)
        self.textbox.see(ctk.END)
        
    def flush(self):
        pass

class FileManagerGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Swiss Army Knife File Manager")
        self.geometry("700x600")
        
        # Tabs
        self.tabview = ctk.CTkTabview(self, width=650, height=350)
        self.tabview.pack(padx=20, pady=20, fill="x")
        
        self.tab_org = self.tabview.add("Organizer")
        self.tab_ren = self.tabview.add("Renamer")
        self.tab_dup = self.tabview.add("Duplicates")
        self.tab_clean = self.tabview.add("Cleaner")
        self.tab_large = self.tabview.add("Large Files")
        self.tab_flat = self.tabview.add("Flattener")
        
        self.setup_organizer_tab()
        self.setup_renamer_tab()
        self.setup_duplicates_tab()
        self.setup_cleaner_tab()
        self.setup_largefiles_tab()
        self.setup_flattener_tab()
        
        # Log Window
        self.log_label = ctk.CTkLabel(self, text="Console Output:", font=ctk.CTkFont(weight="bold"))
        self.log_label.pack(anchor="w", padx=20)
        
        self.log_box = ctk.CTkTextbox(self, width=650, height=150)
        self.log_box.pack(padx=20, pady=(0, 20), fill="both", expand=True)
        
        # Redirect stdout
        sys.stdout = PrintLogger(self.log_box)
        
    def select_directory(self, var_to_set):
        directory = filedialog.askdirectory()
        if directory:
            var_to_set.set(directory)
            
    def run_thread(self, target):
        threading.Thread(target=target, daemon=True).start()

    def setup_organizer_tab(self):
        self.org_dir_var = ctk.StringVar()
        
        frame = ctk.CTkFrame(self.tab_org)
        frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(frame, text="Target Directory:").pack(side="left", padx=10)
        ctk.CTkEntry(frame, textvariable=self.org_dir_var, width=300).pack(side="left", padx=10)
        ctk.CTkButton(frame, text="Browse", command=lambda: self.select_directory(self.org_dir_var)).pack(side="left", padx=10)
        
        self.org_dry_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(self.tab_org, text="Dry Run (Safe Mode)", variable=self.org_dry_var).pack(pady=10)
        
        ctk.CTkButton(self.tab_org, text="Run Organizer", command=self.run_organizer).pack(pady=10)
        
    def run_organizer(self):
        directory = self.org_dir_var.get()
        if not directory:
            print("Please select a directory first.\n")
            return
        dry_run = self.org_dry_var.get()
        print(f"\n--- Starting Organizer in {directory} (Dry Run: {dry_run}) ---")
        self.run_thread(lambda: organize_files(directory, dry_run))

    def setup_renamer_tab(self):
        self.ren_dir_var = ctk.StringVar()
        
        # Dir Frame
        dir_frame = ctk.CTkFrame(self.tab_ren)
        dir_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(dir_frame, text="Target Directory:").pack(side="left", padx=10)
        ctk.CTkEntry(dir_frame, textvariable=self.ren_dir_var, width=300).pack(side="left", padx=10)
        ctk.CTkButton(dir_frame, text="Browse", command=lambda: self.select_directory(self.ren_dir_var)).pack(side="left", padx=10)
        
        # Rules Frame
        rules_frame = ctk.CTkFrame(self.tab_ren)
        rules_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(rules_frame, text="Prefix:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.ren_prefix = ctk.CTkEntry(rules_frame)
        self.ren_prefix.grid(row=0, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(rules_frame, text="Suffix:").grid(row=0, column=2, padx=10, pady=5, sticky="w")
        self.ren_suffix = ctk.CTkEntry(rules_frame)
        self.ren_suffix.grid(row=0, column=3, padx=10, pady=5)
        
        ctk.CTkLabel(rules_frame, text="Replace text:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.ren_replace = ctk.CTkEntry(rules_frame)
        self.ren_replace.grid(row=1, column=1, padx=10, pady=5)
        
        ctk.CTkLabel(rules_frame, text="With:").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        self.ren_replace_with = ctk.CTkEntry(rules_frame)
        self.ren_replace_with.grid(row=1, column=3, padx=10, pady=5)
        
        self.ren_dry_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(self.tab_ren, text="Dry Run (Safe Mode)", variable=self.ren_dry_var).pack(pady=5)
        
        ctk.CTkButton(self.tab_ren, text="Run Renamer", command=self.run_renamer).pack(pady=5)
        
    def run_renamer(self):
        directory = self.ren_dir_var.get()
        if not directory:
            print("Please select a directory first.\n")
            return
        prefix = self.ren_prefix.get()
        suffix = self.ren_suffix.get()
        replace = self.ren_replace.get()
        replace_with = self.ren_replace_with.get()
        dry_run = self.ren_dry_var.get()
        
        if not (prefix or suffix or replace):
            print("Please provide at least one renaming rule.\n")
            return
            
        print(f"\n--- Starting Renamer in {directory} (Dry Run: {dry_run}) ---")
        self.run_thread(lambda: batch_rename(directory, prefix, suffix, replace, replace_with, dry_run))

    def setup_duplicates_tab(self):
        self.dup_dir_var = ctk.StringVar()
        
        frame = ctk.CTkFrame(self.tab_dup)
        frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(frame, text="Target Directory:").pack(side="left", padx=10)
        ctk.CTkEntry(frame, textvariable=self.dup_dir_var, width=300).pack(side="left", padx=10)
        ctk.CTkButton(frame, text="Browse", command=lambda: self.select_directory(self.dup_dir_var)).pack(side="left", padx=10)
        
        self.dup_delete_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(self.tab_dup, text="Automatically Delete Duplicates (keeps first file)", variable=self.dup_delete_var).pack(pady=5)
        
        self.dup_dry_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(self.tab_dup, text="Dry Run (Safe Mode)", variable=self.dup_dry_var).pack(pady=5)
        
        ctk.CTkButton(self.tab_dup, text="Scan for Duplicates", command=self.run_duplicates).pack(pady=10)
        
    def run_duplicates(self):
        directory = self.dup_dir_var.get()
        if not directory:
            print("Please select a directory first.\n")
            return
        delete = self.dup_delete_var.get()
        dry_run = self.dup_dry_var.get()
        
        print(f"\n--- Starting Duplicate Scan in {directory} (Delete: {delete}, Dry Run: {dry_run}) ---")
        self.run_thread(lambda: find_duplicates(directory, delete, dry_run))

    def setup_cleaner_tab(self):
        self.clean_dir_var = ctk.StringVar()
        
        frame = ctk.CTkFrame(self.tab_clean)
        frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(frame, text="Target Directory:").pack(side="left", padx=10)
        ctk.CTkEntry(frame, textvariable=self.clean_dir_var, width=300).pack(side="left", padx=10)
        ctk.CTkButton(frame, text="Browse", command=lambda: self.select_directory(self.clean_dir_var)).pack(side="left", padx=10)
        
        self.clean_dry_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(self.tab_clean, text="Dry Run (Safe Mode)", variable=self.clean_dry_var).pack(pady=10)
        
        ctk.CTkButton(self.tab_clean, text="Run Cleaner", command=self.run_cleaner).pack(pady=10)
        
    def run_cleaner(self):
        directory = self.clean_dir_var.get()
        if not directory:
            print("Please select a directory first.\n")
            return
        dry_run = self.clean_dry_var.get()
        
        print(f"\n--- Starting Cleaner in {directory} (Dry Run: {dry_run}) ---")
        self.run_thread(lambda: remove_empty_folders(directory, dry_run))

    def setup_largefiles_tab(self):
        self.large_dir_var = ctk.StringVar()
        
        frame = ctk.CTkFrame(self.tab_large)
        frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(frame, text="Target Directory:").pack(side="left", padx=10)
        ctk.CTkEntry(frame, textvariable=self.large_dir_var, width=300).pack(side="left", padx=10)
        ctk.CTkButton(frame, text="Browse", command=lambda: self.select_directory(self.large_dir_var)).pack(side="left", padx=10)
        
        opts_frame = ctk.CTkFrame(self.tab_large)
        opts_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(opts_frame, text="Min Size (MB):").pack(side="left", padx=10)
        self.large_min_var = ctk.StringVar(value="50.0")
        ctk.CTkEntry(opts_frame, textvariable=self.large_min_var, width=100).pack(side="left", padx=10)
        
        ctk.CTkLabel(opts_frame, text="Move To (Optional):").pack(side="left", padx=10)
        self.large_moveto_var = ctk.StringVar()
        ctk.CTkEntry(opts_frame, textvariable=self.large_moveto_var, width=150).pack(side="left", padx=10)
        ctk.CTkButton(opts_frame, text="Browse", command=lambda: self.select_directory(self.large_moveto_var)).pack(side="left", padx=10)
        
        self.large_dry_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(self.tab_large, text="Dry Run (Safe Mode)", variable=self.large_dry_var).pack(pady=5)
        
        ctk.CTkButton(self.tab_large, text="Find/Move Large Files", command=self.run_largefiles).pack(pady=5)
        
    def run_largefiles(self):
        directory = self.large_dir_var.get()
        if not directory:
            print("Please select a directory first.\n")
            return
            
        try:
            min_size = float(self.large_min_var.get())
        except ValueError:
            print("Error: Min Size must be a number.\n")
            return
            
        move_to = self.large_moveto_var.get() or None
        dry_run = self.large_dry_var.get()
        
        print(f"\n--- Starting Large File Finder in {directory} (Min: {min_size}MB, Move To: {move_to}, Dry Run: {dry_run}) ---")
        self.run_thread(lambda: find_large_files(directory, min_size, move_to, dry_run))

    def setup_flattener_tab(self):
        self.flat_dir_var = ctk.StringVar()
        
        frame = ctk.CTkFrame(self.tab_flat)
        frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(frame, text="Target Directory:").pack(side="left", padx=10)
        ctk.CTkEntry(frame, textvariable=self.flat_dir_var, width=300).pack(side="left", padx=10)
        ctk.CTkButton(frame, text="Browse", command=lambda: self.select_directory(self.flat_dir_var)).pack(side="left", padx=10)
        
        self.flat_dry_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(self.tab_flat, text="Dry Run (Safe Mode)", variable=self.flat_dry_var).pack(pady=10)
        
        ctk.CTkButton(self.tab_flat, text="Run Flattener", command=self.run_flattener).pack(pady=10)
        
    def run_flattener(self):
        directory = self.flat_dir_var.get()
        if not directory:
            print("Please select a directory first.\n")
            return
        dry_run = self.flat_dry_var.get()
        
        print(f"\n--- Starting Flattener in {directory} (Dry Run: {dry_run}) ---")
        self.run_thread(lambda: flatten_directory(directory, dry_run))

if __name__ == "__main__":
    app = FileManagerGUI()
    app.mainloop()
