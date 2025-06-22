import os
import json
import pyarrow as pa
import pyarrow.parquet as pq

data_folder = "data"


def get_pdf(beteckning):
    year, number = beteckning.split(":")
    if len(year) > 4:
        return None
    filename = f"{year[-2:]}/{year[-2:]}{int(number):04d}.pdf"
    pdf_path = f"jpinfonet_pdf_named/{filename}"
    pdf_path_2 = f"pdf/{filename}"
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            return f.read()
    elif os.path.exists(pdf_path_2):
        with open(pdf_path_2, "rb") as f:
            return f.read()
    else:
        return None


def get_metadata(sfs_dict, parent_id=None):
    data = {}
    data["beteckning"] = sfs_dict["beteckning"]
    title = sfs_dict["rubrik"]
    data["title"] = title.replace("\r\n", " ") if title else None
    year = sfs_dict["publiceringsar"]
    data["year"] = int(year) if year else int(data["beteckning"].split(":")[0])
    data["text"] = None if parent_id else sfs_dict["fulltext"]["forfattningstext"]
    data["amends"] = parent_id
    if data["year"] < 1993:
        pdf = None
    else:
        pdf = get_pdf(data["beteckning"])
    data["pdf"] = pdf
    return data


schema = pa.schema(
    [
        pa.field("beteckning", pa.string()),
        pa.field("title", pa.string()),
        pa.field("year", pa.int32()),
        pa.field("text", pa.string()),
        pa.field("amends", pa.string()),
        pa.field("pdf", pa.binary()),
    ]
)

writer = pq.ParquetWriter("output.parquet", schema, compression="gzip")

batch_size = 100
batch_data = []

for filename in sorted(os.listdir(data_folder)):
    if filename.endswith(".json"):
        file_path = os.path.join(data_folder, filename)
        print(f"Processing year {filename.replace('.json', '')}")

        with open(file_path, "r") as file:
            sfs_list = json.load(file)
            for sfs in sfs_list:
                sfs_dict = sfs["_source"]
                record = get_metadata(sfs_dict)
                batch_data.append(record)
                for amendment in sfs_dict["andringsforfattningar"]:
                    amendment_data = get_metadata(amendment, sfs_dict["beteckning"])
                    batch_data.append(amendment_data)
                if len(batch_data) >= batch_size:
                    arrays = []
                    for field in schema.names:
                        values = [row.get(field) for row in batch_data]
                        arrays.append(pa.array(values))
                    batch_table = pa.Table.from_arrays(arrays, schema=schema)
                    writer.write_table(batch_table)
                    batch_data = []

if batch_data:
    arrays = []
    for field in schema.names:
        values = [row.get(field) for row in batch_data]
        arrays.append(pa.array(values))
    batch_table = pa.Table.from_arrays(arrays, schema=schema)
    writer.write_table(batch_table)

writer.close()

print("Parquet file has been written successfully.")
