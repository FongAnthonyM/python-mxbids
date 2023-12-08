from pathlib import Path

from ucsfbids.datasets import Dataset
from ucsfbids.datasets.exporters.datasetupennexporter import DatasetUPENNExporter

name_map = {
    "EC0204": "UPenn0005",
    "EC0203": "UPenn0006",
    "EC0202": "UPenn0007",
    "EC0201": "UPenn0008",
    "EC0190": "UPenn0009",
    "EC0189": "UPenn0010",
    "EC0188": "UPenn0011",
    "EC0187": "UPenn0012",
    "EC0186": "UPenn0013",
}

if __name__ == "__main__":
    dataset = Dataset(Path("~/kleen-lab/pia/userdata/rchristin/upenn-staging").expanduser())
    dataset.add_exporter("UPENN", DatasetUPENNExporter)
    dataset.create_exporter("UPENN").execute_export(Path("/bids"), "staging", name_map)
