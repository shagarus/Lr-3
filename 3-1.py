import sys
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtGui import QPen, QPainter, QMouseEvent, QKeyEvent, QColor
from PyQt6.QtCore import Qt, QRectF

class Container:
    def __init__(self):
        self.__data = []
    def add(self, obj):
        self.__data.append(obj)
    def remove(self, obj):
        self.__data.remove(obj)
    def get_all(self):
        return self.__data[:]

class CCircle:
    def __init__(self, x, y, radius=20, color=Qt.GlobalColor.white):
        self.x = x
        self.y = y
        self.radius = radius
        self.selected = False
        self.color = color
    
    def contains(self, x, y):
        return (x - self.x) ** 2 + (y - self.y) ** 2 <= self.radius ** 2
    
    def draw(self, painter: QPainter):
        pen = QPen(self.color)
        painter.setPen(pen)
        if self.selected:
            painter.setBrush(Qt.GlobalColor.white)
        else:
            painter.setBrush(Qt.GlobalColor.blue)
        painter.drawEllipse(QRectF(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2))

class CCirclewidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(600, 600, 600, 600)
        self.storage = Container()
        self.show()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        for circle in self.storage.get_all():
            circle.draw(painter)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position()
            x = pos.x()
            y = pos.y()
            circle_click = False
            for circle in (self.storage.get_all()):
                if circle.contains(x, y):
                    if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                        circle.selected = not circle.selected
                    else:
                        for c in self.storage.get_all():
                            c.selected = False
                        circle.selected = True
                    circle_click = True
                    break
            if not circle_click:
                for c in self.storage.get_all():
                    c.selected = False
                self.storage.add(CCircle(x, y))
            self.update()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Backspace:
            delete = [c for c in self.storage.get_all() if c.selected]
            for c in delete:
                self.storage.remove(c)
            self.update()
    
    def resizeEvent(self, a0):
        self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CCirclewidget()
    sys.exit(app.exec())