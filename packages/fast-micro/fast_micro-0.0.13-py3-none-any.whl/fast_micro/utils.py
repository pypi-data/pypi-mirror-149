from fast_micro.constants import UNDERSCORE_RE


def camelize(data: str) -> str:
    """Convert a string to camelCase.

    Parameters
    ----------
    data : str
        snake_case string

    Returns
    -------
    str
        camelized string
    """
    s = str(data)
    str_items = []

    def _replace_fn(match):
        """
        For string "hello_world", match will contain
            the regex capture group for "o_w".
        :rtype: str
        """
        return match.group(1) + match.group(2).upper()

    str_items.extend(
        [
            s[0].lower() if not s[:2].isupper() else s[0],
            UNDERSCORE_RE.sub(_replace_fn, s)[1:],
        ]
    )
    return "".join(str_items)