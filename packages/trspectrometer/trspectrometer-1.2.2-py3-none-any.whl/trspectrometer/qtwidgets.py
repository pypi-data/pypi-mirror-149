import os

from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import Qt

class FlowLayout(QtWidgets.QLayout):
    """
    A ``QLayout`` which arranges its child widgets horizontally and vertically.

    A Qt for Python port of the `layouts/flowlayout <https://doc.qt.io/qt-5/qtwidgets-layouts-flowlayout-example.html>`_ example.
    If enough horizontal space is available, it looks like an ``HBoxLayout``, but if space is lacking, it automatically wraps its children into multiple rows.
    """
    heightChanged = QtCore.Signal(int)

    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)
        if parent is not None:
            self.setContentsMargins(margin, margin, margin, margin)
        self.setSpacing(spacing)

        self._item_list = []

    def __del__(self):
        while self.count():
            self.takeAt(0)

    def addItem(self, item):  # pylint: disable=invalid-name
        self._item_list.append(item)

    def addSpacing(self, size):  # pylint: disable=invalid-name
        self.addItem(QtWidgets.QSpacerItem(size, 0, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum))

    def count(self):
        return len(self._item_list)

    def itemAt(self, index):  # pylint: disable=invalid-name
        if 0 <= index < len(self._item_list):
            return self._item_list[index]
        return None

    def takeAt(self, index):  # pylint: disable=invalid-name
        if 0 <= index < len(self._item_list):
            return self._item_list.pop(index)
        return None

    def expandingDirections(self):  # pylint: disable=invalid-name,no-self-use
        return Qt.Orientations(Qt.Orientation(0))

    def hasHeightForWidth(self):  # pylint: disable=invalid-name,no-self-use
        return True

    def heightForWidth(self, width):  # pylint: disable=invalid-name
        height = self._do_layout(QtCore.QRect(0, 0, width, 0), True)
        return height

    def setGeometry(self, rect):  # pylint: disable=invalid-name
        super().setGeometry(rect)
        self._do_layout(rect, False)

    def sizeHint(self):  # pylint: disable=invalid-name
        return self.minimumSize()

    def minimumSize(self):  # pylint: disable=invalid-name
        size = QtCore.QSize()

        for item in self._item_list:
            minsize = item.minimumSize()
            extent = item.geometry().bottomRight()
            size = size.expandedTo(QtCore.QSize(minsize.width(), extent.y()))

        margin = self.contentsMargins().left()
        size += QtCore.QSize(2 * margin, 2 * margin)
        return size

    def _do_layout(self, rect, test_only=False):
        m = self.contentsMargins()
        effective_rect = rect.adjusted(+m.left(), +m.top(), -m.right(), -m.bottom())
        x = effective_rect.x()
        y = effective_rect.y()
        line_height = 0

        for item in self._item_list:
            wid = item.widget()

            space_x = self.spacing()
            space_y = self.spacing()
            if wid is not None:
                space_x += wid.style().layoutSpacing(
                    QtWidgets.QSizePolicy.PushButton, QtWidgets.QSizePolicy.PushButton, Qt.Horizontal)
                space_y += wid.style().layoutSpacing(
                    QtWidgets.QSizePolicy.PushButton, QtWidgets.QSizePolicy.PushButton, Qt.Vertical)

            next_x = x + item.sizeHint().width() + space_x
            if next_x - space_x > effective_rect.right() and line_height > 0:
                x = effective_rect.x()
                y = y + line_height + space_y
                next_x = x + item.sizeHint().width() + space_x
                line_height = 0

            if not test_only:
                item.setGeometry(QtCore.QRect(QtCore.QPoint(x, y), item.sizeHint()))

            x = next_x
            line_height = max(line_height, item.sizeHint().height())

        new_height = y + line_height - rect.y()
        self.heightChanged.emit(new_height)
        return new_height


class AspectRatioPixmapLabel(QtWidgets.QLabel):
    """
    A QLabel which maintains the correct aspect ratio of the contained image upon resize.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._pixmap = None
        self.setMinimumSize(1, 1)
    
    def setPixmap(self, pixmap):
        self._pixmap = pixmap
        super().setPixmap(self.scaledPixmap())
    
    def heightForWidth(self, width):
        if self._pixmap is None: return self.height()
        return self._pixmap.height()*width/self._pixmap.width()
    
    def sizeHint(self):
        width = self.width()
        return QtCore.QSize(width, self.heightForWidth(width))
    
    def scaledPixmap(self):
        return self._pixmap.scaled(QtCore.QSize(self.size()), Qt.KeepAspectRatio, Qt.SmoothTransformation)
    
    def resizeEvent(self, event):
        if self._pixmap is None: return
        super().setPixmap(self.scaledPixmap())

