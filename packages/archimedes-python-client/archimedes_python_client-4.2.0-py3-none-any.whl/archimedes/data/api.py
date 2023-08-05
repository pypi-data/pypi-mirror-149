"""
A collection of functions for integrating with the Archimedes API
"""

import json
from http import HTTPStatus
from typing import Dict, List

import pandas as pd
import requests
from requests.exceptions import HTTPError, JSONDecodeError

import archimedes
from archimedes.auth import get_auth, NoneAuth
from archimedes.configuration import get_api_config
from archimedes.data.types import Prediction, PredictionData

API_URL = get_api_config().url
API_VERSION = 2


def get_intraday_trades(
    price_areas: List[str] = None,
    start: str = None,
    end: str = None,
    *,
    access_token: str = None,
):
    """Get raw intraday trades from Archimedes Database

    This function can be used to fetch raw time series from the Archimedes Database without any post-processing.
    To see which series are available, use `list_ids()`.

    Example:
        >>> archimedes.get(
        >>>     price_areas=["NO1",],
        >>>     start="2020-06-20T04:00:00+00:00",
        >>>     end="2020-06-20T09:00:00+00:00",
        >>> )
                from_dt to_dt   series_id   version price   trade_time  buy_area    sell_area   attributes
        0	2022-03-01T00:00:00+00:00	2022-03-01T01:00:00+00:00	NP/IntradayTrades	1646193645	146.63	2022-02-28T17:02:06.934+0000	OPX	NO1	{'price': 146.63,...,  'product_code': 'PH-20220301-01'}
        1	2022-03-01T00:00:00+00:00	2022-03-01T01:00:00+00:00	NP/IntradayTrades	1646193645	146.63	2022-02-28T17:02:06.934+0000	OPX	NO1	{'price': 146.63,... , 'product_code': 'PH-20220301-01'}
        2	2022-03-01T00:00:00+00:00	2022-03-01T01:00:00+00:00	NP/IntradayTrades	1646193645	146.63	2022-02-28T17:02:06.934+0000	OPX	NO1	{'price': 146.63, ..., 'product_code': 'PH-20220301-01'}
        ...
        155	2022-03-01T23:00:00+00:00	2022-03-02T00:00:00+00:00	NP/IntradayTrades	1646193645	148.99	2022-03-01T13:05:40.934+0000	NL	NO1	{'price': 148.99,... , 'product_code': 'PH-20220301-24'}
        156	2022-03-01T23:00:00+00:00	2022-03-02T00:00:00+00:00	NP/IntradayTrades	1646193645	148.8	2022-03-01T12:57:58.777+0000	NO1	FI	{'price': 148.8,...,  'product_code': 'PH-20220301-24'}
        157	2022-03-01T23:00:00+00:00	2022-03-02T00:00:00+00:00	NP/IntradayTrades	1646193645	148.8	2022-03-01T12:58:02.115+0000	NO1	FI	{'price': 148.8, ... , 'product_code': 'PH-20220301-24'}


    Args:
        price_areas (List[str], optional): The price areas to pick, all price areas if None. Defaults to None.
        start (str, optional): The first datetime to fetch (inclusive). Returns all if None. Defaults to None.
        end (str, optional): The last datetime to fetch (exclusive). Returns all if None. Defaults to None.
        access_token (str, optional): None - access token for the API

    Returns:
        DataFrame with all the time series data

    Raises:
        HTTPError: If an http error occurs when requesting the API.
        NoneAuth: If the user is unauthorized or if the authorization has expired.
    """

    if isinstance(price_areas, str):
        price_areas = [price_areas]

    if start is None:
        start = archimedes.ArchimedesConstants.DATE_LOW
    else:
        start = pd.to_datetime(start)

    if end is None:
        end = archimedes.ArchimedesConstants.DATE_HIGH
    else:
        end = pd.to_datetime(end)

    query = {
        "series_id": "NP/IntradayTrades",
        "price_areas": price_areas,
        "start": start,
        "end": end,
        "flatten_columns": False,
    }

    observation_data = _make_api_request(
        f"{API_URL}/v{API_VERSION}/observation_json/get",
        access_token=access_token,
        params=query,
    )

    if not len(observation_data):
        return pd.DataFrame(
            columns=[
                "from_dt",
                "to_dt",
                "series_id",
                "version",
                "price",
                "trade_time",
                "buy_area",
                "sell_area",
                "attributes",
            ]
        )
    observation_data = [
        {
            **i,
            "price": i["value"].get("price"),
            "trade_time": i["value"].get("trade_time"),
        }
        for i in observation_data
    ]
    observation_data = pd.DataFrame.from_dict(observation_data)

    # Extracting price area and series id
    observation_data[
        ["series_id1", "series_id2", "buy_area", "sell_area"]
    ] = observation_data["series_id"].str.split("/", 3, expand=True)
    observation_data["series_id"] = (
        observation_data["series_id1"] + "/" + observation_data["series_id2"]
    )
    observation_data["attributes"] = observation_data["value"]
    observation_data["attributes_str"] = observation_data["value"].astype(str)
    observation_data = observation_data.drop_duplicates(
        ["from_dt", "series_id", "attributes_str"]
    )
    observation_data = observation_data.drop(
        ["series_id1", "series_id2", "value", "version", "attributes_str"], axis=1
    )
    observation_data = observation_data.sort_values(by=["from_dt"]).reset_index(
        drop=True
    )

    return observation_data


