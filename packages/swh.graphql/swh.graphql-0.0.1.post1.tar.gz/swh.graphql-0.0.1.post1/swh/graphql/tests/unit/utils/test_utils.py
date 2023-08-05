import datetime

from swh.graphql.utils import utils


class TestUtils:
    def test_b64encode(self):
        assert utils.b64encode("testing") == "dGVzdGluZw=="

    def test_get_encoded_cursor_is_none(self):
        assert utils.get_encoded_cursor(None) is None

    def test_get_encoded_cursor(self):
        assert utils.get_encoded_cursor(None) is None
        assert utils.get_encoded_cursor("testing") == "dGVzdGluZw=="

    def test_get_decoded_cursor_is_none(self):
        assert utils.get_decoded_cursor(None) is None

    def test_get_decoded_cursor(self):
        assert utils.get_decoded_cursor("dGVzdGluZw==") == "testing"

    def test_str_to_sha1(self):
        assert (
            utils.str_to_sha1("208f61cc7a5dbc9879ae6e5c2f95891e270f09ef")
            == b" \x8fa\xccz]\xbc\x98y\xaen\\/\x95\x89\x1e'\x0f\t\xef"
        )

    def test_get_formatted_date(self):
        date = datetime.datetime(
            2015, 8, 4, 22, 26, 14, 804009, tzinfo=datetime.timezone.utc
        )
        assert utils.get_formatted_date(date) == "2015-08-04T22:26:14.804009+00:00"

    def test_paginated(self):
        source = [1, 2, 3, 4, 5]
        response = utils.paginated(source, first=50)
        assert response.results == source
        assert response.next_page_token is None

    def test_paginated_first_arg(self):
        source = [1, 2, 3, 4, 5]
        response = utils.paginated(source, first=2)
        assert response.results == source[:2]
        assert response.next_page_token == "2"

    def test_paginated_after_arg(self):
        source = [1, 2, 3, 4, 5]
        response = utils.paginated(source, first=2, after="2")
        assert response.results == [3, 4]
        assert response.next_page_token == "4"

        response = utils.paginated(source, first=2, after="3")
        assert response.results == [4, 5]
        assert response.next_page_token is None

    def test_paginated_endcursor_outside(self):
        source = [1, 2, 3, 4, 5]
        response = utils.paginated(source, first=2, after="10")
        assert response.results == []
        assert response.next_page_token is None
