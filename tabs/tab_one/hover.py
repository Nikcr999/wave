import numpy as np

def find_nearest(self, x_click):
    idx = np.searchsorted(self.x_data, x_click)
    if idx == 0:
        return self.x_data[0], self.y_data[0]
    elif idx >= len(self.x_data):
        return self.x_data[-1], self.y_data[-1]
    else:
        x1, x2 = self.x_data[idx - 1], self.x_data[idx]
        y1, y2 = self.y_data[idx - 1], self.y_data[idx]
        slope = (y2 - y1) / (x2 - x1)
        y_click = y1 + slope * (x_click - x1)
        return x_click, y_click

def on_hover(self, event):
    if event.inaxes == self.ax:
        x_hover = event.xdata
        y_hover = event.ydata
        if x_hover is None or y_hover is None:
            if hasattr(self, 'hover_text') and self.hover_text:
                self.hover_text.remove()
                self.hover_text = None
            if hasattr(self, 'hover_line') and self.hover_line:
                self.hover_line.remove()
                self.hover_line = None
            self.canvas_plot.draw_idle()
            return

        if hasattr(self, 'hover_text') and self.hover_text:
            self.hover_text.remove()
        if hasattr(self, 'hover_line') and self.hover_line:
            self.hover_line.remove()

        min_dist = float('inf')
        closest_line = None
        closest_x = None
        closest_y = None

        for (wls, ssl), line in self.plot_lines.items():
            x_data = line.get_xdata()
            y_data = line.get_ydata()
            idx = np.searchsorted(x_data, x_hover)
            if idx == 0:
                x_val, y_val = x_data[0], y_data[0]
            elif idx >= len(x_data):
                x_val, y_val = x_data[-1], y_data[-1]
            else:
                x1, x2 = x_data[idx - 1], x_data[idx]
                y1, y2 = y_data[idx - 1], y_data[idx]
                slope = (y2 - y1) / (x2 - x1)
                y_hover_line = y1 + slope * (x_hover - x1)
                x_val, y_val = x_hover, y_hover_line

            dist = np.sqrt((x_hover - x_val)**2 + (y_hover - y_val)**2)

            if dist < min_dist:
                min_dist = dist
                closest_line = line
                closest_x = x_val
                closest_y = y_val

        if closest_x is not None:
            self.hover_line = self.ax.axvline(x=closest_x, color='r', linestyle=':', alpha=0.5)
            self.hover_text = self.ax.text(closest_x, closest_y, f"{closest_x:.2f}",
                                           fontsize=9, color='r', ha='center')
        else:
            if hasattr(self, 'hover_text') and self.hover_text:
                self.hover_text.remove()
                self.hover_text = None
            if hasattr(self, 'hover_line') and self.hover_line:
                self.hover_line.remove()
                self.hover_line = None

        self.canvas_plot.draw_idle()
    else:
        if hasattr(self, 'hover_text') and self.hover_text:
            self.hover_text.remove()
            self.hover_text = None
        if hasattr(self, 'hover_line') and self.hover_line:
            self.hover_line.remove()
            self.hover_line = None

        self.canvas_plot.draw_idle()
