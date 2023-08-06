import enum
import logging
import math
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import matc.constants
import matc.globa
import matc.settings

WINDOW_FLAGS = (
    QtCore.Qt.Dialog
    | QtCore.Qt.FramelessWindowHint
    | QtCore.Qt.WindowStaysOnTopHint
)
# With this it seems we don't capture keyboard events: QtCore.Qt.WindowDoesNotAcceptFocus
# QtCore.Qt.BypassWindowManagerHint


class CursorPosition(enum.Enum):
    inner = enum.auto()
    outside = enum.auto()


class BreathingState(enum.Enum):
    inactive = 0
    breathing_in = 1
    breathing_out = 2


class BreathingDlg(QtWidgets.QDialog):
    close_signal = QtCore.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowFlags(WINDOW_FLAGS)
        self.setWindowTitle(f"Breathing Dialog - {matc.constants.APPLICATION_PRETTY_NAME}")
        self.setWindowIcon(QtGui.QIcon(matc.globa.get_app_icon_path("icon.png")))
        self.setStyleSheet(
            f"background-color: {matc.globa.BLACK_COLOR};"
            "color: #999999;"
            f"selection-background-color: {matc.globa.LIGHT_GREEN_COLOR};"
            "selection-color:#000000;"
        )

        self.vbox_l2 = QtWidgets.QVBoxLayout()
        self.vbox_l2.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vbox_l2)

        self.breathing_gv = BreathingGraphicsView()
        self.vbox_l2.addWidget(self.breathing_gv, alignment=QtCore.Qt.AlignHCenter)
        self.breathing_gv.mouse_btn_released_signal.connect(self.on_brdlg_mouse_btn_released)
        self.breathing_gv.mouse_leave_signal.connect(self.on_brdlg_mouse_leave)
        self.breathing_gv.return_pressed_signal.connect(self.on_brdlg_return_pressed)
        # self.breathing_gv.initiate()

    def close_dlg(self):
        # self.showNormal()
        # -for MacOS. showNormal is used here rather than showMinimized to avoid animation
        self.breathing_gv.ib_qtimeline.stop()
        self.breathing_gv.ob_qtimeline.stop()
        # self.breathing_dlg.circle_go.setScale(1)
        self.breathing_gv.hide()
        self.hide()
        self.close_signal.emit()

    def on_brdlg_mouse_btn_released(self):
        self.close_dlg()

    def on_brdlg_mouse_leave(self):
        self.close_dlg()

    def on_brdlg_return_pressed(self):
        self.close_dlg()

    def show_breathing_only(self):
        # self.breathing_dlg.breathing_gi.update_pos_and_origin_point(VIEW_WIDTH_INT, VIEW_HEIGHT_INT)

        if self.isVisible():
            return

        self.adjustSize()  # -also seems to set x and y to 0
        screen_qrect = QtWidgets.QApplication.desktop().availableGeometry()
        _xpos_int = screen_qrect.left() + (screen_qrect.width() - VIEW_WIDTH_INT) // 2
        _ypos_int = screen_qrect.bottom() - VIEW_HEIGHT_INT + 1
        # -self.sizeHint().height() gives only 52 here, unknown why, so we use VIEW_HEIGHT_INT instead
        # logging.debug("screen_qrect.bottom() = " + str(screen_qrect.bottom()))
        # logging.debug("self.sizeHint().height() = " + str(self.sizeHint().height()))
        self.move(_xpos_int, _ypos_int)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.breathing_dlg.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.close_dlg()
        self.showNormal()

        self.breathing_gv.initiate()

    def on_close_clicked(self):
        self.close_dlg()


TIME_NOT_SET_FT = 0.0
TIME_LINE_IB_DURATION_INT = 8000
TIME_LINE_OB_DURATION_INT = 16000
TIME_LINE_DOT_DURATION_INT = 1000
TIME_LINE_IB_FRAME_RANGE_INT = 1000
TIME_LINE_OB_FRAME_RANGE_INT = 2000
TIME_LINE_IB_DOT_FRAME_RANGE_INT = 255

VIEW_WIDTH_INT = 540
VIEW_HEIGHT_INT = 270
BR_CIRCLE_RADIUS_FT = 45.0

DOT_RADIUS_FT = 7
DOT_SPACING = 3


