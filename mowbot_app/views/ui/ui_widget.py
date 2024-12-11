from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout, 
    QHBoxLayout, 
)

from mowbot_app.views.ui.widgets.status_bar import StatusBar




class UIWidget(QWidget):
    def __init__(
        self,
        config=None,
    ):
        super().__init__()
        
        self.config = config
        
        # create a layout
        layout = QVBoxLayout()
        
        self.status_bar = StatusBar()
        layout.addWidget(self.status_bar)
        layout.addStretch(1)
        
        
        self.setLayout(layout)
        
        