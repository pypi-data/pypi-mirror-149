import datetime
from urllib.error import HTTPError

import pandas as pd
from dateutil.relativedelta import relativedelta


def _zen_to_han(text):
    return text.translate(
        str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)})
    )


def _wareki_to_yyyy(sr):

    df = pd.DataFrame(sr.apply(_zen_to_han)).replace("年", "", regex=True)
    df = df.assign(
        gengou=df["wareki"].replace("[0-9]*", "", regex=True),
        past=df["wareki"]
        .replace("^..([0-9]*)", r"\1", regex=True)
        .astype(int),
    )
    df["offset"] = 0
    df.loc[df["gengou"] == "昭和", "offset"] = 1925
    df.loc[df["gengou"] == "平成", "offset"] = 1988
    df.loc[df["gengou"] == "令和", "offset"] = 2018
    df["year"] = df["offset"] + df["past"]
    return df["year"]


def _build_uri(year, month):
    if year >= 2020:
        extension = "xlsx"
    else:
        extension = "xls"
    if year >= 2011:
        year_file = year
    else:
        year_file = ""
    if year >= 2007:
        prefix = "s"
    else:
        prefix = "m"

    return (
        "https://www.mhlw.go.jp/toukei/saikin/hw/jinkou/geppo/"
        f"{prefix}{year}/xls/{year_file}{month:02}.{extension}"
    )


def _formatting(df):
    df.columns = ["dummy", "category", "wareki"] + [x + 1 for x in range(12)]
    df = df.iloc[:18, 1:].replace("　", "", regex=True)
    df.iloc[:, :2] = df.iloc[:, :2].fillna(method="ffill")
    df["year"] = _wareki_to_yyyy(df["wareki"].replace("･令和元年", "", regex=True))
    df["category"] = df["category"].replace("自然増加", "自然増減", regex=True)
    df = df.drop("wareki", axis=1).set_index(["year", "category"])
    df.columns.name = "month"
    df = df.stack()
    df.name = "value"
    df = df.reset_index()
    df["day"] = 1
    df["ts"] = pd.to_datetime(df[["year", "month", "day"]])

    return df[["category", "ts", "value"]]


def _read_prompt_ym(year, month, verbose=False, ignore_error=False):

    uri = _build_uri(year, month)
    if verbose:
        print(f"download from: {uri}")

    try:
        df = pd.read_excel(uri, skiprows=3)
    except HTTPError as e:
        if verbose:
            print("error: ", e)
        if not ignore_error:
            raise e
        return pd.DataFrame()

    return _formatting(df)


def _translate(df, lang):
    if lang.lower() not in ("japanese", "ja", "jp"):
        df["category"] = df["category"].replace(
            {
                "出生": "live births",
                "婚姻": "marriages",
                "死亡": "deaths",
                "死産": "foetal deaths",
                "自然増減": "natural change",
                "離婚": "divorces",
            }
        )

    return df


def read_prompt(
    year_from=2005,
    year_to=None,
    month_to=None,
    months_offset=2,
    days_offset=23,
    lang="english",
    verbose=False,
    ignore_error=False,
):
    """
    Reading prompt of Vital Statistics in Japan.
    Download from Ministry of Health.

    https://www.mhlw.go.jp/english/


    Parameters
    ----------

    year_from : int, default 2005
        reading year from
    year_to : int, default None
        reading year to
    month_to : int, default None
        reading month to. default value is days_offset days and
        months_offset months before now.
    months_offset : int, default 2
        publication offset month.
    days_offset : int, default 23
        publication offset days.
    lang : str, default english
        category language. "english", "japanese" is available.
    verbose : bool, default False
        output download url to stdout
    ignore_error : bool, default False
        ignore HTTPError

    Returns
    -------
    dataframe : pandas.DataFrame

    Raises
    ------
    HTTPError
        download error

    Refference
    ----------

    data download page
        https://www.mhlw.go.jp/toukei/list/81-1a.html

    Outline of Vital Statistics in Japan
        https://www.mhlw.go.jp/english/database/db-hw/outline/index.html


    """

    if (year_to is None) | (month_to is None):
        last_published = datetime.datetime.now() - relativedelta(
            months=months_offset, days=days_offset
        )
        year_to = last_published.year
        month_to = last_published.month

    result_list = []
    options = dict(verbose=verbose, ignore_error=ignore_error)
    for year in range(year_from + 2, year_to):
        result_list.append(_read_prompt_ym(year, 12, **options))
    result_list.append(_read_prompt_ym(year_to, month_to, **options))
    df = (
        pd.concat(result_list)
        .drop_duplicates()
        .sort_values(["category", "ts"])
    )
    df = df[df.ts.dt.year >= year_from].reset_index(drop=True)
    return _translate(df, lang)
