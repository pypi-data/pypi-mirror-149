class SlashTypeError(Exception):
    def __init__(self, text: str) -> None: ...


class SlashRulesError(Exception):
    def __init__(self, text: str) -> None: ...


class SlashBadColumnNameError(Exception):
    def __init__(self, text: str) -> None: ...


class SlashBadAction(Exception):
    def __init__(self, text: str) -> None: ...


class SlashPatternMismatch(Exception):
    def __init__(self, text: str) -> None: ...


class SlashLenMismatch(Exception):
    def __init__(self, text: str) -> None: ...


class SlashOneTableColumn(Exception):
    def __init__(self, text: str) -> None: ...


class SlashNoResultToFetch(Exception):
    def __init__(self, text: str) -> None: ...


class SlashUnexpectedError(Exception):
    def __init__(self, text: str) -> None: ...


class SlashNotTheSame(Exception):
    def __init__(self, text: str) -> None: ...


class SlashAttributeError(Exception):
    def __init__(self, text: str) -> None: ...
