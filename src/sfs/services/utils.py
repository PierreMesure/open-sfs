def _get_created_or_updated(item):
    updated = item["_source"]["uppdateradDateTime"]
    return updated if updated else item["_source"]["skapadDateTime"]


def get_latest_update(data):
    latest_update = None

    for item in data:
        date = _get_created_or_updated(item)
        if latest_update is None:
            latest_update = date
        else:
            if date > latest_update:
                latest_update = date

    return latest_update


def sort(data):
    return sorted(
        data,
        key=lambda item: (
            item["_source"]["publiceringsar"],
            int(item["_source"]["lopnummer"] or 0),
        ),
    )
