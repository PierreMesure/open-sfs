import requests
import os

OLD_DOMAIN = "https://rkrattsdb.gov.se"
OLD_URL = OLD_DOMAIN + "/SFSdoc/{}/{}{}.pdf"
NEW_DOMAIN = "https://svenskforfattningssamling.se"
NEW_URL = NEW_DOMAIN + "/sites/default/files/sfs/{}-{}/SFS{}-{}.pdf"

os.makedirs("pdf", exist_ok=True)

# Old database starts at 1998:306 and stops at 2018:159
for year in range(2016, 2019):
    FAILURES = 0
    last_digits = year % 100
    last_digits_str = f"{last_digits:02d}"
    year_folder = f"pdf/{last_digits_str}"
    os.makedirs(year_folder, exist_ok=True)

    for lopnummer in range(1, 10000):
        lopnummer_str = f"{lopnummer:04d}"
        url = OLD_URL.format(last_digits_str, last_digits_str, lopnummer_str)
        response = requests.get(url)
        if response.status_code == 200:
            with open(
                f"{year_folder}/{last_digits_str}{lopnummer_str}.pdf",
                "wb",
            ) as file:
                file.write(response.content)
        else:
            FAILURES += 1

            if FAILURES == 10:
                break

# New database starts at 2018:160
for year in range(2018, 2026):
    FAILURES = 0
    last_digits = year % 100
    last_digits_str = f"{last_digits:02d}"
    year_folder = f"pdf/{last_digits_str}"
    os.makedirs(year_folder, exist_ok=True)

    month = 1

    for lopnummer in range(1, 10000):
        lopnummer_str = f"{lopnummer:04d}"

        if year == 2018 and lopnummer < 160:
            continue

        for m in range(month, 13):
            month_str = f"{m:02d}"
            url = NEW_URL.format(year, month_str, year, lopnummer)
            response = requests.get(url)
            if response.status_code == 200:
                with open(
                    f"{year_folder}/{last_digits_str}{lopnummer_str}.pdf",
                    "wb",
                ) as file:
                    file.write(response.content)

                month = m
                break
            elif m == 12:
                FAILURES += 1

        if FAILURES == 10:
            break
