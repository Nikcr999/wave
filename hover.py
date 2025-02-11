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
    if event.inaxes == self.ax and hasattr(self, 'x_data'):
        x_hover = event.xdata
        if x_hover is None:
            return

        x_val, y_val = self.find_nearest(x_hover)

        if hasattr(self, 'hover_text') and self.hover_text:
            self.hover_text.remove()
        if hasattr(self, 'hover_arrow') and self.hover_arrow:
            self.hover_arrow.remove()
        if hasattr(self, 'hover_line') and self.hover_line:
            self.hover_line.remove()

        self.hover_line = self.ax.axvline(x=x_val, color='black', linestyle='dotted', alpha=0.7)

        arrow_x_offset = 50
        arrow_y_offset = 0.3
        self.hover_arrow = self.ax.annotate("", xy=(x_val, y_val),
                                          xytext=(x_val + arrow_x_offset, y_val + arrow_y_offset),
                                          arrowprops=dict(arrowstyle="->", color='black'))

        self.hover_text = self.ax.text(x_val + arrow_x_offset, y_val + arrow_y_offset + 0.1, f"{y_val:.2f}",
                                     fontsize=9, color='black', ha='center',
                                     bbox=dict(facecolor='white', alpha=0.7))

        self.canvas_plot.draw_idle()
    else:
        if hasattr(self, 'hover_text') and self.hover_text:
            self.hover_text.remove()
            self.hover_text = None
        if hasattr(self, 'hover_arrow') and self.hover_arrow:
            self.hover_arrow.remove()
            self.hover_arrow = None
        if hasattr(self, 'hover_line') and self.hover_line:
            self.hover_line.remove()
            self.hover_line = None

        self.canvas_plot.draw_idle()