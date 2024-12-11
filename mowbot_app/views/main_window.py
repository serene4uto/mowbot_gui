from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QStatusBar,
)

from mowbot_app.app_info import __appname__, __appdescription__


class MainWindow(QMainWindow):
    """Main window class for the application"""
    
    def __init__(
        self,
        app=None,
        config=None,
    ):
        super().__init__()
        
        self.app = app
        self.config = config

        # Set the window title
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle(__appname__)
        
        # Set the central widget and the main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)



        # Set the main layout
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        status_bar = QStatusBar()
        status_bar.showMessage(f"{__appname__} - {__appdescription__}")
        self.setStatusBar(status_bar)