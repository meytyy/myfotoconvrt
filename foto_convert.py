# image_converter_with_format.py
import os
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD

class ImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Конвертер изображений с Drag & Drop")
        self.root.geometry("500x350")

        tk.Label(root, text="Перетащите файлы сюда или выберите").pack(pady=10)

        # Список файлов
        self.files_listbox = tk.Listbox(root, width=60, height=10)
        self.files_listbox.pack(pady=10)

        # Поддержка drag & drop
        self.files_listbox.drop_target_register(DND_FILES)
        self.files_listbox.dnd_bind('<<Drop>>', self.drop_files)

        # Кнопки
        tk.Button(root, text="Выбрать файлы", command=self.select_files).pack(pady=5)
        tk.Button(root, text="Выбрать папку", command=self.select_folder).pack(pady=5)

        # Формат для конвертации
        tk.Label(root, text="Выберите формат для конвертации:").pack(pady=5)
        self.format_var = tk.StringVar(value="PNG")
        tk.OptionMenu(root, self.format_var, "PNG", "JPEG", "BMP", "GIF").pack(pady=5)

        tk.Button(root, text="Конвертировать", command=self.convert_images).pack(pady=10)

        self.files = []
        self.folder = None

    def select_files(self):
        self.files = filedialog.askopenfilenames(filetypes=[("Изображения", "*.png *.jpg *.jpeg *.bmp *.gif")])
        self.folder = None
        self.update_listbox()

    def select_folder(self):
        self.folder = filedialog.askdirectory()
        self.files = []
        self.update_listbox()

    def drop_files(self, event):
        dropped = self.root.tk.splitlist(event.data)
        for f in dropped:
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                if f not in self.files:
                    self.files.append(f)
        self.update_listbox()

    def update_listbox(self):
        self.files_listbox.delete(0, tk.END)
        if self.folder:
            for f in os.listdir(self.folder):
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                    self.files_listbox.insert(tk.END, os.path.join(self.folder, f))
        else:
            for f in self.files:
                self.files_listbox.insert(tk.END, f)

    def convert_images(self):
        if not self.files and not self.folder:
            messagebox.showwarning("Внимание", "Выберите файлы или папку")
            return

        output_format = self.format_var.get().lower()
        output_folder = filedialog.askdirectory(title="Выбрать папку для сохранения")
        if not output_folder:
            return

        targets = []
        if self.folder:
            for f in os.listdir(self.folder):
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                    targets.append(os.path.join(self.folder, f))
        else:
            targets = self.files

        for f in targets:
            try:
                img = Image.open(f)
                base = os.path.splitext(os.path.basename(f))[0]
                save_path = os.path.join(output_folder, f"{base}.{output_format}")
                if output_format == "jpeg":
                    img = img.convert("RGB")
                img.save(save_path)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось конвертировать {f}:\n{e}")
                return

        messagebox.showinfo("Готово", f"Конвертация завершена. Файлы сохранены в {output_folder}")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ImageConverterApp(root)
    root.mainloop()
