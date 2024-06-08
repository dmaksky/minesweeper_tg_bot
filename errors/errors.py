class MinesweeperError(Exception):
    pass


class FieldGenerationError(MinesweeperError):
    pass


class MinesGenerationError(MinesweeperError):
    pass


class CellOpeningError(MinesweeperError):
    pass


class MarkToggleError(MinesweeperError):
    pass