def get(
    series_ids: List[str],
    price_areas: List[str] = None,
    start: str = None,
    end: str = None,
    *,
    access_token: str = None,
):
    """Get any number of time series.

    This function can be used to fetch time series from the Archimedes Database.
    To see which series are available, use `list_ids()`.

    Example:
        >>> archimedes.get(
        >>>     series_ids=["NP/AreaPrices"],
        >>>     price_areas=["NO1", "NO2"],
        >>>     start="2020-06-20T04:00:00+00:00",
        >>>     end="2020-06-28T04:00:00+00:00",
        >>> )
        series_id                 NP/AreaPrices
        price_area                          NO1   NO2
        from_dt
        2020-06-20T04:00:00+00:00          1.30  1.30
        2020-06-20T05:00:00+00:00          1.35  1.35
        ...                                 ...   ...
        2020-06-28T03:00:00+00:00          0.53  0.53
        2020-06-28T04:00:00+00:00          0.55  0.55

    Args:
        series_ids (List[str]): The series ids to get.
        price_areas (List[str], optional): The price areas to pick, all price areas if None. Defaults to None.
        start (str, optional): The first datetime to fetch (inclusive). Returns all if None. Defaults to None.
        end (str, optional): The last datetime to fetch (exclusive). Returns all if None. Defaults to None.
        access_token (str, optional): None - access token for the API

    Returns:
        DataFrame with all the time series data

    Raises:
        HTTPError: If an http error occurs when requesting the API.
        NoneAuth: If the user is unauthorized or if the authorization has expired.
    """

    if isinstance(series_ids, str):
        series_ids = [series_ids]

    if isinstance(price_areas, str):
        price_areas = [price_areas]

    if start is None:
        start = archimedes.ArchimedesConstants.DATE_LOW
    else:
        start = pd.to_datetime(start)

    if end is None:
        end = archimedes.ArchimedesConstants.DATE_HIGH
    else:
        end = pd.to_datetime(end)

    query = {
        "series_ids": series_ids,
        "price_areas": price_areas,
        "start": start,
        "end": end,
        "flatten_columns": True,
    }

    df = _make_api_request(
        f"{API_URL}/v{API_VERSION}/data/get",
        access_token=access_token,
        params=query,
    )

    if len(df):
        df = pd.DataFrame.from_dict(df)
        df = df.sort_values(by=["from_dt", "version"])
    else:
        df = pd.DataFrame(
            columns=["series_id", "from_dt", "ref_dt", "value", "version", "price_area"]
        )
    df = df.pivot_table(
        values="value",
        columns=["series_id", "price_area"],
        index="from_dt",
        aggfunc="last",
    )

    del query["series_ids"]
    for series_id in series_ids:
        query["series_id"] = series_id
        observation_data = _make_api_request(
            f"{API_URL}/v{API_VERSION}/observation_json/get",
            access_token=access_token,
            params=query,
        )
        if len(observation_data):
            observation_data = pd.DataFrame.from_dict(observation_data)

            observation_data[
                ["series_id1", "series_id2", "price_area"]
            ] = observation_data["series_id"].str.split("/", 2, expand=True)
            observation_data["series_id"] = (
                observation_data["series_id1"] + "/" + observation_data["series_id2"]
            )
            observation_data = observation_data.drop(
                ["series_id1", "series_id2"], axis=1
            )

            if series_id == "NP/IntradayTrades":

                def agg_func(x):
                    return list(x)

                sort_headers = ["from_dt"]
            else:
                agg_func = "last"
                sort_headers = ["from_dt", "version"]

            observation_data = observation_data.sort_values(by=sort_headers)
            observation_data = observation_data.pivot_table(
                values="value",
                columns=["series_id", "price_area"],
                index="from_dt",
                aggfunc=agg_func,
            )

            df = pd.merge(
                df, observation_data, left_index=True, right_index=True, how="outer"
            )

    df.index = pd.to_datetime(df.index)
    return df


