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
    
    def deselect_all(self):
        for item in self.__data:
            item.selected = False
    
    def get_at_position(self, x, y):
        return [item for item in self.__data if item.contains(x, y)]
    
    def get_last_at_position(self, x, y):
        circles = self.get_at_position(x, y)
        return circles[-1] if circles else None
    
    def get_selected(self):
        return [item for item in self.__data if item.selected]
    
    def toggle_selection_at(self, x, y):
        for item in self.__data:
            if item.contains(x, y):
                item.selected = not item.selected
    
    def select_at(self, x, y):
        for item in self.__data:
            item.selected = item.contains(x, y)

    def toggle_selection_last_at(self, x, y):
        circle = self.get_last_at_position(x, y)
        if circle:
            circle.selected = not circle.selected
    
    def select_last_at(self, x, y):
        self.deselect_all()
        circle = self.get_last_at_position(x, y)
        if circle:
            circle.selected = True

class CCircle:
    def __init__(self, x, y, radius=20, color=Qt.GlobalColor.black):
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
        pen.setWidth(2)
        if self.selected:
            painter.setBrush(Qt.GlobalColor.red)
        else:
            painter.setBrush(Qt.GlobalColor.blue)
        painter.drawEllipse(QRectF(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2))

class CCircleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(600, 600, 600, 600)
        self.storage = Container()
        self.setWindowTitle("Лабораторная работа 3. Часть 1: Круги на форме")
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
            if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                self.storage.toggle_selection_last_at(x, y)
            else:
                if not self.storage.get_at_position(x, y):
                    self.storage.deselect_all()
                    self.storage.add(CCircle(x, y))
                else:
                    self.storage.select_last_at(x, y)
            
            self.update()

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Backspace:
            for circle in self.storage.get_selected():
                self.storage.remove(circle)
            self.update()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CCircleWidget()
    sys.exit(app.exec())