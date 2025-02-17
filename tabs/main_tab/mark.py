import numpy as np

def onclick(self, event):
    if event.inaxes == self.ax and event.button == 1:
        x_click = event.xdata
        y_click = event.ydata
        nearest_point, _ = self.find_nearest(x_click, y_click)
        
        if nearest_point:
            x, y = nearest_point
            marker = self.ax.plot(x, y, 'ro', markersize=8, alpha=0.8)[0]
            vline = self.ax.axvline(x=x, color='black', linestyle=':', alpha=0.5)
            
            text = self.ax.text(
                x, self.ax.get_ylim()[0],
                f'V: {x:.3f}',
                bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.7, ec='gray'),
                ha='center', va='bottom'
            )
            
            self.marked_points.append((marker, vline, text))
            self.canvas_plot.draw()

def undo_mark(self):
    if self.marked_points:
        marker, vline, text = self.marked_points.pop()
        marker.remove()
        vline.remove()
        text.remove()
        self.canvas_plot.draw()

def clear_marks(self):
    while self.marked_points:
        marker, vline, text = self.marked_points.pop()
        marker.remove()
        vline.remove()
        text.remove()
    self.canvas_plot.draw()