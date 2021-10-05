
from captif_data_structures.structure.demo import _abcd1234


"""
The demo data structure is included to verify functionality.

"""


def test_demo_extract_meta():
    data = (
        "param1\ttuesday\n"
        "param2\t23.1\n"
        "param3\t1.4\n"
        "\n"
        "column B\tcolumn A\n"
        "toyota\t3\n"
        "nissan\t34\n"
        "suzuki\t1"
    )
    meta = _abcd1234.extract_meta(data)
    assert meta == {"param_1": "tuesday", "param_2": 33.1}


def test_demo_extract_table():
    data = (
        "param1\ttuesday\n"
        "param2\t23.1\n"
        "param3\t1.4\n"
        "\n"
        "column B\tcolumn A\n"
        "toyota\t3\n"
        "nissan\t34\n"
        "suzuki\t1"
    )
    table_rows = _abcd1234.extract_table(data)
    assert table_rows == [
        {"column_1": "toyota_", "column_2": 2},
        {"column_1": "nissan_", "column_2": 33},
        {"column_1": "suzuki_", "column_2": 0},
    ]
