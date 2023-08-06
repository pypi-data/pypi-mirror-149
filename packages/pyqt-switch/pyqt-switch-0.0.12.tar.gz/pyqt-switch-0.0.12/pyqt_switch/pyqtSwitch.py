from PyQt5.QtCore import Qt, pyqtSignal, QPropertyAnimation, QPoint, QAbstractAnimation

from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QHBoxLayout


class PyQtSwitch(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self, animation_enabled_flag=False):
        super().__init__()
        self.__btn_width = 20
        self.__btn_height = 20
        self.__animationEnabledFlag = animation_enabled_flag
        self.__initUi()

    def __initUi(self):
        self.__btn = QPushButton()
        self.__btn.setCheckable(True)
        self.__btn.setFixedSize(self.__btn_width, self.__btn_height)
        self.__btn.setStyleSheet('QPushButton { background-color: #FFF; }')
        self.__btn.toggled.connect(self.__toggled)

        self.__layForBtnAlign = QHBoxLayout()
        self.__layForBtnAlign.setAlignment(Qt.AlignLeft)
        self.__layForBtnAlign.addWidget(self.__btn)
        self.__layForBtnAlign.setContentsMargins(0, 0, 0, 0)

        innerWidgetForStyle = QWidget()
        innerWidgetForStyle.setLayout(self.__layForBtnAlign)
        self.setStyleSheet(f'QWidget {{ border: 1px solid #AAA; border-radius: {self.__btn_height // 2}px; }}')

        lay = QGridLayout()
        lay.addWidget(innerWidgetForStyle)
        lay.setContentsMargins(0, 0, 0, 0)

        self.setLayout(lay)
        self.setFixedSize(self.__btn_width * 2, self.__btn_height)

        if self.__animationEnabledFlag:
            self.__animation = QPropertyAnimation(self, b'point')
            self.__animation.valueChanged.connect(self.__btn.move)
            self.__animation.setDuration(100)
            self.__animation.setStartValue(QPoint(0, 0))
            self.__animation.setEndValue(QPoint(self.__btn_width, 0))

    def mousePressEvent(self, e):
        self.__btn.toggle()
        return super().mousePressEvent(e)

    def __toggled(self, f):
        if self.__animationEnabledFlag:
            if f:
                self.__animation.setDirection(QAbstractAnimation.Forward)
                self.__animation.start()
            else:
                self.__animation.setDirection(QAbstractAnimation.Backward)
                self.__animation.start()
        else:
            if f:
                self.__btn.move(self.__btn_width, 0)
                self.__layForBtnAlign.setAlignment(Qt.AlignRight)
            else:
                self.__btn.move(0, 0)
                self.__layForBtnAlign.setAlignment(Qt.AlignLeft)
        self.toggled.emit(f)
