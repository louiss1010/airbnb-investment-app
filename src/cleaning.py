"""Cleaning functions for Inside Airbnb detailed listings.

Each function does one job and can be tested on its own.
clean_listings() runs them all in order and reports how many rows each rule removed,
which feeds straight into docs/data_quality.md.
"""
import pandas as pd

# Defaults agreed by the team; change them here and log the change in docs/decisions.md
MAX_MINIMUM_NIGHTS = 30            # longer minimum stays aren't short-term lets
EXCLUDED_ROOM_TYPES = ("Hotel room",)
DATE_COLUMNS = ("first_review", "last_review")


def clean_price(prices: pd.Series) -> pd.Series:
    """'$1,250.00' -> 1250.0. Blanks and unparseable values become NaN."""
    return pd.to_numeric(
        prices.astype("string").str.replace(r"[^0-9.]", "", regex=True),
        errors="coerce",
    ).astype("float64")


def bathrooms_from_text(text: pd.Series) -> pd.Series:
    """'1.5 shared baths' -> 1.5, 'Half-bath' -> 0.5, blank -> NaN."""
    text = text.astype("string").str.lower()
    number = pd.to_numeric(text.str.extract(r"(\d+(?:\.\d+)?)")[0], errors="coerce")
    is_half = text.str.contains("half-bath", na=False) & number.isna()
    return number.mask(is_half, 0.5).astype("float64")


def is_shared_bathroom(text: pd.Series) -> pd.Series:
    """True if the bathroom text says 'shared'. Blank -> False."""
    return text.astype("string").str.lower().str.contains("shared", na=False).astype(bool)


def parse_dates(df: pd.DataFrame, columns=DATE_COLUMNS) -> pd.DataFrame:
    """Convert date text columns to datetimes. Bad or blank values become NaT."""
    df = df.copy()
    for col in columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def fill_reviews_per_month(df: pd.DataFrame) -> pd.DataFrame:
    """reviews_per_month is blank when a listing has no reviews: that means 0, not unknown."""
    df = df.copy()
    no_reviews = df["number_of_reviews"].fillna(0) == 0
    df.loc[no_reviews, "reviews_per_month"] = df.loc[no_reviews, "reviews_per_month"].fillna(0)
    return df


def clean_listings(
    df: pd.DataFrame,
    max_minimum_nights: int = MAX_MINIMUM_NIGHTS,
    excluded_room_types=EXCLUDED_ROOM_TYPES,
    drop_missing_price: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Apply every cleaning rule. Returns (clean_df, report).

    report has one row per filtering step with rows removed and rows remaining.
    """
    df = df.copy()
    steps = [("start", len(df))]

    # Fix types (no rows removed)
    df["price"] = clean_price(df["price"])
    df["bathrooms"] = bathrooms_from_text(df["bathrooms_text"]).fillna(df["bathrooms"])
    df["bathroom_shared"] = is_shared_bathroom(df["bathrooms_text"])
    df = parse_dates(df)
    df = fill_reviews_per_month(df)

    # Filters (each one logged)
    df = df[~df["room_type"].isin(excluded_room_types)]
    steps.append((f"remove room types {list(excluded_room_types)}", len(df)))

    df = df[df["minimum_nights"] <= max_minimum_nights]
    steps.append((f"remove minimum_nights > {max_minimum_nights}", len(df)))

    if drop_missing_price:
        df = df[df["price"].notna()]
        steps.append(("remove missing price", len(df)))

    report = pd.DataFrame(steps, columns=["step", "rows_remaining"])
    report["rows_removed"] = (-report["rows_remaining"].diff()).fillna(0).astype(int)
    return df.reset_index(drop=True), report
