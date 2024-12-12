from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
)

from  .map_view import MapView



class WaypointsSetOptionBar(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QHBoxLayout()
        
        self.setLayout(layout)
        
        self.setFixedHeight(100)

class WaypointsSetDisplay(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        
        # add option bar
        option_bar = WaypointsSetOptionBar()
        layout.addWidget(option_bar)
        layout.setSpacing(10)
        
        # add map view
        map_view = MapView()
        layout.addWidget(map_view)
        
        
        self.setLayout(layout)
        
        
        