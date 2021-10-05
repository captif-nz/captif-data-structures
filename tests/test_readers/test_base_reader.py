
from captif_data_structures.readers import BaseReader, DemoReader
from captif_data_structures.structure.demo import _abcd1234


def test_base_reader_read_data_from_file(data_path):
    path = data_path.joinpath("demo", "abcd1234.dat")
    data = BaseReader._read_data_from_file(path)
    assert data == (
        "param1\ttuesday\n"
        "param2\t23.1\n"
        "param3\t1.4\n"
        "\n"
        "column B\tcolumn A\n"
        "toyota\t3\n"
        "nissan\t34\n"
        "suzuki\t1"
    )

def test_demo_load(data_path):
    path = data_path.joinpath("demo", "abcd1234.dat")
    meta, table_rows, structure_id = DemoReader.load(path)
    assert meta == {"param_1": "tuesday", "param_2": 33.1}
    assert table_rows == [
        {"column_1": "toyota_", "column_2": 2},
        {"column_1": "nissan_", "column_2": 33},
        {"column_1": "suzuki_", "column_2": 0},
    ]
    assert structure_id == "abcd1234"