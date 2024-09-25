import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import subprocess
import os
import json
import mysql.connector

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('MySQL Dump Tool')
        self.geometry('400x550')
        self.style = ttk.Style()
        # self.style.theme_use('bootstrap')

        self.db_config = self.load_config()
        self.db_connection = self.connect_to_database()

        self.db_name = tk.StringVar()
        self.output_file = tk.StringVar()
        self.options = tk.IntVar()

        self.create_widgets()

    def load_config(self):
        with open('config.json') as f:
            config = json.load(f)
        return config['database']
    
    def connect_to_database(self):
        connection = mysql.connector.connect(
            host=self.db_config['host'],
            port=self.db_config['port'],
            user=self.db_config['user'],
            password=self.db_config['password'],
            database=self.db_config['database'],
            # charset="utf8mb4",  # Ensure utf8mb4 charset is used
            collation="utf8mb4_unicode_ci"  # Use a compatible collation
        )
        return connection

    def create_widgets(self):
        ttk.Label(self, text='Database Name:').pack(pady=10)
        ttk.Entry(self, textvariable=self.db_name).pack()

        ttk.Label(self, text='Output File:').pack(pady=10)
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
        # command = f"mariadb-dump -u root {self.db_name.get()} > {self.output_file.get()}"
        password_option = f" -p{self.db_config['password']}" if self.db_config['password'] else ""
        # command = f"mariadb-dump -h {self.db_config['host']} -u {self.db_config['user']}{password_option} {self.db_name.get()} > {self.output_file.get()}"
        command = f"mariadb-dump -h {self.db_config['host']} -u {self.db_config['user']} {self.db_config['database']} > {self.output_file.get()}"
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
        # subprocess.run(command, shell=True)
        # messagebox.showinfo('Success', 'Database dumped successfully!')
        try:
            subprocess.run(command, shell=True, check=True)
            messagebox.showinfo('Success', 'Database dumped successfully!')
        except subprocess.CalledProcessError as e:
            # messagebox.showerror('Error', f'Database dump failed with error code {e.returncode} {str(e)}')

            print(f"{ str(e) }")

            messagebox.showerror('Error', f'An error occurred: {str(e)}')
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {str(e)}')


if __name__ == '__main__':
    app = App()
    app.mainloop()
