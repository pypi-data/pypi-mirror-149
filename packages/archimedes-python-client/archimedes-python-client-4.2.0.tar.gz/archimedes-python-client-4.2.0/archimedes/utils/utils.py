from typing import Dict

import pandas as pd


def create_composite_id(
    series_id: str,
    price_area: str = None,
    quantile: str = None,
    hours_ahead: pd.Timedelta = None,
) -> str:
    """Create a composite ID for a time series.

    The time series can be a data series, or a prediction series.
    For data series, eg. Nordpool data, the composite ID will be similar to:

        NP/ConsumptionImbalancePrices:NO2

    where NP/ConsConsumptionImbalancePrices is the series_id, and NO2 is the price_area.

    For predictions, the composite ID will be something like:
        PX/rk-naive:NO2:H4:Q50

    where PX/rk-naive is the series_id, NO2 is the price area,
    H4 is "four hours ahead" and Q50 is quantile 50.

    Example:
        >>> import pandas as pd
        >>> h = pd.Timedelta(3, "hours")
        >>> create_composite_id(
        >>>     series_id="PX/my-prediction, price_area="NO2", hours_ahead=h, quantile=50
        >>> )
        ""
        {
            "series_id": "PX/my-prediction",
            "price_area": "NO2",
            "hours_ahead": 3,
            "quantile": 50
        }

    Args:
        series_id (str): The series ID.
        price_area (str, optional): The price area. Defaults to None.
        quantile (str, optional): The quantile. Defaults to None.
        hours_ahead (pd.Timedelta, optional):
            Number of hours the timestamp of the predicted value is ahead of the
            reference timestamp for the prediction.

    Returns:
        str: The composite id
    """
    if isinstance(hours_ahead, pd.Timedelta):
        # Converting the timedelta to an integer
        hours_ahead_ = int(hours_ahead.seconds / 3600)
    elif hours_ahead == None:
        pass
    else:
        raise TypeError(
            f"Invalid type {type(hours_ahead)} for hours_ahead: {hours_ahead}>.\n"
            + "Consider using pd.to_timedelta() to convert."
        )

    ordered_parts = [
        series_id,
        price_area,
        f"H{hours_ahead_}" if hours_ahead else None,
        f"Q{quantile}" if quantile else None,
    ]

    nones_removed = [part for part in ordered_parts if part != None]

    composite_id = ":".join(nones_removed)

    return composite_id


def composite_id_to_attributes(composite_id: str) -> Dict:
    """Expand a composite ID to a dict of attributes.

    Since we will often be working with the composite IDs for the
    time series – and since they are an easy way to carry metadata
    about the predictions around, it is useful to be able to do the
    reverse operation of `create_composite_id`.

    A dataframe with columns:
        (dt, composite_id, value)
    can then easily be converted into a dataframe with columns:
        (dt, series_id, hours_ahead, quantile, ...)

    Example (simple):
        >>> composite_id = "PX/rk-nn:NO2:H3:Q90
        >>> composite_id_to_attribute(composite_id)
        {"series_id": "PX/rk-nn", "price_area": "NO2", "hours_ahead": 3, "quantile": 90}

    Example (dataframe):
        >>> df = pd.DataFrame(
        >>>     [
        >>>         ["17:00", "PX/rk-nn:NO2:H3:Q50", 28.43],
        >>>         ["17:00", "PX/rk-nn:NO2:H3:Q90", 31.11]
        >>>     ],
        >>>     columns=["from_dt", "composite_id", "value"]
        >>> )
        >>> dfa = pd.concat(
        >>>     [
        >>>         df,
        >>>         df["composite_id"].apply(
        >>>             composite_id_to_attributes
        >>>         ).apply(
        >>>             pd.Series
        >>>         )
        >>>     ],
        >>>     axis=1
        >>> )
        ...

    Args:
        composite_id (str): The composite ID

    Returns:
        Dict[]: A dictionary of all the attributes
    """
    attributes = {}
    elements = composite_id.split(":")
    series_id, *rest = elements
    attributes["series_id"] = series_id

    for r in rest:
        # Hours ahead part ->
        if "H" in r:
            attributes["hours_ahead"] = pd.Timedelta(int(r[1:]), "hours")
        # Quantile part ->
        elif "Q" in r:
            attributes["quantile"] = int(r[1:])
        # Price area parts ->
        elif "NO" in r:
            attributes["price_area"] = r
        elif "SE" in r:
            attributes["price_area"] = r
        elif "FI" in r:
            attributes["price_area"] = r
        elif "DK" in r:
            attributes["price_area"] = r
        else:
            raise ValueError(f"Uncaught attribute: {r}")

    return attributes