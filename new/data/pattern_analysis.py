"""
Pattern Analysis module for analyzing data patterns.
Contains functions for analyzing low-high-low patterns in data.
"""
import numpy as np

import state
from data.file_reader import read_data_for_key
from ui.table import update_pattern_analysis_table

def analyze_low_high_low_patterns(data):
    """
    Analyzes data to identify low-high-low patterns and calculates percentage values
    
    Args:
        data: List of numerical values
        
    Returns:
        Dictionary containing patterns and percentages
    """
    if len(data) < 3:
        return {'patterns': [], 'percentages': []}
        
    patterns = []
    percentages = []
    
    i = 0
    while i < len(data) - 2:
        if data[i] < data[i+1]:
            start_idx = i
            j = i + 1
            while j < len(data) - 1 and data[j] < data[j+1]:
                j += 1
            peak_idx = j
            
            if j < len(data) - 1 and data[j] > data[j+1]:
                k = j + 1
                while k < len(data) - 1 and data[k] > data[k+1]:
                    k += 1
                end_idx = k
                
                patterns.append((start_idx, peak_idx, end_idx))
                i = end_idx
            else:
                i = j + 1
        else:
            i += 1
    
    total_sum = sum(data)
    if total_sum > 0:
        for start, peak, end in patterns:
            pattern_sum = sum(data[start:end+1])
            percentage = (pattern_sum / total_sum) * 100
            percentages.append(round(percentage, 2))
    
    return {
        'patterns': patterns,
        'percentages': percentages
    }

def analyze_selected_data(selected_key):
    """
    Analyze a selected data series
    
    Args:
        selected_key: Key of the data series to analyze
        
    Returns:
        Dictionary with pattern analysis results
    """
    data = read_data_for_key(selected_key)
    if not data:
        return None
        
    return analyze_low_high_low_patterns(data)

def analyze_all_selected_data(selected_keys):
    """
    Analyze all selected data series and update pattern analysis table
    
    Args:
        selected_keys: List of keys for the data series to analyze
    """
    if not selected_keys:
        # Clear pattern analysis if no keys are selected
        from ui.table import clear_pattern_analysis
        clear_pattern_analysis()
        return
    
    # Store the current pattern data    
    current_keys = set(selected_keys)
    
    # If pattern_data exists, remove keys that are no longer selected
    old_keys = set(state.pattern_data.keys())
    removed_keys = old_keys - current_keys
    
    for key in removed_keys:
        # Remove pattern analysis for this key
        if key in state.pattern_data:
            del state.pattern_data[key]
    
    # Analyze each selected key
    for key in selected_keys:
        result = analyze_selected_data(key)
        if result:
            # Store pattern data
            state.pattern_data[key] = result
    
    # Update the pattern analysis table
    update_pattern_analysis_table()