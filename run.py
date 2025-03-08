import os
from writer import write_json
from rkrattsbaser import get_year

data = []

os.makedirs("data", exist_ok=True)

for i in range(1686, 2025 + 1):
    print(f"Fetching {i}...")
    year_data = get_year(i)
    write_json(year_data, f"data/{i}.json")
    data.extend(year_data)

write_json(data, "data/all.json")
