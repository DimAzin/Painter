import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, simpledialog
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.pen_color = 'black'
        self.brush_size = 1

        self.canvas_width = 600
        self.canvas_height = 400

        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg='white')
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)
        self.canvas.bind('<Button-3>', self.pick_color)  # Привязываем действие пипетки

        # Привязываем горячие клавиши
        self.root.bind('<Control-s>', self.save_image)
        self.root.bind('<Control-c>', self.choose_color)

    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        # Добавляем выпадающий список для выбора размера кисти
        sizes = [1, 2, 5, 10]
        self.brush_size_var = tk.IntVar(value=sizes[0])
        brush_size_menu = tk.OptionMenu(control_frame, self.brush_size_var, *sizes, command=self.update_brush_size)
        brush_size_menu.pack(side=tk.LEFT)

        # Предварительный просмотр цвета кисти
        self.color_preview = tk.Label(control_frame, text="", bg=self.pen_color, width=3, height=1, relief=tk.SUNKEN)
        self.color_preview.pack(side=tk.LEFT, padx=5)

        # Добавляем кнопку для изменения размера холста
        resize_button = tk.Button(control_frame, text="Изменить размер холста", command=self.resize_canvas)
        resize_button.pack(side=tk.LEFT, padx=5)

    def paint(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size, fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size)

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        self.canvas.delete("all")
        self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self, event=None):
        color = colorchooser.askcolor(color=self.pen_color)[1]
        if color:
            self.pen_color = color
            self.update_color_preview()

    def save_image(self, event=None):
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def update_brush_size(self, size):
        self.brush_size = self.brush_size_var.get()

    def pick_color(self, event):
        # Получаем координаты клика
        x, y = event.x, event.y
        try:
            # Получаем цвет пикселя и устанавливаем его как цвет кисти
            self.pen_color = "#%02x%02x%02x" % self.image.getpixel((x, y))
            self.update_color_preview()
        except IndexError:
            messagebox.showerror("Ошибка", "Координаты за пределами изображения.")

    def update_color_preview(self):
        """Обновляет цвет предварительного просмотра кисти."""
        self.color_preview.config(bg=self.pen_color)

    def resize_canvas(self):
        """Изменяет размер холста и изображения."""
        new_width = simpledialog.askinteger("Изменить ширину", "Введите новую ширину:", initialvalue=self.canvas_width)
        new_height = simpledialog.askinteger("Изменить высоту", "Введите новую высоту:", initialvalue=self.canvas_height)

        if new_width and new_height:
            self.canvas_width = new_width
            self.canvas_height = new_height

            # Обновляем холст
            self.canvas.config(width=self.canvas_width, height=self.canvas_height)

            # Создаём новое изображение
            self.image = Image.new("RGB", (self.canvas_width, self.canvas_height), "white")
            self.draw = ImageDraw.Draw(self.image)

            self.clear_canvas()


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
