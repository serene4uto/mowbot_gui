
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QStackedWidget,
)

from PyQt5.QtCore import pyqtSignal, pyqtSlot

from .waypoints_set_display import WaypointsSetDisplay
from .waypoints_follow_display import WaypointsFollowDisplay
from .settings_display import SettingsDisplay


class MultiFuncDisplay(QWidget):
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        mfunc_grb = QGroupBox()
        mfunc_layout = QVBoxLayout()
        
        self.staked_widget = QStackedWidget()
        
        self.staked_widget.addWidget(WaypointsSetDisplay())
        self.staked_widget.addWidget(WaypointsFollowDisplay())
        self.staked_widget.addWidget(SettingsDisplay())
        
        mfunc_layout.addWidget(self.staked_widget)
        mfunc_grb.setLayout(mfunc_layout)
        layout.addWidget(mfunc_grb)
        self.setLayout(layout)
    
    
    @pyqtSlot()
    def on_set_wp_task_btn_clicked(self):
        self.staked_widget.setCurrentIndex(0)
        
        
    @pyqtSlot()
    def on_follow_wp_task_btn_clicked(self):
        self.staked_widget.setCurrentIndex(1)
        
    @pyqtSlot()
    def on_settings_btn_clicked(self):
        self.staked_widget.setCurrentIndex(2)
        
        
        
    
        
        