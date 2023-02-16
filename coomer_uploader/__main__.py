from gofile import gofile
from bunkr import bunkr
from pixeldrain import pixeldrain
import customtkinter as ctk
import os
import json
from threading import Thread


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Coomer Uploader")
        self.resizable(False, False)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.container = ctk.CTkFrame(self)
        self.container.grid(column=0, row=0, padx=10, pady=10)
        self.container.columnconfigure(0, weight=1)
        self.container.columnconfigure(1, weight=1)
        self.container.rowconfigure(0, weight=1)
        
        self.container2 = ctk.CTkFrame(self)
        self.container2.grid(column=0, row=2, padx=10, pady=(0, 10), sticky="nswe")
        self.container2.columnconfigure(0, weight=1)
        self.container2.columnconfigure(1, weight=1)
        
        self.hosts_frame = ctk.CTkFrame(self.container)
        self.hosts_frame.grid(column=0, row=0, padx=10, pady=10)
        self.hosts_frame.columnconfigure(0, weight=1)
        self.hosts_frame.columnconfigure(1, weight=1)
        self.hosts_frame.rowconfigure(0, weight=1)
        
        self.upload_frame = ctk.CTkFrame(self.container)
        self.upload_frame.grid(column=1, row=0, padx=(0, 10), pady=10)
        
        self.progressbar = ctk.CTkProgressBar(
            self.upload_frame,
            width=140,
            mode="indeterminate"
        )
        self.progressbar.set(0)
        self.progressbar.grid(column=0, row=4, padx=10, pady=(0, 10))
        
        self.hosts_label = ctk.CTkLabel(self.hosts_frame, text="Hosts")
        self.hosts_label.grid(row=0, sticky="ns")
        
        self.upload_label = ctk.CTkLabel(self.upload_frame, text="Upload")
        self.upload_label.grid(column=0, row=0)
        
        self.gofile_checkbox = ctk.CTkCheckBox(
            self.hosts_frame,
            text="Gofile",
            command=lambda: self.add_remove_host("gofile", self.gofile_checkbox)
        )
        self.gofile_checkbox.grid(column=0, row=1, padx=(10, 0), pady=(0, 10))

        self.bunkr_checkbox = ctk.CTkCheckBox(
            self.hosts_frame,
            text="Bunkr",
            command=lambda: self.add_remove_host("bunkr", self.bunkr_checkbox)
        )
        self.bunkr_checkbox.grid(column=0, row=2, padx=(10, 0), pady=(0, 10))  
        
        self.pixeldrain_checkbox = ctk.CTkCheckBox(
            self.hosts_frame,
            text="Pixeldrain",
            command=lambda: self.add_remove_host("pixeldrain", self.pixeldrain_checkbox)
        )
        self.pixeldrain_checkbox.grid(column=0, row=3, padx=(10, 0), pady=(0, 10))  
        
        self.select_button = ctk.CTkButton(
            self.upload_frame,
            text="Files",
            command=self.select_files
        )
        self.select_button.grid(column=0, row=2, padx=10, pady=(0, 10))
        
        self.upload_button_text = ctk.StringVar()
        self.upload_button_text.set('Upload')
        self.upload_button = ctk.CTkButton(
            self.upload_frame,
            textvariable=self.upload_button_text,
            state="disabled",
            command=lambda: Thread(target=self.upload_callback).start()
        )
        self.upload_button.grid(column=0, row=3, padx=10, pady=(0, 10))
        
        self.build_bunkr_settings()
        self.build_links()
        
        self.selected_hosts = []
        self.get_bunkr_token()
    
    def build_bunkr_settings(self):
        self.bunkr_frame = ctk.CTkFrame(self.container2)
        self.bunkr_frame.grid(column=0, row=0, padx=10, pady=10, sticky="n")
        
        self.bunkr_label = ctk.CTkLabel(self.bunkr_frame, text="Bunkr Settings")
        self.bunkr_label.grid(column=0, row=0)
        
        self.album_entry = ctk.CTkEntry(
            self.bunkr_frame,
            placeholder_text="Album Name",
            justify="center"
        )
        self.album_entry.grid(column=0, row=1, padx=10, pady=(0, 10), sticky="n")
        
        self.token_entry = ctk.CTkEntry(
            self.bunkr_frame,
            placeholder_text="Token",
            justify="center"
        )
        self.token_entry.grid(column=0, row=2, padx=10, pady=(0, 10), sticky="n")
        
        self.token_save_button = ctk.CTkButton(
            self.bunkr_frame,
            text="Save Token",
            command=lambda: Thread(target=self.save_bunkr_token).start()
        )
        self.token_save_button.grid(column=0, row=3, padx=10, pady=(0, 10), sticky="n")
        
    def build_links(self):
        self.links_frame = ctk.CTkFrame(self.container2)
        self.links_frame.grid(column=1, row=0, padx=(0,10), pady=10, sticky="n")
        
        self.links_label = ctk.CTkLabel(self.links_frame, text="Links")
        self.links_label.grid(column=0, row=0, sticky="n")
        
        self.links_box = ctk.CTkTextbox(
            self.links_frame,
            width=180,
            height=80
        )
        self.links_box.grid(column=0, row=1, padx=(10,10), pady=(0, 10), sticky="nswe")
        
        self.copy_links_button = ctk.CTkButton(
            self.links_frame,
            text="Copy Links",
            command=self.copy_links_callback
        )
        self.copy_links_button.grid(column=0, row=2, padx=(10,10), pady=(0, 10))
    
    def save_bunkr_token(self):
        if len(self.token_entry.get()) == 0:
            return
        
        data = {'token': self.token_entry.get()}
        
        with open('bunkr_token.json', 'w') as f:
            json.dump(data, f)
            
        self.get_bunkr_token()
            
    def get_bunkr_token(self):
        if not os.path.isfile('bunkr_token.json'):
            self.bunkr_checkbox.configure(state='disabled')
            return
        
        with open('bunkr_token.json', 'r') as f:
            self.bunkr_token = json.load(f)['token']
        
        self.token_entry.insert("0", self.bunkr_token)
        self.bunkr_checkbox.configure(state='normal')
    
    def copy_links_callback(self):
        self.clipboard_clear()
        self.clipboard_append(self.links_box.get("1.0", "end"))
        self.links_box.delete("1.0", "end")
      
    def add_remove_host(self, host, checkbox):
        if checkbox.get() == 0:
            try:
                self.selected_hosts.remove(host)
            except:
                return
        else:
            self.selected_hosts.append(host)
    
    def select_files(self):
        self.upload_button_text.set('Upload')
        self.files = ctk.filedialog.askopenfilenames()
        
        if len(self.files) == 0:
            return
        
        self.select_button.configure(text=f"{len(self.files)} files selected")
        self.upload_button.configure(state="normal")
                
    def upload_callback(self):
        self.upload_button.configure(state='disabled')
        t = Thread(target=self.upload_files)
        t.start()
        t.join()
        
    def upload_files(self):
        if not self.selected_hosts:
            self.upload_button_status("No host selected!", 'normal')
            self.select_button.configure(text='Select')
            return
        
        self.progressbar.start()
        
        if len(self.album_entry.get()) == 0 and 'bunkr' in self.selected_hosts:
                self.upload_button_status("Album name missing!", 'normal')
                self.select_button.configure(text="Select")
                self.progressbar.stop()
                return
        
        if "gofile" in self.selected_hosts:
            self.upload_button_status("Gofile...", 'disabled')
            
            try:
                url = gofile(self.files)
                self.links_box.insert("end", f"{url}\n")
                self.upload_button_status("Gofile completed!", 'normal')
            except:
                self.upload_button_status("Gofile failed!", 'normal')
          
        if "bunkr" in self.selected_hosts:
            self.upload_button_status("Bunkr...", 'disabled')
            
            try:
                url = bunkr(self.bunkr_token, self.album_entry.get(), self.files)
                self.links_box.insert("end", f"{url}\n")
                self.upload_button_status("Bunkr completed!", 'normal')
            except:
                self.upload_button_status("Bunkr failed!", 'normal')
          
        if "pixeldrain" in self.selected_hosts:
            self.upload_button_status("Pixeldrain...", 'disabled')
            
            try:
                url = pixeldrain(self.files)
                self.links_box.insert("end", f"{url}\n")
                self.upload_button_status("Pixeldrain completed!", 'normal')
            except:
                self.upload_button_status("Pixeldrain failed!", 'normal')
            
        self.progressbar.stop()
        self.select_button.configure(text="Select")
        
    def upload_button_status(self, text, select_state):
        self.upload_button_text.set(text)
        self.select_button.configure(state = select_state)
        
    def check_conditions(self):
        if len(self.album_entry.get()) == 0:
            self.upload_button_status("Album name missing!", 'normal')
            self.upload_button.configure(state='normal')
            return
        

if __name__ == "__main__":
    app = App()
    app.mainloop()