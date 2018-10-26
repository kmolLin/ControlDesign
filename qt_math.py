import sys
from pylab import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg
from PyQt5 import QtGui, QtCore, QtWidgets


def math_tex_to_qpixmap(math_tex: str, fs: int):

    # set up a mpl figure instance

    fig = Figure()
    fig.patch.set_facecolor('none')
    fig.set_canvas(FigureCanvasAgg(fig))
    renderer = fig.canvas.get_renderer()

    # plot the math_tex expression
    ax = fig.add_axes([0, 0, 1, 1])
    ax.axis('off')
    ax.patch.set_facecolor('none')
    t = ax.text(0, 0, math_tex, ha='left', va='bottom', fontsize=fs)

    # fit figure size to text artist
    f_width, f_height = fig.get_size_inches()
    fig_bbox = fig.get_window_extent(renderer)
    text_bbox = t.get_window_extent(renderer)
    tight_fwidth = text_bbox.width * f_width / fig_bbox.width
    tight_fheight = text_bbox.height * f_height / fig_bbox.height
    fig.set_size_inches(tight_fwidth, tight_fheight)

    # convert mpl figure to QPixmap
    buf, size = fig.canvas.print_to_buffer()
    qimage = QtGui.QImage.rgbSwapped(QtGui.QImage(buf, size[0], size[1],
                                                  QtGui.QImage.Format_ARGB32))
    qpixmap = QtGui.QPixmap(qimage)

    return qpixmap


class MyQTableWidget(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        super(MyQTableWidget, self).__init__(parent)
        self.setHorizontalHeader(MyHorizHeader(self))

    def set_math_header_labels(self, header_labels, font_size):
        qpixmaps = []
        index = 0
        for label in header_labels:
            qpixmaps.append(math_tex_to_qpixmap(label, font_size))
            self.setColumnWidth(index, qpixmaps[index].size().width() + 16)
            index += 1

        self.horizontalHeader().qpixmaps = qpixmaps
        self.setHorizontalHeaderLabels(header_labels)


class MyHorizHeader(QtWidgets.QHeaderView):

    def __init__(self, parent):
        super(MyHorizHeader, self).__init__(QtCore.Qt.Horizontal, parent)

        self.setSectionsClickable(True)
        self.setStretchLastSection(True)

        self.qpixmaps = []

    def paintSection(self, painter, rect, logical_index):

        if not rect.isValid():
            return

        # ------------------------------ paint section (without the label) ----

        opt = QtWidgets.QStyleOptionHeader()
        self.initStyleOption(opt)

        opt.rect = rect
        opt.section = logical_index
        opt.text = ""

        # ---- mouse over highlight ----

        mouse_pos = self.mapFromGlobal(QtGui.QCursor.pos())
        if rect.contains(mouse_pos):
            opt.state |= QtWidgets.QStyle.State_MouseOver

        # ---- paint ----

        painter.save()
        self.style().drawControl(QtWidgets.QStyle.CE_Header, opt, painter, self)
        painter.restore()

        # ------------------------------------------- paint mathText label ----

        qpixmap = self.qpixmaps[logical_index]

        # ---- centering ----

        xpix = (rect.width() - qpixmap.size().width()) / 2. + rect.x()
        ypix = (rect.height() - qpixmap.size().height()) / 2.

        # ---- paint ----

        rect = QtCore.QRect(xpix, ypix, qpixmap.size().width(),
                            qpixmap.size().height())
        painter.drawPixmap(rect, qpixmap)

    def sizeHint(self):

        base_size = QtWidgets.QHeaderView.sizeHint(self)

        base_height = base_size.height()
        if len(self.qpixmaps):
            for pixmap in self.qpixmaps:
                base_height = max(pixmap.height() + 8, base_height)
        base_size.setHeight(base_height)

        self.parentWidget().repaint()

        return base_size


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    w = MyQTableWidget()
    w.verticalHeader().hide()

    labels = [
        '$x= \\alpha+\\frac{1}{a_1+\\frac{1}{a_2+\\frac{1}{a_3+\\frac{1}{a_4}}}}$',
        '$k_{soil}=\\frac{\\sum f_j k_j \\theta_j}{\\sum f_j \\theta_j}$',
        '$\\lambda_{soil}=k_{soil} / C_{soil}$']

    w.setColumnCount(len(labels))
    w.set_math_header_labels(labels, 25)
    w.setRowCount(3)
    w.setAlternatingRowColors(True)

    k = 1
    for j in range(3):
        for i in range(3):
            w.setItem(i, j, QtWidgets.QTableWidgetItem(f'Value {k}'))
            k += 1

    w.show()
    w.resize(700, 200)

    sys.exit(app.exec_())