def get_latest(
    series_ids: List[str],
    price_areas: List[str] = None,
    *,
    access_token: str = None,
):
    """Get the most recent data for any number of time series.

    This function is similar to `get()`, but only fetches data from the past 48 hours,
    potentially including future hours as well (as in the case of Spot price data).

    @TODO: Add an argument `hours` that allows the 'lookback' period to be extended
    to an arbitrary number of hours.

    Example:
        >>> # Calling this function at 2020-03-15T10:15:00
        >>> archimedes.get_latest(
        >>>     series_ids=["NP/AreaPrices", "NP/ConsumptionImbalancePrices"],
        >>>     price_areas=["NO1"],
        >>> )
        series_id                 NP/AreaPrices  NP/ConsumptionImbalancePrices
        price_area                          NO1                            NO1
        from_dt
        2020-03-14T04:11:00+00:00          1.30                           1.30
        2020-03-14T05:12:00+00:00          1.35                           1.35
        ...                                 ...                            ...
        2020-03-15T22:00:00+00:00          0.53                            NaN
        2020-03-15T23:00:00+00:00          0.55                            NaN

    Args:
        series_ids (List[str]): The series ids to get.
        price_areas (List[str], optional): The price areas to pick, all price areas if None. Defaults to None.
        access_token (str, optional): None - access token for the API

    Returns:
        DataFrame with the latest time series data

    Raises:
        HTTPError: If an http error occurs when requesting the API.
        NoneAuth: If the user is unauthorized or if the authorization has expired.
    """
    now_dt = pd.Timestamp.now(tz="utc")
    start_dt = now_dt - pd.Timedelta(days=2)
    # +14 days should be enough in all cases now:
    end_dt = now_dt + pd.Timedelta(days=14)

    df = get(
        series_ids=series_ids,
        price_areas=price_areas,
        start=start_dt.isoformat(),
        end=end_dt.isoformat(),
        access_token=access_token,
    )

    return df


