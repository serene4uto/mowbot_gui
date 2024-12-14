from PyQt5.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QListView,
    QGroupBox,
    QComboBox,
)

from .map_view import MapView
from .process_button import ProcessButton


class WaypointsSetOptionBar(QWidget):
    def __init__(self, config):
        super().__init__()
        
        layout = QHBoxLayout()

        self.start_btn = ProcessButton(
            start_script=config['script_wp_set_start'],
            stop_script=config['script_wp_set_stop'],
        )
        self.start_btn.setText('Start')
        self.start_btn.setFixedWidth(100)
        self.start_btn.setFixedHeight(80)
        layout.addWidget(self.start_btn)
        layout.setSpacing(10)

        self.list_view = QListView()
        self.list_view.setFixedWidth(200)
        self.list_view.setFixedHeight(80)
        layout.addWidget(self.list_view)
        layout.setSpacing(10)
        
        self.log_btn = QPushButton('Log')
        self.log_btn.setFixedWidth(100)
        self.log_btn.setFixedHeight(80)
        layout.addWidget(self.log_btn)
        layout.setSpacing(10)

        # self.genlayout = QVBoxLayout()
        # self.res_lbl = QLabel('Resolution:')
        # self.genlayout.addWidget(self.res_lbl)

        #TODO: auto generate resolution options

        layout.addStretch(1)

        self.save_btn = QPushButton('Save')
        self.save_btn.setFixedWidth(100)
        self.save_btn.setFixedHeight(80)
        layout.addWidget(self.save_btn)
        
        self.setLayout(layout)
        self.setFixedHeight(100)

class WaypointsSetDisplay(QWidget):
    def __init__(self, config):
        super().__init__()

        self.config = config
        
        layout = QVBoxLayout()
        
        # add option bar
        option_bar = WaypointsSetOptionBar(config=self.config)
        layout.addWidget(option_bar)
        layout.setSpacing(10)
        
        # add map view
        map_view = MapView()
        layout.addWidget(map_view)
        
        
        self.setLayout(layout)
        
        
        