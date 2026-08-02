def select_columns(dataframe, columns):

    return dataframe[columns].copy()

def fill_missing_text(dataframe, columns, value="Unknown"):

    dataframe_copy = dataframe.copy()

    for column in columns:
        dataframe_copy[column] = (
            dataframe_copy[column]
            .fillna(value)
        )

    return dataframe_copy