def get_predictions(
    series_ids: List[str] = None,
    price_areas: List[str] = None,
    start: str = None,
    end: str = None,
    ref_dt_start: str = None,
    ref_dt_end: str = None,
    *,
    access_token: str = None,
) -> pd.DataFrame:
    """Get any number of predictions

    This function can be used to fetch predictions from the Archimedes Database.

    Unlike `archimedes.get`, this will return a list, not a dataframe.

    Example:
        >>> archimedes.get_predictions(
            series_ids=["PX/rk-naive"],
            price_areas=["NO1"],
            start="2020"
        )
        >>> [...]

    Args:
        series_ids (List[str], optional): The series ids to get.
        price_areas (List[str], optional): The price areas to get the data for.
        start (str, optional):
            The first datetime to fetch (inclusive). Returns all if None. Defaults to None.
        end (str, optional):
            The last datetime to fetch (exclusive). Returns all if None. Defaults to None.
        ref_dt_start (pd.Timestamp, optional):
            The earliest ref_dt to fetch (inclusive). Defaults to None.
        ref_dt_end (pd.Timestamp, optional):
            The latest ref_dt to fetch (exclusive). Defaults to None.
        access_token (str, optional): None - access token for the API

    Returns:
        DataFrame with all the prediction data
    """
    if isinstance(series_ids, str):
        series_ids = [series_ids]

    if isinstance(price_areas, str):
        price_areas = [price_areas]

    query = {}

    if start is not None:
        query["start"] = pd.to_datetime(start, utc=True)

    if end is not None:
        query["end"] = pd.to_datetime(end, utc=True)

    if ref_dt_start is not None:
        query["ref_dt_start"] = pd.to_datetime(ref_dt_start, utc=True)

    if ref_dt_end is not None:
        query["ref_dt_end"] = pd.to_datetime(ref_dt_end, utc=True)

    if series_ids is not None:
        query["series_ids"] = series_ids

    if price_areas is not None:
        query["price_areas"] = price_areas

    data = _make_api_request(
        f"{API_URL}/v{API_VERSION}/data/get_predictions",
        access_token=access_token,
        params=query,
    )

    for item in data:
        json_data = item.get("json_data")
        item.update(json_data)
        del item["json_data"]

    df = pd.DataFrame.from_dict(data)

    date_fields = ["from_dt", "run_dt", "ref_dt"]

    for date_field in date_fields:
        if date_field in df:
            df[date_field] = pd.to_datetime(df[date_field], utc=True)

    df = df.fillna("")

    return df


def list_series_price_areas(series_id: str, *, access_token: str = None):
    """
    Retrieve all of the price_areas which are available for the specified data series

    Example:
        >>> archimedes.list_series_price_areas('NP/AreaPrices')
           price_areas
        0          DK1
        1          DK2
        ...        ...
        10         SE3
        11         SE4

    Returns:
        Dataframe with all available price areas for the specified series_id
    """
    query = {
        "series_id": series_id,
    }
    data = _make_api_request(
        f"{API_URL}/v{API_VERSION}/data/list_series_price_areas",
        access_token=access_token,
        params=query,
    )
    data = pd.DataFrame.from_dict(data)

    observation_data = _make_api_request(
        f"{API_URL}/v{API_VERSION}/observation_json/list_series_price_areas",
        access_token=access_token,
        params=query,
    )
    observation_data = pd.DataFrame.from_dict(observation_data)

    price_area_df = pd.concat([data, observation_data]).drop_duplicates()
    price_area_df = price_area_df.sort_values("price_areas").reset_index(drop=True)
    return price_area_df


def list_ids(sort: bool = False, *, access_token: str = None):
    """List all the series ids available.

    Example:
        >>> archimedes.list_ids()
                                    series_id
        0   NP/NegativeProductionImbalancePrices
        1                    NP/ProductionTotals
        ..                                   ...
        38                 NP/OrdinaryDownVolume
        39                    NP/SpecialUpVolume

    Args:
        sort (bool): False - return all series in one dataframe column, True - order dataframe by data-origin
        access_token (str, optional): None - access token for the API

    Returns:
        DataFrame with all available list_ids
    """
    data = _make_api_request(
        f"{API_URL}/v{API_VERSION}/data/list_ids", access_token=access_token
    )
    data = pd.DataFrame.from_dict(data)

    observation_data = _make_api_request(
        f"{API_URL}/v{API_VERSION}/observation_json/list_ids", access_token=access_token
    )
    observation_data = pd.DataFrame.from_dict(observation_data)

    series_df = pd.concat([data, observation_data]).drop_duplicates()
    series_df = series_df.sort_values(["series_id"]).reset_index(drop=True)
    if not sort:
        return series_df

    series_df["pre"] = series_df["series_id"].str.split("/", 1).str[0]
    series_df = pd.DataFrame.from_dict(
        series_df.groupby("pre")["series_id"].apply(list).to_dict(), orient="index"
    ).transpose()
    series_df = series_df[sorted(series_df.columns)]

    series_df = series_df.fillna("")
    return series_df.copy()


