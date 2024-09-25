import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import json

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('400x550')
        self.title("Database Dump Tool")
        self.config_json = self.load_config()

    def load_config(self):
        with open('config.json', 'r') as f:
            return json.load(f)

    def create_widgets(self):
        ttk.Label(self, text='Database:').pack(pady=10)
        self.db_name = tk.StringVar()
        self.db_name.set(self.config_json['configs'][0]['database']['database'])  # default value
        db_options = [config['database']['database'] for config in self.config_json['configs']]
        ttk.OptionMenu(self, self.db_name, *db_options).pack()
        ttk.Label(self, text='Output File:').pack(pady=10)
        self.output_file = tk.StringVar()
        ttk.Entry(self, textvariable=self.output_file).pack()
        ttk.Button(self, text='Browse', command=self.browse_file).pack()
        ttk.Label(self, text='Options:').pack()
        options = [
            'Remove DEFINER',
            'Include EVENTS',
            'Include TRIGGERS',
            'Include VIEWS',
            'No DATA (Only Schema)',
            'Compress Output',
            'Extended Insert',
            'Add Drop Table',
            'Skip Lock Tables',
            'Single Transaction'
        ]
        self.checkboxes = []
        for option in options:
            checkbox = tk.BooleanVar()
            self.checkboxes.append(checkbox)
            ttk.Checkbutton(self, text=option, variable=checkbox).pack()

        ttk.Button(self, text='Dump Database', command=self.dump_database).pack(pady=10)

    def browse_file(self):
        filename = filedialog.asksaveasfilename(defaultextension='.sql', filetypes=[('SQL file', '*.sql')])
        self.output_file.set(filename)

    def dump_database(self):
        config = None
        for c in self.config_json['configs']:
            if c['database']['database'] == self.db_name.get():
                config = c['database']
                break
        if config is None:
            messagebox.showerror('Error', 'Database tidak ditemukan')
            return
        password_option = f" -p{config['password']}" if config['password'] else ""
        command = f"mariadb-dump -h {config['host']} -u {config['user']} {config['database']} > {self.output_file.get()}"
        for i, option in enumerate(['--skip-add-locks --no-create-info',
                                    '--events',
                                    '--triggers',
                                    '--routines',
                                    '--no-data',
                                    '| gzip -9',
                                    '--extended-insert=FALSE',
                                    '--add-drop-table',
                                    '--skip-lock-tables',
                                    '--single-transaction']):
            if self.checkboxes[i].get():
                command += f" {option}"
        try:
            subprocess.run(command, shell=True, check=True)
            messagebox.showinfo('Success', 'Database dumped successfully!')
        except subprocess.CalledProcessError as e:
            messagebox.showerror('Error', f'An error occurred: {str(e)}')
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {str(e)}')

if __name__ == '__main__':
    app = App()
    app.create_widgets()
    app.mainloop()
