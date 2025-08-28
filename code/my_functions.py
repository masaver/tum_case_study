def normalize_intensity_by_reference(row, reference_channel, list_of_batches):

    """
    Normalizes intensity values in a dataset based on a reference channel for each batch.
    Intensities are scaled back to their original value range using the median of all reference intensity values.

    Parameters:
        row (pd.Series): The data row containing intensity values.
        reference_channel (str): The name of the reference channel to normalize by.
        list_of_batches (list): List of batch identifiers to process.

    Returns:
        pd.Series: The normalized intensity values for the row.
    """

    # Extract intensity values for the reference channel across all batches
    reference_values = row[row.index.str.startswith(f'Reporter intensity corrected {reference_channel} ')]

    # Remove zero values and calculate the median of the non-zero reference intensities
    non_zero_references = reference_values[reference_values != 0]
    reference_median = non_zero_references.median() if not non_zero_references.empty else 0

    # Create a mask to identify all channels starting with "Reporter intensity corrected"
    reporter_mask = row.index.str.startswith("Reporter intensity corrected ")

    # Initialize a dictionary to store the normalized values
    res_dict = row.to_dict()

    # Iterate through each batch
    for batch in list_of_batches:
        # Extract reference intensity for the current batch
        reference_col = f'Reporter intensity corrected {reference_channel} {batch}'
        reference_intensity = row.get(reference_col, 0)

        # Identify all channels for the current batch
        batch_channels_mask = reporter_mask & row.index.str.endswith(f" {batch}")
        batch_values = row[batch_channels_mask]

        # Normalize batch values using reference intensity, if non-zero
        if reference_intensity != 0:
            normalized_values = (batch_values / reference_intensity) * reference_median
        else:
            normalized_values = pd.Series(0, index=batch_values.index)

        # Update the result dictionary with the normalized values
        res_dict.update(normalized_values.to_dict())

    return pd.Series(res_dict)