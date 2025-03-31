def is_power_of_2(n):
    return (n > 0) and (n & (n - 1)) == 0

def irregular_percentage(perlist, block_name, first_prefix, first_val, second_prefix, second_val, start_wls, ssl_count):
    first_prefix_perlist = [
        [53.739503613945698, 46.260496386054442], 
        [24.675143494889796, 29.198554421768671, 46.126302083333333], 
        [53.944781037414966, 46.055218962585033], 
        [53.955410289115665, 46.044589710884335], 
        [53.845131802721078, 46.154868197278917], 
        [53.889641794217769, 46.110358205782311]
    ]
    
    # Append new patterns to the perlist
    update_perlist = []
    # max_patterns = len(perlist)
    # for i in range(0, ssl_count):
    #     first_prefix_perlist.append(pattern_fn.analyze_HLH_pattern(read_fn.read_data_for_key(block_name, 
    #     f"{first_prefix}_{first_val}_{second_prefix}_{i}", start_wls, ssl_count)))
    
    # print('first_prefix_perlist', first_prefix_perlist)

    element_counts = [len(lst) for lst in first_prefix_perlist]
    count_dict = {}
    for count in element_counts:
        count_dict[count] = count_dict.get(count, 0) + 1

    majority_length = max(count_dict, key=count_dict.get)
    if not is_power_of_2(majority_length):
        raise ValueError("Majority length is not a power of 2. Check data consistency.")

    # Step 2: Identify correct lists and find percentage ranges
    correct_lists = [lst for lst in perlist if len(lst) == majority_length]
    
    # Calculate min and max values for each percentage element (for both ranges)
    min_values1 = [min(values) for values in zip(*correct_lists)]
    max_values1 = [max(values) for values in zip(*correct_lists)]
    
    # Define ranges for the first and second elements
    range_start1, range_end1 = min_values1[0], max_values1[0]
    range_start2, range_end2 = min_values1[1], max_values1[1]

    # Round the ranges for readability
    rounded_ranges = [
        (int(min_val), int(max_val) + (1 if max_val - int(max_val) > 0.5 else 0))
        for min_val, max_val in zip(min_values1, max_values1)
    ]

    # Step 3: Identify and correct incorrect lists
    corrected_perlist = []
    for lst in perlist:
        if len(lst) != majority_length:
            # Sum progressively to get within the desired range for the first elements
            sum_value = 0
            for val in lst[:-1]: // make change here
                sum_value += val
                # Check if the sum is within the first range
                if range_start1 <= sum_value <= range_end1:
                    break  # We stop once the sum falls within the range
            # Check the last value (it should fall within the second range)
            last_value = lst[-1]
            if last_value < range_start2:
                last_value = range_start2
            elif last_value > range_end2:
                last_value = range_end2

            # Append corrected list
            new_list = [sum_value, last_value]  # Corrected sum and the last value
            corrected_perlist.append(new_list)

    # Step 4: Print results
    print(f"Majority length: {majority_length}")
    for i, (low, high) in enumerate(rounded_ranges, start=1):
        print(f"Percentage {i} range: {low}% - {high}%")

    # Return only the corrected lists and the count of corrected lists
    return corrected_perlist, len(corrected_perlist)

# Sample Data
perlist = [
    [53.739503613945698, 46.260496386054442], 
    [24.675143494889796, 29.198554421768671, 46.126302083333333],  # Incorrect
    [53.944781037414966, 46.055218962585033], 
    [53.955410289115665, 46.044589710884335], 
    [53.845131802721078, 46.154868197278917], 
    [53.889641794217769, 46.110358205782311]
]

# Run processing function and get corrected lists
corrected_perlist, corrected_count = irregular_percentage(perlist, 'block_name', 'first_prefix', 1, 'second_prefix', 2, 0, 2)

# Print corrected lists and their count
print("Corrected Lists:")
for lst in corrected_perlist:
    print(lst)

print(f"Total corrected lists: {corrected_count}")