def list_prediction_ids(*, access_token: str = None):
    """List all the prediction series ids available.

    Example:
        >>> archimedes.list_prediction_ids()
                                     series_id
        0               PX/rk-nn-probabilities
        1   PX/rk-nn-direction-probabilities/U
        ..                                ...
        22                           PX/rk-901
        23                         PX/rk-naive
    """

    data = _make_api_request(
        f"{API_URL}/v{API_VERSION}/data/list_prediction_ids", access_token=access_token
    )

    return pd.DataFrame.from_dict(data)


def get_predictions_ref_dts(prediction_id: str = None, *, access_token: str = None):
    """Get which ref_dts are available.

    ref_dt == prediction_build_dt
    Users views in the database.

    Args:
        prediction_id (str): The series id to get the reference dts for. If None, get ref_dts for all prediction_ids.
        access_token (str, optional): Access token for the API

    Returns:
        DataFrame with all ref_dts
    """
    query = {}

    if prediction_id:
        query["prediction_id"] = prediction_id

    data = _make_api_request(
        f"{API_URL}/v{API_VERSION}/data/get_predictions_ref_dts",
        access_token=access_token,
        params=query,
    )

    return pd.DataFrame.from_dict(data)


def _make_api_request(url, method="GET", access_token=None, *args, **kwargs):
    if access_token is None:
        archimedes_auth = get_auth()
        if archimedes_auth is None:
            raise NoneAuth(
                "access_token parameter must be passed when using USE_WEB_AUTHENTICATION"
            )
        access_token = archimedes_auth.get_access_token_silent()

    headers = kwargs.pop("headers", None)
    if headers is None:
        headers = {}

    headers.update({"Authorization": f"Bearer {access_token}"})

    r = requests.request(method, url, headers=headers, *args, **kwargs)

    if r.status_code not in [HTTPStatus.OK, HTTPStatus.CREATED]:
        try:
            response_json = r.json()
            if "message" in response_json:
                error_message = response_json.get("message")
            elif "detail" in response_json:
                error_message = response_json.get("detail")
            else:
                error_message = json.dumps(response_json)
        except JSONDecodeError:
            error_message = r.content
        raise HTTPError(f"API Error: {error_message}")

    return r.json()


def store_prediction(
    prediction_id: str,
    from_dt: pd.Timestamp,
    ref_dt: pd.Timestamp,
    run_dt: pd.Timestamp,
    data: Dict,
    *,
    access_token: str = None,
):
    """Store a prediction

    Example:
        >>> import archimedes
        >>> import pandas as pd
        >>> from dateutil.tz import gettz
        >>> tz_oslo = gettz("Europe/Oslo")
        >>> prediction_id = "test-prediction-id"
        >>> from_dt = pd.Timestamp("2021-04-11 23:47:16.854775807", tz=tz_oslo)
        >>> ref_dt = pd.Timestamp("2021-04-10 23:00:00.000000000", tz=tz_oslo)
        >>> run_dt = pd.Timestamp.now(tz=tz_oslo)
        >>> data = {"direction": "D", "probability": 0.8632089971077396, "hours_ahead": 1, "price_area": "NO1"}
        >>> archimedes.store_prediction(
        >>>     prediction_id=prediction_id,
        >>>     from_dt=from_dt,
        >>>     ref_dt=ref_dt,
        >>>     run_dt=run_dt,
        >>>     data=data
        >>> )
        True
    """
    payload = {
        "prediction_id": prediction_id,
        "from_dt": from_dt.isoformat(),
        "ref_dt": ref_dt.isoformat(),
        "run_dt": run_dt.isoformat(),
        "data": data,
    }

    ret = _make_api_request(
        f"{API_URL}/v{API_VERSION}/data/store_prediction",
        method="POST",
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
        access_token=access_token,
    )

    return ret.get("success", False)


