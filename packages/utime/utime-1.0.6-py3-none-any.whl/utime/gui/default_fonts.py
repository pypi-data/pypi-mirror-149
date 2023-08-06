from PyQt5.QtGui import QFont


class TitleFont(QFont):
    def __init__(self, bold=True, parent=None):
        super(TitleFont, self).__init__(parent)
        self.setBold(bold)
        self.setPointSize(16)


class LargeTitleFont(QFont):
    def __init__(self, parent=None):
        super(LargeTitleFont, self).__init__(parent)
        self.setBold(True)
        self.setPointSize(22)


COLOR_SHEETS = {
    "yellow": "color: #fcb911;",
    "green": "color: #38c44b;",
    "red": "color: #bc2525;"
}
