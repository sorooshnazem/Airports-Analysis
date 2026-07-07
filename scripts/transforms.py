def select_columns(dataframe, columns):

    return dataframe[columns].copy()

def fill_missing_text(dataframe, columns, value="Unknown"):

    for column in columns:
        dataframe[column] = dataframe[column].fillna(value)

    return dataframe
