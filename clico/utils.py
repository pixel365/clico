from validators import url, ValidationFailure


def validate_url(s: str) -> str:
    s = s.split('?')[0]
    is_valid = url(value=s, public=True)
    if isinstance(is_valid, ValidationFailure):
        raise ValueError(f'Invalid value `{s}`')
    return s