class BreathingGraphicsView(QtWidgets.QGraphicsView):
    mouse_btn_released_signal = QtCore.pyqtSignal()
    mouse_leave_signal = QtCore.pyqtSignal()
    first_breathing_gi_signal = QtCore.pyqtSignal()
    return_pressed_signal = QtCore.pyqtSignal()

    # Also contains the graphics scene
    def __init__(self, i_can_be_closed: bool = True) -> None:
        super().__init__()

        self.breathing_count = 0
        self.br_dots_gi_list = []

        self.first_shown: bool = True
        self.breathing_state = BreathingState.inactive
        self._can_be_closed_bool = i_can_be_closed
        self._keyboard_active_bool = True
        self._start_time_ft = TIME_NOT_SET_FT
        self._ib_length_ft_list = []
        self._ob_length_ft_list = []

        # Window setup
        self.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        self.setLineWidth(0)
        # self.setStyleSheet("border-radius: 15px;")
        self.setFixedWidth(VIEW_WIDTH_INT)
        self.setFixedHeight(VIEW_HEIGHT_INT)
        t_brush = QtGui.QBrush(QtGui.QColor(matc.globa.BLACK_COLOR))
        self.setBackgroundBrush(t_brush)
        self.setRenderHints(
            QtGui.QPainter.Antialiasing |
            QtGui.QPainter.SmoothPixmapTransform
        )
        self.setAlignment(QtCore.Qt.AlignCenter)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        # ..set position
        screen_qrect = QtWidgets.QApplication.desktop().availableGeometry()
        self._xpos_int = screen_qrect.left() + (screen_qrect.width() - VIEW_WIDTH_INT) // 2
        self._ypos_int = screen_qrect.bottom() - VIEW_HEIGHT_INT - 60
        # -self.sizeHint().height() gives only 52 here, unknown why, so we use VIEW_HEIGHT_INT instead
        self.move(self._xpos_int, self._ypos_int)

        # Graphics and layout setup..
        vbox_l2 = QtWidgets.QVBoxLayout()
        self.setLayout(vbox_l2)
        # ..graphics scene
        self._graphics_scene = QtWidgets.QGraphicsScene()
        self._graphics_scene.setSceneRect(QtCore.QRectF(0, 0, VIEW_WIDTH_INT, VIEW_HEIGHT_INT))
        self.setScene(self._graphics_scene)

        # ..help text
        help_text_str = "Hover over the green box breathing in and outside the green box breathing out"
        self.help_text_gi = MyQGraphicsTextItem()
        self.help_text_gi.setHtml(matc.globa.get_html(help_text_str, 18))
        self._graphics_scene.addItem(self.help_text_gi)

        # ..text
        self.text_gi = MyQGraphicsTextItem()
        # self.text_gi.setAcceptHoverEvents(False)  # -so that the underlying item will not be disturbed
        self.text_gi.position_signal.connect(self._breathing_gi_position_changed)
        self._graphics_scene.addItem(self.text_gi)

        # Animation
        self.ib_qtimeline = QtCore.QTimeLine(duration=TIME_LINE_IB_DURATION_INT)
        self.ib_qtimeline.setFrameRange(1, TIME_LINE_IB_FRAME_RANGE_INT)
        self.ib_qtimeline.setCurveShape(QtCore.QTimeLine.LinearCurve)
        self.ib_qtimeline.frameChanged.connect(self.frame_change_breathing_in)
        self.ob_qtimeline = QtCore.QTimeLine(duration=TIME_LINE_OB_DURATION_INT)
        self.ob_qtimeline.setFrameRange(1, TIME_LINE_OB_FRAME_RANGE_INT)
        self.ob_qtimeline.setCurveShape(QtCore.QTimeLine.LinearCurve)
        self.ob_qtimeline.frameChanged.connect(self.frame_change_breathing_out)

        self.breathing_phrase = None
        ##### self.initiate()

        # https://forum.qt.io/topic/106003/how-to-seamlessly-place-item-into-scene-at-specific-location-adding-qgraphicsitem-to-scene-always-places-it-at-0-0/2


        # ..custom dynamic breathing graphic (may be possible to change this in the future)

        self.br_vis_go_list = []

        bar_go = BreathingBarQgo()
        bar_go.hide()
        self.br_vis_go_list.append(bar_go)
        self._graphics_scene.addItem(bar_go)

        c_go = BreathingCircleQgo()
        c_go.hide()
        self.br_vis_go_list.append(c_go)
        self._graphics_scene.addItem(c_go)

        self.dot_qtimeline = QtCore.QTimeLine(duration=TIME_LINE_DOT_DURATION_INT)
        self.dot_qtimeline.setFrameRange(1, TIME_LINE_IB_DOT_FRAME_RANGE_INT)
        # self.dot_qtimeline.setCurveShape(QtCore.QTimeLine.EaseOutCurve)
        # self.dot_qtimeline.setEasingCurve(QtCore.QEasingCurve.OutQuad)
        self.dot_qtimeline.setEasingCurve(QtCore.QEasingCurve.InOutQuad)
        self.dot_qtimeline.frameChanged.connect(self.on_frame_change_dot)

    def on_text_hover(self):
        self._breathing_gi_position_changed(CursorPosition.inner.value)

    def show(self):
        raise Exception("Call not supported, call function in super class instead, or use initiate")

    def initiate(self):
        self.breathing_state = BreathingState.inactive

        self.breathing_count = 0
        for br_dot in self.br_dots_gi_list:
            self._graphics_scene.removeItem(br_dot)
        self.br_dots_gi_list.clear()

        for br_vis_go in self.br_vis_go_list:
            br_vis_go.hide()
        br_vis: int = matc.settings.settings[matc.settings.SK_BREATHING_VISUALIZATION]
        self.active_br_go = self.br_vis_go_list[br_vis]
        self.active_br_go.show()
        self.active_br_go.update_pos_and_origin_point()
        self.active_br_go.position_signal.connect(self._breathing_gi_position_changed)

        if matc.globa.active_phrase_id == matc.globa.BREATHING_PHRASE_NOT_SET:
            self.breathing_phrase = matc.settings.get_topmost_breathing_phrase()
            matc.globa.active_phrase_id = self.breathing_phrase.id
        self.breathing_phrase = matc.settings.get_breathing_phrase(matc.globa.active_phrase_id)

        help_text_pointf = QtCore.QPointF(
            VIEW_WIDTH_INT / 2 - self.help_text_gi.boundingRect().width() / 2,
            10
        )
        self.help_text_gi.setPos(help_text_pointf)
        self.help_text_gi.show()

        self.text_gi.setHtml(self._get_ib_ob_html())
        text_pointf = QtCore.QPointF(
            VIEW_WIDTH_INT / 2 - self.text_gi.boundingRect().width() / 2,
            VIEW_HEIGHT_INT - self.text_gi.boundingRect().height() - 10
        )
        self.text_gi.setPos(text_pointf)

        super().show()

        move_mouse_cursor: bool = matc.settings.settings[matc.settings.SK_MOVE_MOUSE_CURSOR]
        if self.first_shown:
            self.first_shown = False
        elif move_mouse_cursor:
            screen_point = self.mapToGlobal(QtCore.QPoint(35, 35))
            screen = QtGui.QGuiApplication.primaryScreen()
            mouse_cursor = QtGui.QCursor()
            mouse_cursor.setPos(screen, screen_point)
            # https://doc.qt.io/qt-5/qcursor.html#setPos-1

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        super().mousePressEvent(event)
        event.accept()
        if self._can_be_closed_bool:
            self.mouse_btn_released_signal.emit()

    def leaveEvent(self, i_qevent) -> None:
        if self._can_be_closed_bool:
            self.mouse_leave_signal.emit()

    def _get_ib_ob_html(self, i_ib_underscore: bool = False, i_ob_underscore: bool = False) -> str:
        ib_html: str = matc.globa.get_html(self.breathing_phrase.in_breath, 18, i_ib_underscore)
        ob_html: str = matc.globa.get_html(self.breathing_phrase.out_breath, 18, i_ob_underscore)
        return ib_html + ob_html

    def _start_breathing_in(self) -> None:
        if self.breathing_state == BreathingState.breathing_in:
            return
        self.breathing_state = BreathingState.breathing_in

        self.on_frame_change_dot(TIME_LINE_IB_DOT_FRAME_RANGE_INT)

        self.breathing_count += 1
        br_dots_gi = DotQgo(self.breathing_count)
        self.br_dots_gi_list.append(br_dots_gi)
        self._graphics_scene.addItem(br_dots_gi)
        br_dots_gi.show()
        for br_dot in self.br_dots_gi_list:
            br_dot.update_pos(len(self.br_dots_gi_list))

        if self.breathing_count == 1:
            self.first_breathing_gi_signal.emit()

        self.help_text_gi.hide()

        self.text_gi.setHtml(self._get_ib_ob_html(i_ib_underscore=True))
        self.ob_qtimeline.stop()
        self.ib_qtimeline.start()

        self.dot_qtimeline.stop()
        self.dot_qtimeline.start()

    def _start_breathing_out(self) -> None:
        if self.breathing_state != BreathingState.breathing_in:
            return
        self.breathing_state = BreathingState.breathing_out

        self.active_br_go._peak_width_ft = self.active_br_go.rectf.width()

        self.text_gi.setHtml(self._get_ib_ob_html(i_ob_underscore=True))
        self.ib_qtimeline.stop()
        self.ob_qtimeline.start()

    def keyPressEvent(self, i_qkeyevent) -> None:
        if self._keyboard_active_bool:
            if i_qkeyevent.key() == QtCore.Qt.Key_Shift:
                logging.debug("shift key pressed")
                self._start_breathing_in()
            elif i_qkeyevent.key() == QtCore.Qt.Key_Return:
                logging.debug("return key pressed")
                self.return_pressed_signal.emit()

    def keyReleaseEvent(self, i_qkeyevent) -> None:
        if self._keyboard_active_bool:
            if i_qkeyevent.key() == QtCore.Qt.Key_Shift:
                logging.debug("shift key released")
                self._start_breathing_out()

    def _breathing_gi_position_changed(self, i_pos_type: int) -> None:
        if i_pos_type == CursorPosition.inner.value:
            self._start_breathing_in()
            # self.circle_go.update_pos_and_origin_point(VIEW_WIDTH_INT, VIEW_HEIGHT_INT)

        elif i_pos_type == CursorPosition.outside.value:
            self._start_breathing_out()
            # self.text_gi.update_pos_and_origin_point(VIEW_WIDTH_INT, VIEW_HEIGHT_INT)
            # self.circle_go.update_pos_and_origin_point(VIEW_WIDTH_INT, VIEW_HEIGHT_INT)

        """
        # Calculating coords..
        # ..breathing rectangle/area
        hover_rectangle_qsize = QtCore.QSizeF(BR_WIDTH_FT, BR_HEIGHT_FT)
        x: float = self.circle_go.x() + (self.circle_go.boundingRect().width() - hover_rectangle_qsize.width()) / 2
        y: float = self.circle_go.y() + (self.circle_go.boundingRect().height() - hover_rectangle_qsize.height()) / 2
        pos_pointf = QtWidgets.QGraphicsItem.mapFromItem(self.circle_go, self.circle_go, x, y)  # -widget coords
        hover_rectangle_coords_qrect = QtCore.QRectF(pos_pointf, hover_rectangle_qsize)
        logging.debug(f"{hover_rectangle_coords_qrect=}")
        # ..mouse cursor
        cursor = QtGui.QCursor()  # -screen coords
        cursor_pos_widget_coords_qp = self.mapFromGlobal(cursor.pos())  # -widget coords
        logging.debug(f"{cursor_pos_widget_coords_qp=}")

        # Check if cursor is inside the area, and start the animation
        if hover_rectangle_coords_qrect.contains(cursor_pos_widget_coords_qp):
            matc.globa.breathing_state = matc.globa.BreathingState.breathing_in
            self._start_breathing_in()
            self.circle_go.update_pos_and_origin_point(VIEW_WIDTH_INT, VIEW_HEIGHT_INT)
        """

    def frame_change_breathing_in(self, i_frame_nr: int) -> None:
        # new_scale_int_ft = 1 + 0.001 * i_frame_nr
        # self.circle_go.setScale(new_scale_int_ft)

        self.active_br_go.change_size_br_in(i_frame_nr)

    def frame_change_breathing_out(self, i_frame_nr: int) -> None:
        # self.circle_go.setScale(new_scale_int_ft)

        self.active_br_go.change_size_br_out(i_frame_nr)

    def on_frame_change_dot(self, i_frame_nr: int) -> None:
        if len(self.br_dots_gi_list) <= 0:
            return
        last_dot_git: DotQgo = self.br_dots_gi_list[-1]
        last_dot_git.color.setAlpha(i_frame_nr)
        last_dot_git.update()
        # self._graphics_scene.update(last_dot_git.rectf)
        # last_dot_git.paint()