def store_predictions(
    prediction_id: str,
    prediction_data: List[PredictionData],
    *,
    access_token: str = None,
):
    """Store a prediction

    Example:
        >>> import archimedes
        >>> import pandas as pd
        >>> from dateutil.tz import gettz
        >>> tz_oslo = gettz("Europe/Oslo")
        >>> prediction_id = "test-prediction-id"
        >>> from_dt = pd.Timestamp("2021-04-11 23:47:16.854775807", tz=tz_oslo)
        >>> ref_dt = pd.Timestamp("2021-04-10 23:00:00.000000000", tz=tz_oslo)
        >>> run_dt = pd.Timestamp.now(tz=tz_oslo)
        >>> data = {"direction": "D", "probability": 0.8632089971077396, "hours_ahead": 1, "price_area": "NO1"}
        >>> prediction_data = [{'from_dt': from_dt, 'ref_dt': ref_dt, 'run_dt': run_dt, 'data': data }]
        >>> archimedes.store_predictions(
        >>>     prediction_id=prediction_id,
        >>>     prediction_data=prediction_data
        >>> )
        True
    """

    predictions = [
        {
            "from_dt": p["from_dt"].isoformat(),
            "ref_dt": p["ref_dt"].isoformat(),
            "run_dt": p["run_dt"].isoformat(),
            "data": p["data"],
        }
        for p in prediction_data
    ]

    payload = {
        "prediction_id": prediction_id,
        "data": predictions,
    }

    ret = _make_api_request(
        f"{API_URL}/v{API_VERSION}/data/store_predictions",
        method="POST",
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
        access_token=access_token,
    )

    return ret.get("success", False)


def forecast_list_ref_times(
    series_id: str,
    start: pd.Timestamp = None,
    end: pd.Timestamp = None,
    limit: int = None,
    *,
    access_token: str = None,
):
    """
    List all forecast reference times (the times that the forecast was generated)

    Args:
        series_id (str): The ID of the data series to find all the forecast reference times (the time the forecast was
            generated). Retrieve the complete list of series (both forecasts and observations) using the list_ids
            resource.
        start (pd.Timestamp, optional): The first datetime to fetch (inclusive). Returns all if not set. Should be
            specified in ISO 8601 format.
            (eg - '2021-11-29T06:00:00+00:00')
        end (pd.Timestamp, optional): The last datetime to fetch (exclusive). Returns all if not set. Should be
            specified in ISO 8601 format.
            (eg - '2021-11-30T06:00:00+00:00')
        limit (int, optional): Limit the output to a specific number of entries. No limit if not specified.
        access_token (str, optional): Access token for the API

    Example:
        >>> start = pd.Timestamp("2022-01-09T06:00:00+00:00")
        >>> end = pd.Timestamp("2022-01-10T06:00:00+00:00")
        >>> archimedes.forecast_list_ref_times('MET/forecast_air_temperature_2m', start, end)
                                   ref_times
        0   2022-01-10T05:00:00.000000+00:00
        1   2022-01-10T04:00:00.000000+00:00
        ...                              ...
        22  2022-01-09T07:00:00.000000+00:00
        23  2022-01-09T06:00:00.000000+00:00

    Returns:
        Dataframe with all of the forecast reference times
    """
    query = {
        "series_id": series_id,
        "start": start.isoformat() if start is not None else None,
        "end": end.isoformat() if end is not None else None,
        "limit": limit,
    }

    data = _make_api_request(
        f"{API_URL}/v{API_VERSION}/forecast/list_ref_times",
        access_token=access_token,
        params=query,
    )

    return pd.DataFrame.from_dict(data)


