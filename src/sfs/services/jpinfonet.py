import os
import shutil
import requests

URL = "https://www.jpinfonet.se/documentfile/getfile?portalId=56&docId={}&propId=5"

for i in range(352104, 361048 + 1):
    url = URL.format(i)
    response = requests.get(url)
    if response.status_code == 200:
        with open(
            f"./jpinfonet_pdf/{i}.pdf",
            "wb",
        ) as file:
            file.write(response.content)

END2 = 361048

for i in range(93, 98 + 1):
    os.makedirs(f"jpinfonet_pdf_named/{i}", exist_ok=True)


def alphabetical(start, end, start2, year):
    numbers = [str(i) for i in range(start, end + 1)]
    numbers.sort()
    j = 0

    for i in range(start2, END2 + 1):
        try:
            print(f"{i} -> {numbers[j]}")
            shutil.copy(
                f"jpinfonet_pdf/{i}.pdf",
                f"jpinfonet_pdf_named/{year}/{year}{int(numbers[j]):04d}.pdf",
            )
        except FileNotFoundError:
            print(f"{i}.pdf not found, continuing...")
            continue
        except IndexError:
            print("Reached the end of the list for this year, stopping.")
            break
        j += 1


def ascending(start, end, start2, year):
    numbers = range(start, end + 1)
    j = 0

    for i in range(start2, END2 + 1):
        try:
            print(f"{i} -> {numbers[j]}")
            shutil.copy(
                f"jpinfonet_pdf/{i}.pdf",
                f"jpinfonet_pdf_named/{year}/{year}{int(numbers[j]):04d}.pdf",
            )
        except FileNotFoundError:
            print(f"{i}.pdf not found, continuing...")
            continue
        except IndexError:
            print("Reached the end of the list for this year, stopping.")
            break
        j += 1


alphabetical(1, 1033, 352104, "93")
ascending(1034, 1750, 353141, "93")
alphabetical(1, 670, 353863, "94")
ascending(1000, 1041, 354533, "94")
ascending(671, 999, 354575, "94")
ascending(1042, 1335, 354906, "94")
ascending(1336, 1336, 361045, "94")
ascending(1337, 1501, 355201, "94")  # 1501 needs to be merged?
ascending(1502, 1659, 355376, "94")
ascending(1660, 1660, 361048, "94")
ascending(1661, 2093, 355534, "94")
alphabetical(1, 682, 355991, "95")
ascending(1000, 1331, 356676, "95")
ascending(683, 999, 357008, "95")
ascending(1332, 1730, 357325, "95")
alphabetical(1, 751, 357724, "96")
ascending(1000, 1155, 358477, "96")
ascending(752, 999, 358634, "96")
ascending(1156, 1657, 358886, "96")
alphabetical(1, 495, 359390, "97")
ascending(496, 773, 359889, "97")
ascending(775, 935, 360170, "97")
ascending(1000, 1338, 360334, "97")
ascending(936, 999, 360673, "97")
alphabetical(1, 305, 360738, "98")
