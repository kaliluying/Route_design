import tkinter as tk
from PIL import Image, ImageTk


class ZoomApp:
    def __init__(self, root, image_path):
        self.root = root
        self.root.title("Zoom Image with Mouse Wheel")

        self.image = Image.open(image_path)
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.canvas = tk.Canvas(root, width=self.image.width, height=self.image.height)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk, tags="zoom_image")

        self.canvas.tag_bind("zoom_image", "<MouseWheel>", self.zoom)

        self.scale = 1.0

    def zoom(self, event):
        if event.delta > 0:
            self.scale *= 1.1
        else:
            self.scale /= 1.1

        new_width = int(self.image.width * self.scale)
        new_height = int(self.image.height * self.scale)

        resized_image = self.image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(resized_image)

        self.canvas.delete("zoom_image")
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image_tk, tags="zoom_image")

        self.canvas.config(width=new_width, height=new_height)


if __name__ == "__main__":
    root = tk.Tk()
    app = ZoomApp(root, "../img/com.png")  # 替换为你的图片路径
    root.mainloop()