def forecast_diff(
    comparison_type: str,
    series_ids: List[str],
    price_areas: List[str] = None,
    ref_time1: pd.Timestamp = None,
    ref_time2: pd.Timestamp = None,
    *,
    access_token: str = None,
):
    """
    Get the difference between two different forecasts.

    Args:
        comparison_type: The type of comparison to do to the two forecasts:
            forecast_update - how has the the forecast for a specific time range been updated. The two forecast
                reference times must be within ~60 hours of each other. Otherwise the output will be empty (because
                the forecasts don't overlap).

            forecast_diff - compares the forecasts of any two dates to indicate how different they are.
        series_ids: The ID of the data series to get (eg - 'MET/forecast_air_temperature_2m' or
            'MET/forecast_wind_speed_10m'). To specify multiple data series, include the series_ids parameter multiple
            times in the url.
            Retrieve the complete list of series using the list_ids resource.
        price_areas: The name of the price area(eg - 'NO2', 'NO5', or 'DE1-NO1'). To specify multiple price areas,
            include the price_areas parameter multiple times in the url.
            Retrieve the complete list of price areas available for a specified series ID using list_series_price_areas
            resource.
        ref_time1: Specify one of the two timestamps for when a forecast was created. Should be specified in ISO 8601
            format (eg - '2021-11-29T06:00:00+00:00').
        ref_time2: Specify another of the two timestamps for when a forecast was created. Should be specified in ISO
            8601 format (eg - '2021-11-29T06:00:00+00:00').
        access_token (str, optional): Access token for the API

    Returns:
        Dataframe with the diff of the two forecasts
    """
    assert comparison_type in [
        "forecast_update",
        "forecast_diff",
    ], f"Unknown comparison_type '{comparison_type}' (should be either 'forecast_update' or 'forecast_diff')"
    query = {
        "forecast_comparison_type": comparison_type,
        "series_ids": series_ids,
        "price_areas": price_areas,
        "ref_time1": ref_time1,
        "ref_time2": ref_time2,
    }

    data = _make_api_request(
        f"{API_URL}/v{API_VERSION}/forecast/diff",
        access_token=access_token,
        params=query,
    )

    return pd.DataFrame.from_dict(data)


def forecast_get_by_ref_time_interval(
    series_id: str,
    price_area: str,
    start: pd.Timestamp = None,
    end: pd.Timestamp = None,
    forecast_interval: int = 24,
    day_ahead_hour: int = None,
    *,
    access_token: str = None,
):
    """
    Get a single forecast value for every hour. The value should be from the forecast that was generated at least
    forecast_interval hours prior.

    Args:
        series_id: The ID of the data series to get (eg - 'MET/forecast_air_temperature_2m' or
            'MET/forecast_wind_speed_10m'). Retrieve the complete list of series using the list_ids resource.
        price_area: The name of the price area(eg - 'NO2', 'SE3'). Retrieve the complete list of price areas available
            for a specified series ID using list_series_price_areas resource.
        start: The first datetime to fetch (inclusive). Returns all if not set. Should be specified in ISO 8601 format
            (eg - '2021-11-29T06:00:00+00:00')
        end: The last datetime to fetch (exclusive). Returns all if not set. Should be specified in ISO 8601 format
            (eg - '2021-11-30T06:00:00+00:00')
        forecast_interval: The number of hours earlier that the forecast must have been generated. In some cases, it
            could be older (if no forecast was generated at exactly that hour). NOTE - this is ignored if
            day_ahead_hour is set.
        day_ahead_hour: Used for day-ahead market. Indicates the hour of the day when the market closes (CET - Central
            European Time). Will return the forecast generated before this time on the previous day
            ('forecast_interval' will be set to 24). For example, if set to '12' (noon CET), the values shown for every
            hour of a specific day will be fetched from the most recent forecast generated before noon (most likely
            11am) on the previous day.
        access_token (str, optional): Access token for the API

    Returns:
        Dataframe with the forecasted values
    """
    query = {
        "series_id": series_id,
        "price_area": price_area,
        "start": start,
        "end": end,
        "forecast_interval": forecast_interval,
        "day_ahead_hour": day_ahead_hour,
    }

    data = _make_api_request(
        f"{API_URL}/v{API_VERSION}/forecast/get_by_ref_time_interval",
        access_token=access_token,
        params=query,
    )

    return pd.DataFrame.from_dict(data)
