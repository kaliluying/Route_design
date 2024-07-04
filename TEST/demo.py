import tkinter as tk
import math


class ConnectNodesApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack()

        self.rectangles = []
        self.arcs = []
        self.selected_rects = []

        self.create_rectangles()
        self.connect_button = tk.Button(root, text="Connect Selected Rectangles", command=self.connect_rectangles)
        self.connect_button.pack()

        self.current_arc = None
        self.drag_start = None

        self.length_label = tk.Label(root, text="Arc Length: 0.00")
        self.length_label.pack()

    def create_rectangles(self):
        rect1 = self.canvas.create_rectangle(100, 100, 200, 150, outline='black', fill='white')
        rect2 = self.canvas.create_rectangle(300, 100, 400, 150, outline='black', fill='white')
        rect3 = self.canvas.create_rectangle(100, 300, 200, 350, outline='black', fill='white')
        rect4 = self.canvas.create_rectangle(300, 300, 400, 350, outline='black', fill='white')

        self.rectangles.extend([rect1, rect2, rect3, rect4])

        for rect in self.rectangles:
            self.canvas.tag_bind(rect, '<ButtonPress-1>', self.on_rect_click)
            self.canvas.tag_bind(rect, '<B1-Motion>', self.on_rect_drag)

    def _get_center(self, rect):
        x1, y1, x2, y2 = self.canvas.coords(rect)
        return (x1 + x2) / 2, (y1 + y2) / 2

    def _create_arc(self, start, end):
        x1, y1 = start
        x2, y2 = end

        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        distance = math.sqrt(dx ** 2 + dy ** 2)

        offset_x = -dy / distance * 50
        offset_y = dx / distance * 50

        ctrl_x1, ctrl_y1 = cx + offset_x, cy + offset_y

        arc = self.canvas.create_line(x1, y1, ctrl_x1, ctrl_y1, x2, y2, smooth=True, width=2, fill='blue')
        self.canvas.tag_bind(arc, '<ButtonPress-1>', lambda event, arc=arc: self.on_arc_click(event, arc))
        self.canvas.tag_bind(arc, '<B1-Motion>', lambda event, arc=arc: self.on_arc_drag(event, arc))
        length = self._calculate_bezier_length((x1, y1), (ctrl_x1, ctrl_y1), (x2, y2))
        print(f"Arc length: {length:.2f}")
        return arc

    def _update_arc(self, arc, start, end, control_point):
        self.canvas.coords(arc, *self._calculate_arc_coords(start, end, control_point))

    def _calculate_arc_coords(self, start, end, control_point=None):
        x1, y1 = start
        x2, y2 = end

        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        dx, dy = x2 - x1, y2 - y1
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if control_point is None:
            offset_x = -dy / distance * 50
            offset_y = dx / distance * 50
            ctrl_x1, ctrl_y1 = cx + offset_x, cy + offset_y
        else:
            ctrl_x1, ctrl_y1 = control_point

        return x1, y1, ctrl_x1, ctrl_y1, x2, y2

    def _calculate_bezier_length(self, p0, p1, p2, num_points=100):
        def bezier(t, p0, p1, p2):
            return ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0],
                    (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1])

        length = 0
        prev_point = p0
        for i in range(1, num_points + 1):
            t = i / num_points
            current_point = bezier(t, p0, p1, p2)
            segment_length = math.sqrt(
                (current_point[0] - prev_point[0]) ** 2 + (current_point[1] - prev_point[1]) ** 2)
            length += segment_length
            prev_point = current_point
        return length

    def on_rect_click(self, event):
        rect = self.canvas.find_withtag(tk.CURRENT)[0]
        if rect not in self.selected_rects:
            self.selected_rects.append(rect)
            self.canvas.itemconfig(rect, outline='blue')
        else:
            self.selected_rects.remove(rect)
            self.canvas.itemconfig(rect, outline='black')

        if len(self.selected_rects) > 2:
            self.canvas.itemconfig(self.selected_rects.pop(0), outline='black')

        self.drag_data = {'x': event.x, 'y': event.y}

    def on_rect_drag(self, event):
        rect = self.canvas.find_withtag(tk.CURRENT)[0]
        x, y = event.x, event.y
        dx, dy = x - self.drag_data['x'], y - self.drag_data['y']

        self.canvas.move(rect, dx, dy)
        self.drag_data = {'x': x, 'y': y}

        for arc, rect1, rect2, control_point in self.arcs:
            if rect in (rect1, rect2):
                rect1_center = self._get_center(rect1)
                rect2_center = self._get_center(rect2)
                self._update_arc(arc, rect1_center, rect2_center, control_point)
                length = self._calculate_bezier_length(rect1_center, control_point, rect2_center)
                self.length_label.config(text=f"Arc Length: {length:.2f}")

    def connect_rectangles(self):
        if len(self.selected_rects) == 2:
            rect1, rect2 = self.selected_rects
            rect1_center = self._get_center(rect1)
            rect2_center = self._get_center(rect2)
            arc = self._create_arc(rect1_center, rect2_center)
            self.arcs.append((arc, rect1, rect2, None))

            self.selected_rects = []
            self.canvas.itemconfig(rect1, outline='black')
            self.canvas.itemconfig(rect2, outline='black')

    def on_arc_click(self, event, arc):
        self.current_arc = arc
        self.drag_start = event.x, event.y

    def on_arc_drag(self, event, arc):
        if arc == self.current_arc:
            x, y = event.x, event.y
            dx, dy = x - self.drag_start[0], y - self.drag_start[1]

            coords = self.canvas.coords(arc)
            if coords:
                x1, y1, ctrl_x1, ctrl_y1, x2, y2 = coords

                ctrl_x1 += dx
                ctrl_y1 += dy

                self.canvas.coords(arc, x1, y1, ctrl_x1, ctrl_y1, x2, y2)

                for i, (a, rect1, rect2, _) in enumerate(self.arcs):
                    if a == arc:
                        self.arcs[i] = (arc, rect1, rect2, (ctrl_x1, ctrl_y1))
                        print(self.arcs)
                        rect1_center = self._get_center(rect1)
                        rect2_center = self._get_center(rect2)
                        self._update_arc(arc, rect1_center, rect2_center, (ctrl_x1, ctrl_y1))
                        length = self._calculate_bezier_length(rect1_center, (ctrl_x1, ctrl_y1), rect2_center)
                        self.length_label.config(text=f"Arc Length: {length:.2f}")
                        break

            self.drag_start = x, y


if __name__ == "__main__":
    root = tk.Tk()
    app = ConnectNodesApp(root)
    root.mainloop()
