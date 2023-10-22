from avda.helper import get_avid_from_title
import pytest


get_avid_from_title_testdata = [
    ("FC2-3611004 【#102】色白152cmあざと可", "FC2-3611004"),
    ("MIDV-024 エロス覚醒 めちゃイキ追撃4本番 激イキ161回 子宮痙攣189回 マン汁2448cc 石川澪", "MIDV-024"),
    ("SDDE-664-トビジオっ! 学園ハイスクール 学校にいる間はずっと潮吹きっぱなし・失", "SDDE-664"),
]


@pytest.mark.parametrize(
    "title,expected",
    get_avid_from_title_testdata,
    ids=[i for i in range(1, len(get_avid_from_title_testdata) + 1)],
)
def test_get_avid_from_title(title, expected: str):
    assert get_avid_from_title(title) == expected
