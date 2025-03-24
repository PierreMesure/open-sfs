import json
import requests

BETA_URL = "https://beta.rkrattsbaser.gov.se/elasticsearch/SearchEsByRawJson"


def _post(payload_dict):
    payload = json.dumps(payload_dict)
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", BETA_URL, headers=headers, data=payload).json()

    return response["hits"]["hits"]


def get_law(id):
    payload_dict = {
        "api": "search",
        "json": {"query": {"bool": {"must": [{"term": {"beteckning.keyword": id}}]}}},
    }

    return _post(payload_dict)


def get_year(year):
    # import os
    # if os.path.exists(f"data/{year}.json"):
    #     with open(f"data/{year}.json", "r") as file:
    #         return json.load(file)
    # else:
    #     return []

    payload_dict = {
        "searchIndexes": ["Sfs"],
        "api": "search",
        "json": {
            "sort": [{"beteckningSortable.sort": {"order": "asc"}}],
            "query": {
                "bool": {
                    "must": [
                        {
                            "bool": {
                                "should": [
                                    {"terms": {"publiceringsar.keyword": [year]}}
                                ]
                            }
                        },
                        {"term": {"publicerad": True}},
                    ]
                }
            },
            "size": 10000,
            "from": 0,
        },
    }

    return _post(payload_dict)


def get_newer_items(date):
    payload_dict = {
        "searchIndexes": ["Sfs"],
        "api": "search",
        "json": {
            "sort": [{"beteckningSortable.sort": {"order": "asc"}}],
            "query": {
                "bool": {
                    "must": [
                        {"range": {"uppdateradDateTime": {"gt": date}}},
                        {"term": {"publicerad": True}},
                    ]
                }
            },
            "size": 10000,
            "from": 0,
        },
    }

    return _post(payload_dict)
