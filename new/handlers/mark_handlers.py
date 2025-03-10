"""
Mark handlers module for functions related to marking points on the plot.
Contains functions for adding, removing, and managing marks.
"""
import numpy as np

import state
from handlers.hover_handlers import find_nearest

def onclick(event):
    """
    Handle mouse click events on the plot
    
    Args:
        event: Mouse event object
    """
    if not state.plot_lines:  # Don't allow marking if no plots exist
        return
        
    if event.inaxes == state.ax and event.button == 1:
        x_click = event.xdata
        y_click = event.ydata
        nearest_point, _ = find_nearest(x_click, y_click)
        
        if nearest_point:
            x, y = nearest_point
            # Add marker at the nearest point
            marker = state.ax.plot(x, y, 'ro', markersize=8, alpha=0.8)[0]
            
            # Add vertical dotted line
            vline = state.ax.axvline(x=x, color='black', linestyle=':', alpha=0.5)
            
            # Add text at bottom of vertical line
            text = state.ax.text(
                x, state.ax.get_ylim()[0],
                f'V: {x:.3f}',
                bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.7, ec='gray'),
                ha='center', va='bottom'
            )
            
            state.marked_points.append((marker, vline, text))
            state.canvas_plot.draw()

def undo_mark():
    """
    Remove the last marked point from the plot
    """
    if state.marked_points:
        marker, vline, text = state.marked_points.pop()
        marker.remove()
        vline.remove()
        text.remove()
        state.canvas_plot.draw()

def clear_marks():
    """
    Remove all marked points from the plot
    """
    while state.marked_points:
        marker, vline, text = state.marked_points.pop()
        marker.remove()
        vline.remove()
        text.remove()
    state.canvas_plot.draw()

def restore_marks(marks):
    """
    Restore marked points from saved data
    
    Args:
        marks: List of (marker, vline, text) tuples
    """
    for mark in marks:
        marker_data = mark[0].get_data()
        x_val = marker_data[0][0]
        y_val = marker_data[1][0]
        
        marker = state.ax.plot(x_val, y_val, 'ro', markersize=8, alpha=0.8)[0]
        vline = state.ax.axvline(x=x_val, color='black', linestyle=':', alpha=0.5)
        text = state.ax.text(
            x_val, state.ax.get_ylim()[0],
            f'V: {x_val:.3f}',
            bbox=dict(boxstyle='round,pad=0.5', fc='white', alpha=0.7, ec='gray'),
            ha='center', va='bottom'
        )
        state.marked_points.append((marker, vline, text))