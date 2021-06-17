import pytest
from processor import AdminProcessor, InvalidAdminCommand


@pytest.mark.parametrize("x,y", [("I say pen time five number six seven", "/tp5 67"), ("command clear all", "/clear_all"),
                                 ("pen stop go ten number one two three", "/sg10 123"),
                                 ("pen go number one two three", '/dt 123')])
def test_get(x, y):
    p = AdminProcessor()
    try:
        assert p.get(x) == y
    except InvalidAdminCommand:
        assert None is y
