import json
import requests
from datetime import datetime
import traceback
import pandas as pd


class Query:
    """
    Query object for bitquery
    """

    def __init__(self, API_KEY):
        self.API_KEY = API_KEY

    def run(self, query, to_df=False):
        headers = {"X-API-KEY": self.API_KEY}
        request = requests.post(
            "https://graphql.bitquery.io/", json={"query": query}, headers=headers
        )
        result = request.json()
        assert "data" in result.keys(), result

        try:
            chain = list(result["data"].keys())[0]
        except:
            traceback.format_exc()
            raise Exception("only one chain allowed per query")
        try:
            table = list(result["data"][chain].keys())[0]
        except:
            traceback.format_exc()
            raise Exception("only one table allowed per query")

        if to_df:
            try:
                result = pd.json_normalize(result["data"][chain][table])
            except:
                raise Exception(
                    "Too many rows queried. Try limiting the # of rows with options: {limit: 25000}"
                )
            # Rename columns for easier access
            col_map = {}
            for col in result.columns:
                col_map[col] = "".join(word.title() for word in col.split("."))
            result = result.rename(columns=col_map)
            print(f"Retrieved {result.shape[0]} rows")

        return result

    def run_batch(self, query, start, end, batch_freq="7D"):
        """
        Runs a batched query and returns a Pandas DataFrame.
        Expects query to have time: {between: ["%s", "%s"]} in the query.
        start, end must be in format "2022-04-01T00:00:0"

        """
        assert (
            'time: {between: ["%s", "%s"]}' in query
        ), "Query must have time string specified"
        dates_batched = pd.date_range(start, end, freq=batch_freq)
        dates_batched = [
            str(x.isoformat()) for x in dates_batched.append(pd.DatetimeIndex([end]))
        ]
        results = []
        date_ranges = list(zip(dates_batched, dates_batched[1:]))
        for date_range in date_ranges:
            assert len(date_range) == 2
            print(datetime.now(), f"querying from {date_range[0]} to {date_range[1]}")
            data = self.run(query % (date_range[0], date_range[1]), to_df=True)
            results.append(data)

        df = pd.concat(results, ignore_index=False)
        return df
