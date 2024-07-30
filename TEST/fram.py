import tkinter as tk
import math

class ConnectNodesApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack()

        self.rectangles = []
        self.obstacles = []
        self.arcs = []
        self.selected_rects = []

        self.create_rectangles()
        self.create_obstacles()
        self.connect_button = tk.Button(root, text="Connect Selected Rectangles", command=self.connect_rectangles)
        self.connect_button.pack()

        self.current_arc = None
        self.drag_start = None

        self.length_label = tk.Label(root, text="Arc Length: 0.00")
        self.length_label.pack()

    def create_rectangles(self):
        rect1 = self.canvas.create_rectangle(100, 100, 150, 150, outline='black', fill='white')  # 长方形
        rect2 = self.canvas.create_rectangle(300, 100, 350, 150, outline='black', fill='white')
        rect3 = self.canvas.create_rectangle(100, 300, 150, 350, outline='black', fill='white')
        rect4 = self.canvas.create_rectangle(300, 300, 350, 350, outline='black', fill='white')

        self.rectangles.extend([rect1, rect2, rect3, rect4])

        for rect in self.rectangles:
            self.canvas.tag_bind(rect, '<ButtonPress-1>', self.on_rect_click)
            self.canvas.tag_bind(rect, '<B1-Motion>', self.on_rect_drag)

    def create_obstacles(self):
        obstacle1 = self.canvas.create_rectangle(200, 120, 210, 130, outline='black', fill='grey')
        obstacle2 = self.canvas.create_rectangle(200, 320, 210, 330, outline='black', fill='grey')

        self.obstacles.extend([obstacle1, obstacle2])

        for obstacle in self.obstacles:
            self.canvas.tag_bind(obstacle, '<ButtonPress-1>', self.on_obstacle_click)
            self.canvas.tag_bind(obstacle, '<B1-Motion>', self.on_obstacle_drag)

    def _get_center(self, rect):
        x1, y1, x2, y2 = self.canvas.coords(rect)
        return (x1 + x2) / 2, (y1 + y2) / 2

    def _create_arc(self, start, end):
        x1, y1 = start
        x2, y2 = end

        # Define control points for the cubic Bezier curve
        ctrl1_x = x1 + 100
        ctrl1_y = y1
        ctrl2_x = x2 - 100
        ctrl2_y = y2

        arc = self.canvas.create_line(x1, y1, ctrl1_x, ctrl1_y, ctrl2_x, ctrl2_y, x2, y2, smooth=True, width=2, fill='blue')
        self.canvas.tag_bind(arc, '<ButtonPress-1>', lambda event, arc=arc: self.on_arc_click(event, arc))
        self.canvas.tag_bind(arc, '<B1-Motion>', lambda event, arc=arc: self.on_arc_drag(event, arc))

        # Calculate initial length of the arc
        length = self._calculate_bezier_length((x1, y1), (ctrl1_x, ctrl1_y), (ctrl2_x, ctrl2_y), (x2, y2))
        self.length_label.config(text=f"Arc Length: {length:.2f}")

        return arc, [ctrl1_x, ctrl1_y, ctrl2_x, ctrl2_y]

    def _update_arc(self, arc, start, end, control_points):
        self.canvas.coords(arc, *self._calculate_arc_coords(start, end, control_points))

    def _calculate_arc_coords(self, start, end, control_points):
        x1, y1 = start
        x2, y2 = end
        ctrl1_x, ctrl1_y, ctrl2_x, ctrl2_y = control_points

        return x1, y1, ctrl1_x, ctrl1_y, ctrl2_x, ctrl2_y, x2, y2

    def _calculate_bezier_length(self, p0, p1, p2, p3, num_points=100):
        def bezier(t, p0, p1, p2, p3):
            return ((1 - t)**3 * p0[0] + 3 * (1 - t)**2 * t * p1[0] + 3 * (1 - t) * t**2 * p2[0] + t**3 * p3[0],
                    (1 - t)**3 * p0[1] + 3 * (1 - t)**2 * t * p1[1] + 3 * (1 - t) * t**2 * p2[1] + t**3 * p3[1])

        length = 0
        prev_point = p0
        for i in range(1, num_points + 1):
            t = i / num_points
            current_point = bezier(t, p0, p1, p2, p3)
            segment_length = math.sqrt((current_point[0] - prev_point[0])**2 + (current_point[1] - prev_point[1])**2)
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

        for arc, rect1, rect2, control_points in self.arcs:
            if rect in (rect1, rect2):
                rect1_center = self._get_center(rect1)
                rect2_center = self._get_center(rect2)
                self._update_arc(arc, rect1_center, rect2_center, control_points)
                length = self._calculate_bezier_length(rect1_center, control_points[:2], control_points[2:], rect2_center)
                self.length_label.config(text=f"Arc Length: {length:.2f}")

    def on_obstacle_click(self, event):
        obstacle = self.canvas.find_withtag(tk.CURRENT)[0]
        self.drag_data = {'x': event.x, 'y': event.y, 'obstacle': obstacle}

    def on_obstacle_drag(self, event):
        obstacle = self.drag_data['obstacle']
        x, y = event.x, event.y
        dx, dy = x - self.drag_data['x'], y - self.drag_data['y']

        self.canvas.move(obstacle, dx, dy)
        self.drag_data = {'x': x, 'y': y}

        for arc, start, end, control_points in self.arcs:
            if start == obstacle or end == obstacle:
                start_center = start
                end_center = end
                self._update_arc(arc, start_center, end_center, control_points)
                length = self._calculate_bezier_length(start_center, control_points[:2], control_points[2:], end_center)
                self.length_label.config(text=f"Arc Length: {length:.2f}")

    def connect_rectangles(self):
        if len(self.selected_rects) == 2:
            rect1, rect2 = self.selected_rects
            rect1_center = self._get_center(rect1)
            rect2_center = self._get_center(rect2)

            obstacle_start, obstacle_end = self._get_closest_obstacles(rect1_center, rect2_center)
            if obstacle_start and obstacle_end:
                # 将 rect1 连接到 obstacle_start
                self.canvas.create_line(rect1_center, obstacle_start, width=2, fill='red')

                # 在 obstacle_start 和 obstacle_end 之间创建贝塞尔弧
                arc, control_points = self._create_arc(obstacle_start, obstacle_end)
                self.arcs.append((arc, obstacle_start, obstacle_end, control_points))

                # 将 obstacle_end 连接到 rect2
                self.canvas.create_line(obstacle_end, rect2_center, width=2, fill='red')
            else:
                arc, control_points = self._create_arc(rect1_center, rect2_center)
                self.arcs.append((arc, rect1, rect2, control_points))

    def _get_closest_obstacles(self, start, end):
        start_obstacle = None
        end_obstacle = None
        min_start_dist = float('inf')
        min_end_dist = float('inf')

        for obstacle in self.obstacles:
            obstacle_center = self._get_center(obstacle)
            start_dist = math.sqrt((obstacle_center[0] - start[0])**2 + (obstacle_center[1] - start[1])**2)
            end_dist = math.sqrt((obstacle_center[0] - end[0])**2 + (obstacle_center[1] - end[1])**2)

            if start_dist < min_start_dist:
                min_start_dist = start_dist
                start_obstacle = obstacle_center

            if end_dist < min_end_dist:
                min_end_dist = end_dist
                end_obstacle = obstacle_center

        return start_obstacle, end_obstacle

    def on_arc_click(self, event, arc):
        self.current_arc = arc
        self.drag_start = (event.x, event.y)

    def on_arc_drag(self, event, arc):
        if arc == self.current_arc:
            x, y = event.x, event.y
            dx, dy = x - self.drag_start[0], y - self.drag_start[1]

            coords = self.canvas.coords(arc)
            if coords:
                x1, y1, ctrl1_x, ctrl1_y, ctrl2_x, ctrl2_y, x2, y2 = coords
                ctrl1_x += dx
                ctrl1_y += dy
                ctrl2_x += dx
                ctrl2_y += dy

                self.canvas.coords(arc, x1, y1, ctrl1_x, ctrl1_y, ctrl2_x, ctrl2_y, x2, y2)

                for arc_data in self.arcs:
                    if arc_data[0] == arc:
                        arc_data[3] = [ctrl1_x, ctrl1_y, ctrl2_x, ctrl2_y]
                        length = self._calculate_bezier_length((x1, y1), (ctrl1_x, ctrl1_y), (ctrl2_x, ctrl2_y), (x2, y2))
                        self.length_label.config(text=f"Arc Length: {length:.2f}")

                self.drag_start = event.x, event.y

if __name__ == "__main__":
    root = tk.Tk()
    app = ConnectNodesApp(root)
    root.mainloop()
