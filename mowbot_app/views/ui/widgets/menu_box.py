from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QGroupBox,
)

from PyQt5.QtCore import pyqtSignal, pyqtSlot

class MenuBox(QWidget):
    
    settings_btn_clicked_signal = pyqtSignal()
    set_wp_task_btn_clicked_signal = pyqtSignal()
    follow_wp_task_btn_clicked_signal = pyqtSignal()
    bringup_btn_clicked_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        layout = QVBoxLayout()
        menu_grb = QGroupBox('Menu')
        menu_grb.setStyleSheet("QGroupBox { font-size: 16px; font-weight: bold; }")
        menu_layout = QVBoxLayout()
        
        self.settings_btn = QPushButton('Settings')
        self.settings_btn.setFixedHeight(50)
        menu_layout.addWidget(self.settings_btn)
        
        task_menu_grb = QGroupBox('Tasks')
        task_menu_grb.setStyleSheet("QGroupBox { font-size: 14px; font-weight: bold; }")
        task_menu_layout = QVBoxLayout()
        self.set_wp_task_btn = QPushButton('Set Waypoints')
        self.set_wp_task_btn.setFixedHeight(50)
        task_menu_layout.addWidget(self.set_wp_task_btn)
        task_menu_layout.setSpacing(10)
        self.follow_wp_task_btn = QPushButton('Follow Waypoints')
        self.follow_wp_task_btn.setFixedHeight(50)
        task_menu_layout.addWidget(self.follow_wp_task_btn)
        task_menu_layout.setSpacing(10)
        task_menu_layout.addStretch(1)
        
        task_menu_grb.setLayout(task_menu_layout)
        
        menu_layout.addWidget(task_menu_grb)
        
        menu_grb.setLayout(menu_layout)
        layout.addWidget(menu_grb)
        
        self.bringup_btn = QPushButton('Start')
        self.bringup_btn.setStyleSheet("font-size: 20px; font-weight: bold;")
        self.bringup_btn.setFixedHeight(100)
        layout.addWidget(self.bringup_btn)
        self.setLayout(layout)
        self.setFixedWidth(300)
        
        self.settings_btn.clicked.connect(self.on_settings_btn_clicked)
        self.set_wp_task_btn.clicked.connect(self.on_set_wp_task_btn_clicked)
        self.follow_wp_task_btn.clicked.connect(self.on_follow_wp_task_btn_clicked)
        
    
    def on_settings_btn_clicked(self):
        self.settings_btn_clicked_signal.emit()
        
        
    def on_set_wp_task_btn_clicked(self):
        self.set_wp_task_btn_clicked_signal.emit()
        
    
    def on_follow_wp_task_btn_clicked(self):
        self.follow_wp_task_btn_clicked_signal.emit()
        
    
