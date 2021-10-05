
from datetime import datetime

from captif_data_structures.readers import DeflectionBeamReader


def test_deflection_beam_reader_cb379c14(data_path):
    path = data_path.joinpath("deflection_beam", "cb379c14.dat")
    meta, table_rows, structure_id = DeflectionBeamReader.load(path)

    assert meta == {
        "datetime": datetime(2020, 6, 30, 8, 31),
        "station_no": 0,
        "max_raw_deflection_mm": 0.591,
    }
    assert table_rows == [
        {"distance_m": 0.0, "raw_deflection_mm": -0.1257},
        {"distance_m": 0.01, "raw_deflection_mm": -0.1210},
        {"distance_m": 0.02, "raw_deflection_mm": -0.1247},
    ]
    assert structure_id == "cb379c14"
