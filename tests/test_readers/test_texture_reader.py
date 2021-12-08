
from datetime import date

from captif_data_structures.readers import TextureReader


def test_texture_reader_4102a5dd(data_path):
    path = data_path.joinpath("texture", "4102a5dd.dat")
    meta, table_rows, structure_id = TextureReader.load(path)

    assert meta == {
        "date": date(2019, 1, 16),
        "file_number": 0,
    }
    assert table_rows == [
        {"distance_mm": 0, "relative_height_mm": None},
        {"distance_mm": 0.037, "relative_height_mm": None},
        {"distance_mm": 0.075, "relative_height_mm": None},
        {"distance_mm": 0.112, "relative_height_mm": None},
        {"distance_mm": 0.150, "relative_height_mm": None},
        {"distance_mm": 0.187, "relative_height_mm": -0.122},
        {"distance_mm": 0.225, "relative_height_mm": -0.065},
    ]
    assert structure_id == "4102a5dd"


def test_texture_reader_245ff223(data_path):
    path = data_path.joinpath("texture", "245ff223.dat")
    meta, table_rows, structure_id = TextureReader.load(path)

    assert meta == {
        "date": date(2021, 9, 29),
        "file_number": 1,
    }
    assert table_rows == [
        {"distance_mm": 0, "relative_height_mm": -2.232},
        {"distance_mm": 0.037, "relative_height_mm": None},
        {"distance_mm": 0.075, "relative_height_mm": -2.090},
    ]
    assert structure_id == "245ff223"


def test_texture_reader_7cd12dee(data_path):
    path = data_path.joinpath("texture", "7cd12dee.dat")
    meta, table_rows, structure_id = TextureReader.load(path)

    assert meta == {"sample_spacing_mm": 1.0}
    assert table_rows == [
        {"distance_mm": 0, "relative_height_mm": -7.406126},
        {"distance_mm": 1.0, "relative_height_mm": -7.214107},
        {"distance_mm": 2.0, "relative_height_mm": -7.239000},
        {"distance_mm": 3.0, "relative_height_mm": -7.295854},
    ]
    assert structure_id == "7cd12dee"


def test_texture_reader_0319aee1(data_path):
    path = data_path.joinpath("texture", "0319aee1.dat")
    meta, table_rows, structure_id = TextureReader.load(path)

    assert meta == {
        "date": date(2021, 10, 22),
        "file_number": 0,
    }
    assert table_rows == [
        {"distance_mm": 0, "relative_height_mm": -0.027},
        {"distance_mm": 0.037, "relative_height_mm": -0.044},
        {"distance_mm": 0.075, "relative_height_mm": 0.019},
    ]
    assert structure_id == "0319aee1"
