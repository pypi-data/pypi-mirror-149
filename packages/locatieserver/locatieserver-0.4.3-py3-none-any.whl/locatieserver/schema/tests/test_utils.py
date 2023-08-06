from locatieserver.schema.utils import Point, point_matcher


def test_point_regex():

    x = point_matcher.findall("POINT(5.10696041 52.06415055)")

    assert len(x[0]) == 2

    x = point_matcher.findall("POINT(179534 548410)")

    assert len(x[0]) == 2


def test_point():
    centroide_ll = Point("POINT(5.10696041 52.06415055)")

    assert centroide_ll.x == "5.10696041"
    assert centroide_ll.y == "52.06415055"

    centroide_ll = Point("POINT(10696041 06415055)")

    assert centroide_ll.x == "10696041"
    assert centroide_ll.y == "06415055"


def test_point_empty():
    centroide_ll = Point("")

    assert centroide_ll.x is None


def test_point_non_point_value():
    centroide_ll = Point("XYZ(1.0 2.0)")

    assert centroide_ll.x == "1.0"


def test_point_string_value():
    centroide_ll = Point("ABC")

    assert centroide_ll.x is None
