def onclick(self, event):
    if event.inaxes == self.ax and hasattr(self, 'plot_lines'):
        x_click = event.xdata
        if x_click is None:
            return

        min_dist = float('inf')
        closest_x, closest_y = None, None

        for key, line in self.plot_lines.items():
            x_data = line.get_xdata()
            y_data = line.get_ydata()
            idx = np.searchsorted(x_data, x_click)
            if idx == 0:
                x_val, y_val = x_data[0], y_data[0]
            elif idx >= len(x_data):
                x_val, y_val = x_data[-1], y_data[-1]
            else:
                x1, x2 = x_data[idx - 1], x_data[idx]
                y1, y2 = y_data[idx - 1], y_data[idx]
                slope = (y2 - y1) / (x2 - x1)
                y_val = y1 + slope * (x_click - x1)
                x_val = x_click

            dist = (x_click - x_val) ** 2
            if dist < min_dist:
                min_dist = dist
                closest_x, closest_y = x_val, y_val

        if closest_x is not None:
            vline = self.ax.axvline(x=closest_x, color='r', linestyle=':', alpha=0.5)
            marker, = self.ax.plot(closest_x, closest_y, 'ro')
            text_label = self.ax.text(closest_x, closest_y, f"{closest_x:.2f}", fontsize=9, color='black', ha='center')

            self.marked_points.append((vline, marker, text_label))
            self.canvas_plot.draw_idle()


def undo_mark(self):
    if self.marked_points:
        vline, marker, text_label = self.marked_points.pop()
        vline.remove()
        marker[0].remove()
        text_label.remove()
        self.canvas_plot.draw_idle()

def clear_marks(self):
    while self.marked_points:
        self.undo_mark()
