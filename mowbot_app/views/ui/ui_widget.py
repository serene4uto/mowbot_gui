from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
)

from PyQt5.QtCore import pyqtSignal, pyqtSlot

from mowbot_app.views.ui.widgets import StatusBar, MenuBox, MultiFuncDisplay


class UIWidget(QWidget):
    def __init__(
        self,
        config=None,
    ):
        super().__init__()
        
        self.config = config
        
        # Create a main vertical layout
        layout = QVBoxLayout()
        
        # Add a status bar at the top
        self.status_bar = StatusBar()
        layout.addWidget(self.status_bar)
        
        # Create a horizontal layout
        self.hlayout = QHBoxLayout()
        
        # Create a left vertical layout that expands fully
        self.hleft_layout = QVBoxLayout()
        
        # Add the menu box to the left layout
        self.menu_box = MenuBox()
        self.hleft_layout.addWidget(self.menu_box)
        
        # Ensure the left layout takes all vertical space
        self.hlayout.addLayout(self.hleft_layout, 1)  # Stretch factor 1 for left layout
        
        self.mfunc_display = MultiFuncDisplay()
        self.hlayout.addWidget(self.mfunc_display)
        
        # self.hlayout.addStretch(1) 
        
        # Add the horizontal layout to the main vertical layout
        layout.addLayout(self.hlayout, 1)  # Stretch factor 1 for the hlayout
        
        self.setLayout(layout)
        
        # Connect signals
        self.menu_box.settings_btn_clicked_signal.connect(
            self.mfunc_display.on_settings_btn_clicked
        )
        self.menu_box.set_wp_task_btn_clicked_signal.connect(
            self.mfunc_display.on_set_wp_task_btn_clicked
        )
        self.menu_box.follow_wp_task_btn_clicked_signal.connect(
            self.mfunc_display.on_follow_wp_task_btn_clicked
        )