import numpy as np
import pandas as pd

from src.cleaning import (
    bathrooms_from_text,
    clean_listings,
    clean_price,
    fill_reviews_per_month,
    is_shared_bathroom,
    parse_dates,
)


# ---------- clean_price ----------
def test_clean_price_strips_symbols_and_commas():
    result = clean_price(pd.Series(["$1,250.00", "£95.00", "$60"]))
    assert result.tolist() == [1250.0, 95.0, 60.0]


def test_clean_price_blank_becomes_nan():
    result = clean_price(pd.Series([None, "", np.nan]))
    assert result.isna().all()


def test_clean_price_already_numeric():
    assert clean_price(pd.Series([80.0, 120])).tolist() == [80.0, 120.0]


# ---------- bathrooms ----------
def test_bathrooms_from_text_numbers():
    result = bathrooms_from_text(pd.Series(["1 bath", "1.5 shared baths", "2 private baths"]))
    assert result.tolist() == [1.0, 1.5, 2.0]


def test_bathrooms_from_text_half_bath():
    result = bathrooms_from_text(pd.Series(["Half-bath", "Shared half-bath", "Private half-bath"]))
    assert result.tolist() == [0.5, 0.5, 0.5]


def test_bathrooms_from_text_blank():
    assert bathrooms_from_text(pd.Series([None])).isna().all()


def test_is_shared_bathroom():
    result = is_shared_bathroom(pd.Series(["1.5 shared baths", "1 bath", None]))
    assert result.tolist() == [True, False, False]


# ---------- dates and reviews ----------
def test_parse_dates():
    df = parse_dates(pd.DataFrame({"first_review": ["2023-05-01", None],
                                   "last_review": ["2025-01-10", "not a date"]}))
    assert pd.api.types.is_datetime64_any_dtype(df["first_review"])
    assert df["last_review"].isna().tolist() == [False, True]


def test_fill_reviews_per_month_only_when_no_reviews():
    df = pd.DataFrame({"number_of_reviews": [0, 5], "reviews_per_month": [np.nan, np.nan]})
    result = fill_reviews_per_month(df)
    assert result["reviews_per_month"].iloc[0] == 0
    assert np.isnan(result["reviews_per_month"].iloc[1])  # has reviews but no rate: leave as unknown


# ---------- clean_listings ----------
def make_listings():
    return pd.DataFrame({
        "price": ["$100.00", "$2,000.00", None, "$80.00", "$50.00"],
        "room_type": ["Entire home/apt", "Hotel room", "Private room", "Entire home/apt", "Private room"],
        "minimum_nights": [2, 1, 3, 1125, 1],
        "bathrooms": [np.nan, 1, np.nan, 1, np.nan],
        "bathrooms_text": ["1.5 baths", "1 bath", "Half-bath", "1 bath", "1 shared bath"],
        "first_review": ["2023-01-01"] * 5,
        "last_review": ["2025-06-01"] * 5,
        "number_of_reviews": [10, 3, 0, 4, 0],
        "reviews_per_month": [1.2, 0.3, np.nan, 0.5, np.nan],
    })


def test_clean_listings_filters():
    clean, report = clean_listings(make_listings())
    # hotel removed, 1125-night minimum removed, missing price removed -> 2 rows left
    assert len(clean) == 2
    assert "Hotel room" not in clean["room_type"].values
    assert clean["minimum_nights"].max() <= 30
    assert clean["price"].notna().all()


def test_clean_listings_report_adds_up():
    raw = make_listings()
    clean, report = clean_listings(raw)
    assert report["rows_removed"].sum() == len(raw) - len(clean)
    assert report["rows_remaining"].iloc[-1] == len(clean)


def test_clean_listings_types():
    clean, _ = clean_listings(make_listings())
    assert clean["price"].dtype == float
    assert clean["bathrooms"].tolist() == [1.5, 1.0]
    assert clean["reviews_per_month"].notna().all()


def test_clean_listings_does_not_change_input():
    raw = make_listings()
    before = raw.copy()
    clean_listings(raw)
    pd.testing.assert_frame_equal(raw, before)
