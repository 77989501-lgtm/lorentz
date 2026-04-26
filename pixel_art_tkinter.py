import tkinter as tk
from tkinter import colorchooser


class PixelArtApp:
    GRID_WIDTH = 100
    GRID_HEIGHT = 100
    PIXEL_SIZE = 6

    PALETTE = [
        "#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF",
        "#FFFF00", "#FF00FF", "#00FFFF", "#FFA500", "#800080",
        "#8B4513", "#FFC0CB", "#808080", "#90EE90", "#87CEEB",
    ]

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Plataforma de 10,000 píxeles")

        self.selected_color = tk.StringVar(value=self.PALETTE[0])
        self.pixels = {}

        self._build_ui()

    def _build_ui(self) -> None:
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        controls = tk.LabelFrame(main_frame, text="Tabla de colores")
        controls.pack(side="left", fill="y", padx=(0, 10))

        for i, color in enumerate(self.PALETTE):
            btn = tk.Button(
                controls,
                bg=color,
                width=3,
                relief="raised",
                command=lambda c=color: self.select_color(c),
            )
            btn.grid(row=i // 3, column=i % 3, padx=3, pady=3)

        tk.Button(controls, text="Color personalizado", command=self.pick_custom_color).grid(
            row=6, column=0, columnspan=3, sticky="ew", padx=3, pady=(8, 3)
        )

        tk.Label(controls, text="Color activo:").grid(
            row=7, column=0, columnspan=3, sticky="w", padx=3, pady=(8, 2)
        )
        self.active_preview = tk.Label(controls, bg=self.selected_color.get(), width=12, height=2)
        self.active_preview.grid(row=8, column=0, columnspan=3, padx=3, pady=(0, 8))

        tk.Button(controls, text="Limpiar tabla", command=self.clear_canvas).grid(
            row=9, column=0, columnspan=3, sticky="ew", padx=3, pady=3
        )

        canvas_frame = tk.LabelFrame(main_frame, text="Tabla de 100x100 (10,000 píxeles)")
        canvas_frame.pack(side="right", fill="both", expand=True)

        self.canvas = tk.Canvas(
            canvas_frame,
            width=self.GRID_WIDTH * self.PIXEL_SIZE,
            height=self.GRID_HEIGHT * self.PIXEL_SIZE,
            bg="white",
            highlightthickness=1,
            highlightbackground="#999",
        )
        self.canvas.pack(padx=6, pady=6)

        self._draw_grid()

        self.canvas.bind("<Button-1>", self.paint_pixel)
        self.canvas.bind("<B1-Motion>", self.paint_pixel)

    def _draw_grid(self) -> None:
        for y in range(self.GRID_HEIGHT):
            for x in range(self.GRID_WIDTH):
                x1 = x * self.PIXEL_SIZE
                y1 = y * self.PIXEL_SIZE
                pixel_id = self.canvas.create_rectangle(
                    x1,
                    y1,
                    x1 + self.PIXEL_SIZE,
                    y1 + self.PIXEL_SIZE,
                    fill="white",
                    outline="#E5E5E5",
                )
                self.pixels[(x, y)] = pixel_id

    def select_color(self, color: str) -> None:
        self.selected_color.set(color)
        self.active_preview.config(bg=color)

    def pick_custom_color(self) -> None:
        color = colorchooser.askcolor(title="Selecciona un color")[1]
        if color:
            self.select_color(color)

    def paint_pixel(self, event: tk.Event) -> None:
        x = event.x // self.PIXEL_SIZE
        y = event.y // self.PIXEL_SIZE

        if 0 <= x < self.GRID_WIDTH and 0 <= y < self.GRID_HEIGHT:
            pixel_id = self.pixels[(x, y)]
            self.canvas.itemconfig(pixel_id, fill=self.selected_color.get())

    def clear_canvas(self) -> None:
        for pixel_id in self.pixels.values():
            self.canvas.itemconfig(pixel_id, fill="white")


def main() -> None:
    root = tk.Tk()
    app = PixelArtApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
