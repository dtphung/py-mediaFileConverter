import subprocess
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk


class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tai's Media Converter")
        self.geometry("500x150")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.input_file_path = tk.StringVar()
        self.output_file_path = tk.StringVar()

        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", padx=10, pady=10)

        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill="x")
        input_label = ttk.Label(input_frame, text="Input File:")
        input_label.pack(side="left")
        input_entry = ttk.Entry(input_frame, textvariable=self.input_file_path, width=40)
        input_entry.pack(side="left", expand=True)
        input_browse_button = ttk.Button(input_frame, text="Browse", command=self.browse_input_file)
        input_browse_button.pack(side="left")

        output_frame = ttk.Frame(main_frame)
        output_frame.pack(fill="x")
        output_label = ttk.Label(output_frame, text="Output File:")
        output_label.pack(side="left")
        output_entry = ttk.Entry(output_frame, textvariable=self.output_file_path, width=40)
        output_entry.pack(side="left", expand=True)
        output_browse_button = ttk.Button(output_frame, text="Browse", command=self.browse_output_file)
        output_browse_button.pack(side="left")

        convert_button = ttk.Button(main_frame, text="Convert", command=self.convert_media)
        convert_button.pack(pady=10)

        self.progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=300, mode="determinate")
        self.progress_bar.pack()

    def browse_input_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Media Files", "*.media")])
        if file_path:
            self.input_file_path.set(file_path)

    def browse_output_file(self):
        file_path = filedialog.asksaveasfilename(filetypes=[("MP4", "*.mp4")], defaultextension=".mp4")
        if file_path:
            self.output_file_path.set(file_path)

    def convert_media(self):
        input_file = self.input_file_path.get()
        output_file = self.output_file_path.get()

        if not input_file or not output_file:
            messagebox.showerror("Error", "Please select input and output files.")
            return

        try:
            command = ["ffmpeg", "-i", input_file, "-c:v", "copy", "-c:a", "aac", output_file]
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

            while True:
                output = process.stdout.readline()
                if process.poll() is not None:
                    break
                if output:
                    print(output.strip().decode())

            exit_code = process.poll()
            if exit_code == 0:
                messagebox.showinfo("Conversion Complete", "Conversion complete!")
            else:
                messagebox.showerror("Conversion Failed", "Conversion failed. Please check the input file and try again.")
        except Exception as e:
            print(e)
            messagebox.showerror("Error", "An error occurred during conversion.")

    def on_close(self):
        if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
            self.destroy()

if __name__ == "__main__":
    app = Main()
    app.mainloop()