class MyQGraphicsTextItem(QtWidgets.QGraphicsTextItem):
    position_signal = QtCore.pyqtSignal(int)

    def __init__(self) -> None:
        super().__init__()
        self.setDefaultTextColor(QtGui.QColor(matc.globa.DARKER_GREEN_COLOR))
        self.setTextWidth(VIEW_WIDTH_INT - 20)

    def hoverMoveEvent(self, event: QtWidgets.QGraphicsSceneHoverEvent) -> None:
        cursor_posx = int(event.pos().x())
        cursor_posy = int(event.pos().y())
        upper_rect = QtCore.QRect(
            int(self.boundingRect().x()), int(self.boundingRect().y()),
            int(self.boundingRect().width()), int(self.boundingRect().height() // 2))
        if upper_rect.contains(cursor_posx, cursor_posy):
            self.position_signal.emit(CursorPosition.inner.value)
        else:
            self.position_signal.emit(CursorPosition.outside.value)

    def hoverLeaveEvent(self, i_qgraphicsscenehoverevent) -> None:
        # Please note that this function is entered in case the user hovers over something
        #  on top of this graphics item
        self.position_signal.emit(CursorPosition.outside.value)


class DotQgo(QtWidgets.QGraphicsObject):
    def __init__(self, i_number: int):
        super().__init__()
        self.number = i_number
        self.rectf = QtCore.QRectF(0, 0, 2*DOT_RADIUS_FT, 2*DOT_RADIUS_FT)
        self.setAcceptHoverEvents(False)
        self.color = QtGui.QColor(matc.globa.LIGHT_GREEN_COLOR)
        self.color.setAlpha(0)

    def boundingRect(self):
        return self.rectf

    # Overridden
    def paint(self, i_qpainter: QtGui.QPainter, i_qstyleoptiongraphicsitem, widget=None) -> None:
        # i_qpainter.fillRect(self.rectf, t_brush)
        t_brush = QtGui.QBrush(self.color)
        i_qpainter.setBrush(t_brush)
        pen = QtGui.QPen()
        pen.setWidth(0)
        i_qpainter.setPen(pen)
        i_qpainter.drawEllipse(self.rectf)

    def update_pos(self, i_total_nr: int) -> None:
        x_delta = (self.number - 0.5 - i_total_nr / 2) * (self.boundingRect().width() + DOT_SPACING)
        x: float = VIEW_WIDTH_INT / 2 - self.boundingRect().width() / 2 + x_delta
        y: float = self.boundingRect().height()
        self.setPos(QtCore.QPointF(x, y))


class BreathingQgo(QtWidgets.QGraphicsObject):
    position_signal = QtCore.pyqtSignal(int)

    def change_size_br_in(self, i_frame_nr: int):
        pass

    def change_size_br_out(self, i_frame_nr: int):
        pass

    def __init__(self):
        super().__init__()
        self.rectf = QtCore.QRectF()
        self.setAcceptHoverEvents(True)
        self._peak_width_ft = BR_CIRCLE_RADIUS_FT * 2

    def boundingRect(self):
        return self.rectf

    def update_pos_and_origin_point(self) -> None:
        x: float = VIEW_WIDTH_INT / 2 - self.boundingRect().width() / 2
        y: float = VIEW_HEIGHT_INT / 2 - self.boundingRect().height() / 2
        self.setPos(QtCore.QPointF(x, y))
        self.setTransformOriginPoint(self.boundingRect().center())

    def hoverLeaveEvent(self, i_qgraphicsscenehoverevent) -> None:
        # Please note that this function is entered in case the user hovers over something
        #  on top of this graphics item
        self.position_signal.emit(CursorPosition.outside.value)

    def hoverMoveEvent(self, i_qgraphicsscenehoverevent: QtWidgets.QGraphicsSceneHoverEvent) -> None:
        pass


class BreathingCircleQgo(BreathingQgo):
    """
    "The QGraphicsObject class provides a base class for all graphics items that require signals,
    slots and properties."
    https://doc.qt.io/qt-5/qgraphicsobject.html

    breathing in: ignoring the state of the circle, instead using the same starting state
    breathing out: using the state of the circle
    """

    def __init__(self):
        super().__init__()
        self.rectf = QtCore.QRectF(
            0, 0,
            2*BR_CIRCLE_RADIUS_FT, 2*BR_CIRCLE_RADIUS_FT
        )

    def change_size_br_in(self, i_frame_nr: int):
        new_width_ft = 2 * BR_CIRCLE_RADIUS_FT + 0.1 * i_frame_nr
        self.rectf.setWidth(new_width_ft)
        self.rectf.setHeight(new_width_ft)
        self.update_pos_and_origin_point()

    def change_size_br_out(self, i_frame_nr: int):
        new_width_ft = self._peak_width_ft - 0.06 * i_frame_nr
        if new_width_ft < 2 * BR_CIRCLE_RADIUS_FT:
            new_width_ft = 2 * BR_CIRCLE_RADIUS_FT
        self.rectf.setWidth(new_width_ft)
        self.rectf.setHeight(new_width_ft)
        self.update_pos_and_origin_point()

    # Overridden
    def paint(self, i_qpainter: QtGui.QPainter, i_qstyleoptiongraphicsitem, widget=None) -> None:
        # i_qpainter.fillRect(self.rectf, t_brush)
        t_brush = QtGui.QBrush(QtGui.QColor(matc.globa.LIGHT_GREEN_COLOR))
        i_qpainter.setBrush(t_brush)
        i_qpainter.drawEllipse(self.rectf)

    # Overridden
    def hoverMoveEvent(self, i_qgraphicsscenehoverevent: QtWidgets.QGraphicsSceneHoverEvent) -> None:
        # self.hover_signal.emit()

        cposx = self.boundingRect().center().x()
        cposy = self.boundingRect().center().y()
        # logging.debug(f"{cposy=}")
        pposx = i_qgraphicsscenehoverevent.pos().x()
        pposy = i_qgraphicsscenehoverevent.pos().y()
        # logging.debug(f"{pposy=}")

        distance_from_center: float = math.dist([0, 0], [pposx-cposx, pposy-cposy])
        # logging.debug(f"{distance_from_center=}")

        if distance_from_center < BR_CIRCLE_RADIUS_FT:
            self.position_signal.emit(CursorPosition.inner.value)
        elif distance_from_center > self.rectf.width() // 2:
            self.position_signal.emit(CursorPosition.outside.value)


BR_BAR_WIDTH_FT = 120.0
BR_BAR_HEIGHT_FT = 40.0


class BreathingBarQgo(BreathingQgo):
    def __init__(self):
        super().__init__()
        self.rectf = QtCore.QRectF(
            0, 0,
            BR_BAR_WIDTH_FT, BR_BAR_HEIGHT_FT
        )

    # Overridden
    def paint(self, i_qpainter: QtGui.QPainter, i_qstyleoptiongraphicsitem, widget=None) -> None:
        # i_qpainter.fillRect(self.rectf, t_brush)
        t_brush = QtGui.QBrush(QtGui.QColor(matc.globa.LIGHT_GREEN_COLOR))
        i_qpainter.setBrush(t_brush)
        i_qpainter.drawRoundedRect(self.rectf, 5, 5)

    def change_size_br_in(self, i_frame_nr: int):
        new_width_ft = BR_BAR_WIDTH_FT + 0.2 * i_frame_nr
        self.rectf.setWidth(new_width_ft)
        self.update_pos_and_origin_point()

    def change_size_br_out(self, i_frame_nr: int):
        new_width_ft = self._peak_width_ft - 0.12 * i_frame_nr
        if new_width_ft < BR_BAR_WIDTH_FT:
            new_width_ft = BR_BAR_WIDTH_FT
        self.rectf.setWidth(new_width_ft)
        self.update_pos_and_origin_point()

    # Overridden
    def hoverMoveEvent(self, i_qgraphicsscenehoverevent: QtWidgets.QGraphicsSceneHoverEvent) -> None:
        self.position_signal.emit(CursorPosition.inner.value)
