def onclick(self, event):
    if event.inaxes == self.ax and hasattr(self, 'x_data'):
        x_click = event.xdata
        if x_click is None:
            return
        
        x_val, y_val = self.find_nearest(x_click)
        vline = self.ax.axvline(x=x_val, color='r', linestyle=':', alpha=0.5)
        marker = self.ax.plot(x_val, y_val, 'ro')
        text_label = self.ax.text(x_val, min(self.y_data) - 0.1,
                                f"{x_val:.2f}",
                                fontsize=9, color='black', ha='center')
        
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