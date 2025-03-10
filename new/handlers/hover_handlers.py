"""
Hover handlers module for functions related to hover effects on the plot.
Contains functions for handling mouse hover events on the plot.
"""
import numpy as np

import state

def find_nearest(x_click, y_click=None):
    """
    Find the nearest data point to the given coordinates
    
    Args:
        x_click: X coordinate
        y_click: Optional Y coordinate
        
    Returns:
        Tuple of (point, line_key) or (None, None) if no nearby point
    """
    if not state.plot_lines:
        return None, None
        
    min_dist = float('inf')
    nearest_point = None
    nearest_line = None
    
    for key, line in state.plot_lines.items():
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
                nearest_line = key
            if dist2 < min_dist:
                min_dist = dist2
                nearest_point = (x_data[idx], y_data[idx])
                nearest_line = key
                
    return nearest_point, nearest_line if min_dist < 0.02 else (None, None)

def on_hover(event):
    """
    Handle mouse hover events on the plot
    
    Args:
        event: Mouse event object
    """
    if not state.plot_lines:
        return
        
    if not event.inaxes == state.ax:
        clear_hover_elements()
        return
        
    x_hover = event.xdata
    y_hover = event.ydata
    
    if x_hover is None or y_hover is None:
        clear_hover_elements()
        return
        
    nearest_point, _ = find_nearest(x_hover)
    if nearest_point:
        x, y = nearest_point
        clear_hover_elements()
        state.hover_elements['line'] = state.ax.axvline(x=x, color='black', linestyle=':', alpha=0.5)
        state.hover_elements['text'] = state.ax.text(
            x, y + 0.1,
            f'V: {x:.3f}',
            bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'),
            ha='center', va='bottom'
        )
        state.canvas_plot.draw_idle()
    else:
        clear_hover_elements()

def clear_hover_elements():
    """
    Clear hover indicator elements from the plot
    """
    for element in state.hover_elements.values():
        if element:
            element.remove()
    state.hover_elements = {'text': None, 'line': None}
    if state.canvas_plot:
        state.canvas_plot.draw_idle()