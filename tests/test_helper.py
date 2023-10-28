from avda.helper import avid
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
    assert avid.get_avid_from_title(title) == expected


@pytest.mark.parametrize(
    "filename,expected",
    [
        ("ABP-123.nfo", "ABP-123"),
        ("ssis-456.NFO", "SSIS-456"),
        ("ipz-789-c.nfo", "IPZ-789"),
        ("midv-001-UC.nfo", "MIDV-001"),
        ("heyzo-6666.nfo", "HEYZO-6666"),
    ],
)
def test_get_avid_from_filename(filename, expected: str):
    assert avid.get_avid_from_filename(filename) == expected
