
from datetime import datetime

from captif_data_structures.readers import LapCountReader


def test_lap_count_reader_d26612dd(data_path):
    path = data_path.joinpath("lap_count", "d26612dd.dat")
    meta, table_rows, structure_id = LapCountReader.load(path)

    assert meta == {}
    assert table_rows == [
        {"lap_count": 0, "datetime": datetime(2021, 4, 1, 10, 47)},
        {"lap_count": 637, "datetime": datetime(2021, 9, 22, 15, 9)},
        {"lap_count": 638, "datetime": datetime(2021, 9, 22, 15, 15)},
    ]
    assert structure_id == "d26612dd"


def test_lap_count_reader_e7b769c1(data_path):
    path = data_path.joinpath("lap_count", "e7b769c1.dat")
    meta, table_rows, structure_id = LapCountReader.load(path)

    assert meta == {}
    assert table_rows == [
        {"lap_count": 1032, "datetime": datetime(2021, 9, 23, 11, 46, 7), "position_cm": 180, "speed_kph": 0},
        {"lap_count": 1033, "datetime": datetime(2021, 9, 23, 11, 47, 59), "position_cm": 137, "speed_kph": 4},
        {"lap_count": 1034, "datetime": datetime(2021, 9, 23, 11, 48, 43), "position_cm": 131, "speed_kph": 5},
    ]
    assert structure_id == "e7b769c1"
