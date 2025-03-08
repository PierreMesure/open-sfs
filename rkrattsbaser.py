import json
import requests

from writer import write_json

BETA_URL = "https://beta.rkrattsbaser.gov.se/elasticsearch/SearchEsByRawJson"


def get_law(id):
    payload = json.dumps(
        {
            "api": "search",
            "json": {
                "query": {"bool": {"must": [{"term": {"beteckning.keyword": id}}]}}
            },
        }
    )
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", BETA_URL, headers=headers, data=payload).json()

    print(response)


def get_year(year):
    payload = json.dumps(
        {
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
    )
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", BETA_URL, headers=headers, data=payload).json()

    return response["hits"]["hits"]
