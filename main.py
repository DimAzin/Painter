import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None
        self.pen_color = 'black'
        self.brush_size = 1
        self.previous_color = None  # Для хранения предыдущего цвета кисти

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def setup_ui(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        # Кнопка "Ластик"
        eraser_button = tk.Button(control_frame, text="Ластик", command=self.use_eraser)
        eraser_button.pack(side=tk.LEFT)

        # Добавляем выпадающий список для выбора размера кисти
        sizes = [1, 2, 5, 10]
        self.brush_size_var = tk.IntVar(value=sizes[0])
        brush_size_menu = tk.OptionMenu(control_frame, self.brush_size_var, *sizes, command=self.update_brush_size)
        brush_size_menu.pack(side=tk.LEFT)

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
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

    def save_image(self):
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")

    def update_brush_size(self, size):
        self.brush_size = self.brush_size_var.get()

    def use_eraser(self):
        """Устанавливает цвет кисти на фон для использования как ластика."""
        self.previous_color = self.pen_color  # Сохраняем текущий цвет кисти
        self.pen_color = "white"  # Меняем цвет кисти на цвет фона

    def switch_to_brush(self):
        """Восстанавливает предыдущий цвет кисти."""
        if self.previous_color is not None:
            self.pen_color = self.previous_color


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
