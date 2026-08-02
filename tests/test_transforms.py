import pytest
import pandas as pd
from scripts.transforms import (
    fill_missing_text,
    select_columns
)


def test_select_columns():

    dataframe = pd.DataFrame(
        {
            "id": [1, 2],
            "name": ["Airport A", "Airport B"],
            "country": ["IT", "FR"]
        }
    )

    result = select_columns(
        dataframe,
        ["id", "name"]
    )

    assert list(result.columns) == ["id", "name"]


def test_fill_missing_text():

    dataframe = pd.DataFrame(
        {
            "city": ["Rome", None, "Paris"]
        }
    )

    result = fill_missing_text(
        dataframe,
        ["city"]
    )

    assert result.loc[1, "city"] == "Unknown"


def test_fill_missing_text_multiple_columns():

    dataframe = pd.DataFrame(
        {
            "city": ["Rome", None, "Paris"],
            "country": ["Italy", "France", None]
        }
    )

    result = fill_missing_text(
        dataframe,
        ["city", "country"],
        value="Missing"
    )

    assert result.loc[1, "city"] == "Missing"
    assert result.loc[2, "country"] == "Missing"


def test_select_columns_returns_copy():

    dataframe = pd.DataFrame(
        {
            "id": [1, 2],
            "name": ["Airport A", "Airport B"],
            "country": ["IT", "FR"]
        }
    )

    result = select_columns(
        dataframe,
        ["id", "name"]
    )

    result.loc[0, "name"] = "Modified Airport"

    assert dataframe.loc[0, "name"] == "Airport A"


def test_select_columns_raises_error_for_missing_column():

    dataframe = pd.DataFrame(
        {
            "id": [1, 2],
            "name": ["Airport A", "Airport B"]
        }
    )

    with pytest.raises(KeyError):

        select_columns(
            dataframe,
            ["id", "country"]
        )

def test_fill_missing_text_returns_copy():

    dataframe = pd.DataFrame(
        {
            "city": ["Rome", None, "Paris"]
        }
    )

    result = fill_missing_text(
        dataframe,
        ["city"]
    )

    assert pd.isna(dataframe.loc[1, "city"])
    assert result.loc[1, "city"] == "Unknown"
    assert result is not dataframe


def test_fill_missing_text_raises_error_for_missing_column():

    dataframe = pd.DataFrame(
        {
            "city": ["Rome", None, "Paris"]
        }
    )

    with pytest.raises(KeyError):

        fill_missing_text(
            dataframe,
            ["country"]
        )