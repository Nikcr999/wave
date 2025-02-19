import numpy as np

def find_nearest(self, x_click, y_click=None):
    if not self.plot_lines:  # Return if no plots exist
        return None, None
        
    min_dist = float('inf')
    nearest_point = None
    nearest_line = None
    
    for (wls, ssl), line in self.plot_lines.items():
        x_data = line.get_xdata()
        y_data = line.get_ydata()
        
        idx = np.searchsorted(x_data, x_click)
        if idx > 0 and idx < len(x_data):
            if y_click is not None:
                dist1 = np.sqrt((x_data[idx-1] - x_click)**2 + (y_data[idx-1] - y_click)**2)
                dist2 = np.sqrt((x_data[idx] - x_click)**2 + (y_data[idx] - y_click)**2)
            else:
                dist1 = abs(x_data[idx-1] - x_click)
                dist2 = abs(x_data[idx] - x_click)
            
            if dist1 < min_dist:
                min_dist = dist1
                nearest_point = (x_data[idx-1], y_data[idx-1])
                nearest_line = (wls, ssl)
            if dist2 < min_dist:
                min_dist = dist2
                nearest_point = (x_data[idx], y_data[idx])
                nearest_line = (wls, ssl)
                
    return nearest_point, nearest_line if min_dist < 0.02 else (None, None)

def on_hover(self, event):
    if not self.plot_lines:  # Don't show hover if no plots exist
        return
        
    if not event.inaxes == self.ax:
        self._clear_hover_elements()
        return
        
    x_hover = event.xdata
    y_hover = event.ydata
    
    if x_hover is None or y_hover is None:
        self._clear_hover_elements()
        return
        
    nearest_point, _ = self.find_nearest(x_hover)
    if nearest_point:
        x, y = nearest_point
        self._clear_hover_elements()
        self.hover_elements['line'] = self.ax.axvline(x=x, color='black', linestyle=':', alpha=0.5)
        self.hover_elements['text'] = self.ax.text(
            x, y + 0.1,
            f'V: {x:.3f}',
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'),
            ha='center', va='bottom'
        )
        self.canvas_plot.draw_idle()
    else:
        self._clear_hover_elements()

def _clear_hover_elements(self):
    if hasattr(self, 'hover_elements'):
        for element in self.hover_elements.values():
            if element:
                element.remove()
        self.hover_elements = {'text': None, 'line': None}
        self.canvas_plot.draw_idle()