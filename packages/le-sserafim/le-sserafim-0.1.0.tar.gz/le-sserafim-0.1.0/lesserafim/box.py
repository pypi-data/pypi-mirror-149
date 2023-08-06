
_BOX_LESSERAFIM = [
    6,
    7,
    8,
    9,
    3,
    5,
    4,
    2,
    0,
    1,
]

_BOX_IMFEARLESS = [
    8,
    9,
    7,
    4,
    6,
    5,
    0,
    1,
    2,
    3,
]


def _transform(s: str, box: list[int], padding=' '):
    chars = []
    sub_length = len(box)
    for chunk_idx in range(0, len(s), sub_length):
        sub = s[chunk_idx:chunk_idx+sub_length]
        if len(sub) != sub_length:
            sub += padding * (sub_length - len(sub))
        for idx in box:
            chars.append(sub[idx])
    return ''.join(chars)


def _le_sserafim(s: str, padding=' '):
    return _transform(s=s, box=_BOX_LESSERAFIM, padding=padding)


def _im_fearless(s: str, padding=' '):
    return _transform(s=s, box=_BOX_IMFEARLESS, padding=padding)
