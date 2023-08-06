# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# MAIN FILE
# ///////////////////////////////////////////////////////////////
from djsciops.axon_gui.main import *
from pathlib import Path
import djsciops

# GLOBALS
# ///////////////////////////////////////////////////////////////
GLOBAL_STATE = False
GLOBAL_TITLE_BAR = True


class UIFunctions(MainWindow):
    # MAXIMIZE/RESTORE
    # ///////////////////////////////////////////////////////////////
    def maximize_restore(self):
        global GLOBAL_STATE
        status = GLOBAL_STATE
        if status == False:
            self.showMaximized()
            GLOBAL_STATE = True
            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self.ui.maximizeRestoreAppBtn.setToolTip("Restore")
            self.ui.maximizeRestoreAppBtn.setIcon(
                QIcon(":/icons/images/icons/icon_restore.png")
            )
            self.ui.frame_size_grip.hide()
            self.left_grip.hide()
            self.right_grip.hide()
            self.top_grip.hide()
            self.bottom_grip.hide()
        else:
            GLOBAL_STATE = False
            self.showNormal()
            self.resize(self.width() + 1, self.height() + 1)
            self.ui.appMargins.setContentsMargins(10, 10, 10, 10)
            self.ui.maximizeRestoreAppBtn.setToolTip("Maximize")
            self.ui.maximizeRestoreAppBtn.setIcon(
                QIcon(":/icons/images/icons/icon_maximize.png")
            )
            self.ui.frame_size_grip.show()
            self.left_grip.show()
            self.right_grip.show()
            self.top_grip.show()
            self.bottom_grip.show()

    # RETURN STATUS
    # ///////////////////////////////////////////////////////////////
    def returStatus(self):
        return GLOBAL_STATE

    # SET STATUS
    # ///////////////////////////////////////////////////////////////
    def setStatus(self, status):
        global GLOBAL_STATE
        GLOBAL_STATE = status

    # TOGGLE MENU
    # ///////////////////////////////////////////////////////////////
    def toggleMenu(self, enable):
        if enable:
            # GET WIDTH
            width = self.ui.leftMenuBg.width()
            maxExtend = Settings.MENU_WIDTH
            standard = 60

            # SET MAX WIDTH
            if width == 60:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION
            self.animation = QPropertyAnimation(self.ui.leftMenuBg, b"minimumWidth")
            self.animation.setDuration(Settings.TIME_ANIMATION)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QEasingCurve.InOutQuart)
            self.animation.start()

    # TOGGLE LEFT BOX
    # ///////////////////////////////////////////////////////////////
    def toggleLeftBox(self, enable):
        if enable:
            # GET WIDTH
            width = self.ui.extraLeftBox.width()
            maxExtend = Settings.LEFT_BOX_WIDTH
            color = Settings.BTN_LEFT_BOX_COLOR
            standard = 0

            # GET BTN STYLE
            style = self.ui.toggleLeftBox.styleSheet()

            # SET MAX WIDTH
            if width == 0:
                widthExtended = maxExtend
                # SELECT BTN
                self.ui.toggleLeftBox.setStyleSheet(style + color)
            else:
                widthExtended = standard
                # RESET BTN
                self.ui.toggleLeftBox.setStyleSheet(style.replace(color, ""))

        UIFunctions.start_config_box_animation(self, width, "left")

    def start_config_box_animation(self, left_box_width, direction):
        left_width = 0

        # Check values
        if left_box_width == 0 and direction == "left":
            left_width = Settings.LEFT_BOX_WIDTH
        else:
            left_width = 0

        # ANIMATION LEFT BOX
        self.left_box = QPropertyAnimation(self.ui.extraLeftBox, b"minimumWidth")
        self.left_box.setDuration(Settings.TIME_ANIMATION)
        self.left_box.setStartValue(left_box_width)
        self.left_box.setEndValue(left_width)
        self.left_box.setEasingCurve(QEasingCurve.InOutQuart)

        # GROUP ANIMATION
        self.group = QParallelAnimationGroup()
        self.group.addAnimation(self.left_box)
        self.group.start()

    def toggleConsole(self):
        # GET HEIGHT
        height = self.ui.bottomBar.height()
        maxExtend = Settings.CONSOLE_BOX_HEIGHT
        standard = 22

        # SET MAX WIDTH
        if height == 22:
            heightExtended = maxExtend
            self.ui.toggleConsoleBtn.setIcon(
                QIcon(":/icons/images/icons/cil-caret-bottom.png")
            )
        else:
            heightExtended = standard
            self.ui.toggleConsoleBtn.setIcon(
                QPixmap(":icons/images/icons/cil-caret-right.png")
            )

        UIFunctions.start_console_box_animation(self, height)
        self.ui.upload_status.verticalScrollBar().setValue(
            self.ui.upload_status.verticalScrollBar().maximum()
        )
        self.ui.upload_status.ensureCursorVisible()

    def start_console_box_animation(self, console_box_height):
        console_height = 22

        # Check values
        if console_box_height == 22:
            console_height = Settings.CONSOLE_BOX_HEIGHT
        else:
            console_height = 22

        # ANIMATION LEFT BOX
        self.console_box = QPropertyAnimation(self.ui.bottomBar, b"minimumHeight")
        self.console_box.setDuration(Settings.TIME_ANIMATION)
        self.console_box.setStartValue(console_box_height)
        self.console_box.setEndValue(console_height)
        self.console_box.setEasingCurve(QEasingCurve.InOutQuart)

        # GROUP ANIMATION
        self.group = QParallelAnimationGroup()
        self.group.addAnimation(self.console_box)
        self.group.start()

    # SELECT/DESELECT MENU
    # ///////////////////////////////////////////////////////////////
    # SELECT
    def selectMenu(getStyle):
        select = getStyle + Settings.MENU_SELECTED_STYLESHEET
        return select

    # DESELECT
    def deselectMenu(getStyle):
        deselect = getStyle.replace(Settings.MENU_SELECTED_STYLESHEET, "")
        return deselect

    # RESET SELECTION
    def resetStyle(self, widget):
        for w in self.ui.topMenu.findChildren(QPushButton):
            if w.objectName() != widget:
                w.setStyleSheet(UIFunctions.deselectMenu(w.styleSheet()))

    # IMPORT THEMES FILES QSS/CSS
    # ///////////////////////////////////////////////////////////////
    def theme(self, file, useCustomTheme):
        if useCustomTheme:
            str = open(file, "r").read()
            self.ui.styleSheet.setStyleSheet(str)

    # START - GUI DEFINITIONS
    # ///////////////////////////////////////////////////////////////
    def uiDefinitions(self):
        def dobleClickMaximizeRestore(event):
            # IF DOUBLE CLICK CHANGE STATUS
            if event.type() == QEvent.MouseButtonDblClick:
                QTimer.singleShot(250, lambda: UIFunctions.maximize_restore(self))

        self.ui.titleRightInfo.mouseDoubleClickEvent = dobleClickMaximizeRestore

        if Settings.ENABLE_CUSTOM_TITLE_BAR:
            # STANDARD TITLE BAR
            self.setWindowFlags(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)

            # MOVE WINDOW / MAXIMIZE / RESTORE
            def moveWindow(event):
                # IF MAXIMIZED CHANGE TO NORMAL
                if UIFunctions.returStatus(self):
                    UIFunctions.maximize_restore(self)
                # MOVE WINDOW
                if event.buttons() == Qt.LeftButton:
                    self.move(self.pos() + event.globalPos() - self.dragPos)
                    self.dragPos = event.globalPos()
                    event.accept()

            self.ui.titleRightInfo.mouseMoveEvent = moveWindow

            # CUSTOM GRIPS
            self.left_grip = CustomGrip(self, Qt.LeftEdge, True)
            self.right_grip = CustomGrip(self, Qt.RightEdge, True)
            self.top_grip = CustomGrip(self, Qt.TopEdge, True)
            self.bottom_grip = CustomGrip(self, Qt.BottomEdge, True)

        else:
            self.ui.appMargins.setContentsMargins(0, 0, 0, 0)
            self.ui.minimizeAppBtn.hide()
            self.ui.maximizeRestoreAppBtn.hide()
            self.ui.closeAppBtn.hide()
            self.ui.frame_size_grip.hide()

        # DROP SHADOW
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(17)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.bgApp.setGraphicsEffect(self.shadow)

        # RESIZE WINDOW
        self.sizegrip = QSizeGrip(self.ui.frame_size_grip)
        self.sizegrip.setStyleSheet(
            "width: 20px; height: 20px; margin 0px; padding: 0px;"
        )

        # MINIMIZE
        self.ui.minimizeAppBtn.clicked.connect(lambda: self.showMinimized())

        # MAXIMIZE/RESTORE
        self.ui.maximizeRestoreAppBtn.clicked.connect(
            lambda: UIFunctions.maximize_restore(self)
        )

        # CLOSE APPLICATION
        self.ui.closeAppBtn.clicked.connect(lambda: self.close())

    def resize_grips(self):
        if Settings.ENABLE_CUSTOM_TITLE_BAR:
            self.left_grip.setGeometry(0, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 10, 10, 10, self.height())
            self.top_grip.setGeometry(0, 0, self.width(), 10)
            self.bottom_grip.setGeometry(0, self.height() - 10, self.width(), 10)

    # ///////////////////////////////////////////////////////////////
    # END - GUI DEFINITIONS

    # DIRECTORY TREE
    # ///////////////////////////////////////////////////////////////
    def refresh_tree(tree, path_or_dict, method):
        tree.clear()
        if method == "dict":
            UIFunctions.fill_tree_from_dict(tree.invisibleRootItem(), path_or_dict)
        elif method == "path":
            UIFunctions.fill_tree_from_path(
                tree.invisibleRootItem(), path_or_dict, originalpath=path_or_dict
            )
        tree.sortItems(0, Qt.AscendingOrder)

    def fill_tree_from_dict(item, value):
        def new_item(parent, text, val=None):
            child = QTreeWidgetItem([text])
            if len(text.split(".")) == 1:
                child.setIcon(0, QIcon(":/icons/images/icons/cil-folder.png"))
            else:
                child.setIcon(0, QIcon(":/icons/images/icons/cil-file.png"))
            UIFunctions.fill_tree_from_dict(child, val)
            parent.addChild(child)
            child.setExpanded(True)

        if value is None:
            return
        elif isinstance(value, dict):
            for key, val in sorted(value.items()):
                new_item(item, str(key), val)

    def fill_tree_from_path(
        tree, startpath, originalpath=None, checkable=True, checklist=None
    ):
        def new_item(parent, text, path):
            child = QTreeWidgetItem([text, path])
            if os.path.isdir(path):
                child.setIcon(0, QIcon(":/icons/images/icons/cil-folder.png"))
                child.setFlags(
                    child.flags() | Qt.ItemIsAutoTristate | Qt.ItemIsUserCheckable
                )
            else:
                child.setIcon(0, QIcon(":/icons/images/icons/cil-file.png"))
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
            if checkable:
                UIFunctions.fill_tree_from_path(child, path)
                child.setCheckState(0, Qt.Checked)
                parent.addChild(child)
                child.setExpanded(True)
            else:
                if text in checklist:
                    UIFunctions.fill_tree_from_path(
                        child, path, checkable=checkable, checklist=checklist
                    )
                    parent.addChild(child)

        if os.path.isfile(startpath):
            return
        else:
            if startpath == originalpath:
                new_item(tree, os.path.basename(startpath), startpath)
            else:
                for element in os.listdir(startpath):
                    path_info = startpath + "/" + element
                    new_item(tree, os.path.basename(element), path_info)

    def update_bucket_tree(self):
        try:
            UIFunctions.refresh_tree(
                self.ui.browse_s3_bucket,
                djsciops_axon.list_files(
                    session=self.session,
                    s3_bucket=self.ui.s3_bucket.text(),
                    s3_prefix=self.ui.browse_s3_dir.text(),
                ),
                "dict",
            )
            djsciops_utils.log("Successfully Loaded Bucket", gui=self.ui)
        except Exception as e:
            djsciops_utils.log(f"Failed to load Bucket: {e}", gui=self.ui)

    def update_bucket_preview(self):
        self.ui.s3_bucket_dir.clear()
        self.ui.s3_dir.setText(
            self.ui.s3_dir.text() + "/"
            if self.ui.s3_dir.text()[-1] != "/"
            else self.ui.s3_dir.text()
        )
        child = QTreeWidgetItem([self.ui.s3_dir.text()])
        child.setIcon(0, QIcon(":/icons/images/icons/cil-folder.png"))

        checklist = []
        iterator = QTreeWidgetItemIterator(
            self.ui.local_dir_tree, QTreeWidgetItemIterator.Checked
        )
        while iterator.value():
            item = iterator.value()
            checklist.append(item.text(0))
            iterator += 1
        UIFunctions.fill_tree_from_path(
            child, self.ui.local_dir.text(), checkable=False, checklist=checklist
        )
        self.ui.s3_bucket_dir.invisibleRootItem().addChild(child)
        child.setExpanded(True)
        self.ui.s3_bucket_dir.sortItems(0, Qt.AscendingOrder)
