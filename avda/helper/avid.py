import re
import typing


def get_avid_from_title(title: str) -> typing.Optional[str]:
    pattern = r"[A-Za-z0-9]+-\d+"
    result = re.search(pattern, title)
    if result:
        return result.group(0)
    return "unknown"


AVID_RULES = {
    "tokyo.*hot": lambda x: str(
        re.search(r"(cz|gedo|k|n|red-|se)\d{2,4}", x, re.I).group()
    ),
    "carib": lambda x: str(re.search(r"\d{6}(-|_)\d{3}", x, re.I).group()).replace(
        "_", "-"
    ),
    "1pon|mura|paco": lambda x: str(
        re.search(r"\d{6}(-|_)\d{3}", x, re.I).group()
    ).replace("-", "_"),
    "10mu": lambda x: str(re.search(r"\d{6}(-|_)\d{2}", x, re.I).group()).replace(
        "-", "_"
    ),
    "x-art": lambda x: str(re.search(r"x-art\.\d{2}\.\d{2}\.\d{2}", x, re.I).group()),
    "xxx-av": lambda x: "".join(
        ["xxx-av-", re.findall(r"xxx-av[^\d]*(\d{3,5})[^\d]*", x, re.I)[0]]
    ),
    "heydouga": lambda x: "heydouga-"
    + "-".join(re.findall(r"(\d{4})[\-_](\d{3,4})[^\d]*", x, re.I)[0]),
    "heyzo": lambda x: "HEYZO-" + re.findall(r"heyzo[^\d]*(\d{4})", x, re.I)[0],
    "mdbk": lambda x: str(re.search(r"mdbk(-|_)(\d{4})", x, re.I).group()),
    "mdtm": lambda x: str(re.search(r"mdtm(-|_)(\d{4})", x, re.I).group()),
    "caribpr": lambda x: str(re.search(r"\d{6}(-|_)\d{3}", x, re.I).group()).replace(
        "_", "-"
    ),
}


def get_avid_from_filename(filename: str) -> typing.Optional[str]:
    try:
        for k, v in AVID_RULES.items():
            if re.search(k, filename, re.I):
                return v(filename)
    except:
        pass
    return None
