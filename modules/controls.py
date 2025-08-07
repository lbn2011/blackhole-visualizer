import numpy as np
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGroupBox, QGridLayout, 
                            QLabel, QSlider, QDoubleSpinBox, QPushButton,
                            QComboBox)
from PyQt5.QtCore import Qt, pyqtSignal

class ControlPanel(QWidget):
    parametersChanged = pyqtSignal(dict)
    
    def __init__(self, simulator, parent=None):
        super().__init__(parent)
        self.simulator = simulator
        self.setObjectName("controlPanel")
        
        # 初始化控件
        self.init_ui()
        self.update_controls()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # 黑洞参数组
        bh_group = QGroupBox("黑洞参数")
        bh_layout = QGridLayout(bh_group)
        
        # 黑洞质量
        bh_layout.addWidget(QLabel("黑洞质量 (M☉):"), 0, 0)
        self.mass_slider = QSlider(Qt.Horizontal)
        self.mass_slider.setRange(4, 10)  # 10^4 to 10^10 solar masses (log scale)
        self.mass_slider.valueChanged.connect(self.on_param_change)
        bh_layout.addWidget(self.mass_slider, 0, 1)
        self.mass_spin = QDoubleSpinBox()
        self.mass_spin.setRange(1e4, 1e10)
        self.mass_spin.setDecimals(1)
        self.mass_spin.setSingleStep(0.1)
        self.mass_spin.valueChanged.connect(self.on_param_change)
        bh_layout.addWidget(self.mass_spin, 0, 2)
        
        # 自旋参数
        bh_layout.addWidget(QLabel("自旋参数:"), 1, 0)
        self.spin_slider = QSlider(Qt.Horizontal)
        self.spin_slider.setRange(0, 99)
        self.spin_slider.valueChanged.connect(self.on_param_change)
        bh_layout.addWidget(self.spin_slider, 1, 1)
        self.spin_spin = QDoubleSpinBox()
        self.spin_spin.setRange(0.0, 0.99)
        self.spin_spin.setSingleStep(0.01)
        self.spin_spin.setDecimals(2)
        self.spin_spin.valueChanged.connect(self.on_param_change)
        bh_layout.addWidget(self.spin_spin, 1, 2)
        
        # 吸积率
        bh_layout.addWidget(QLabel("吸积率:"), 2, 0)
        self.accretion_slider = QSlider(Qt.Horizontal)
        self.accretion_slider.setRange(0, 100)
        self.accretion_slider.valueChanged.connect(self.on_param_change)
        bh_layout.addWidget(self.accretion_slider, 2, 1)
        self.accretion_spin = QDoubleSpinBox()
        self.accretion_spin.setRange(0.0, 1.0)
        self.accretion_spin.setSingleStep(0.01)
        self.accretion_spin.setDecimals(2)
        self.accretion_spin.valueChanged.connect(self.on_param_change)
        bh_layout.addWidget(self.accretion_spin, 2, 2)
        
        layout.addWidget(bh_group)
        
        # 吸积盘参数组
        disk_group = QGroupBox("吸积盘参数")
        disk_layout = QGridLayout(disk_group)
        
        # 内半径
        disk_layout.addWidget(QLabel("内半径 (R_s):"), 0, 0)
        self.inner_radius_slider = QSlider(Qt.Horizontal)
        self.inner_radius_slider.setRange(20, 500)  # 实际值 = value/100
        self.inner_radius_slider.valueChanged.connect(self.on_param_change)
        disk_layout.addWidget(self.inner_radius_slider, 0, 1)
        self.inner_radius_spin = QDoubleSpinBox()
        self.inner_radius_spin.setRange(1.0, 10.0)
        self.inner_radius_spin.setSingleStep(0.1)
        self.inner_radius_spin.setDecimals(1)
        self.inner_radius_spin.valueChanged.connect(self.on_param_change)
        disk_layout.addWidget(self.inner_radius_spin, 0, 2)
        
        # 外半径
        disk_layout.addWidget(QLabel("外半径 (R_s):"), 1, 0)
        self.outer_radius_slider = QSlider(Qt.Horizontal)
        self.outer_radius_slider.setRange(100, 2500)
        self.outer_radius_slider.valueChanged.connect(self.on_param_change)
        disk_layout.addWidget(self.outer_radius_slider, 1, 1)
        self.outer_radius_spin = QDoubleSpinBox()
        self.outer_radius_spin.setRange(5.0, 50.0)
        self.outer_radius_spin.setSingleStep(0.5)
        self.outer_radius_spin.setDecimals(1)
        self.outer_radius_spin.valueChanged.connect(self.on_param_change)
        disk_layout.addWidget(self.outer_radius_spin, 1, 2)
        
        # 温度
        disk_layout.addWidget(QLabel("温度 (K):"), 2, 0)
        self.temp_slider = QSlider(Qt.Horizontal)
        self.temp_slider.setRange(1, 8)  # 10^4 to 10^8 K (log scale)
        self.temp_slider.valueChanged.connect(self.on_param_change)
        disk_layout.addWidget(self.temp_slider, 2, 1)
        self.temp_spin = QDoubleSpinBox()
        self.temp_spin.setRange(1e4, 1e8)
        self.temp_spin.setSingleStep(0.1e4)
        self.temp_spin.setDecimals(0)
        self.temp_spin.valueChanged.connect(self.on_param_change)
        disk_layout.addWidget(self.temp_spin, 2, 2)
        
        # 湍流
        disk_layout.addWidget(QLabel("湍流强度:"), 3, 0)
        self.turbulence_slider = QSlider(Qt.Horizontal)
        self.turbulence_slider.setRange(0, 90)  # 0.0 to 0.9
        self.turbulence_slider.valueChanged.connect(self.on_param_change)
        disk_layout.addWidget(self.turbulence_slider, 3, 1)
        self.turbulence_spin = QDoubleSpinBox()
        self.turbulence_spin.setRange(0.0, 0.9)
        self.turbulence_spin.setSingleStep(0.1)
        self.turbulence_spin.setDecimals(2)
        self.turbulence_spin.valueChanged.connect(self.on_param_change)
        disk_layout.addWidget(self.turbulence_spin, 3, 2)
        
        layout.addWidget(disk_group)
        
        # 光线参数组
        light_group = QGroupBox("光线参数")
        light_layout = QGridLayout(light_group)
        
        # 光线弯曲
        light_layout.addWidget(QLabel("光线弯曲强度:"), 0, 0)
        self.bending_slider = QSlider(Qt.Horizontal)
        self.bending_slider.setRange(80, 99)  # 0.8 to 0.99
        self.bending_slider.setValue(95)
        self.bending_slider.valueChanged.connect(self.on_param_change)
        light_layout.addWidget(self.bending_slider, 0, 1)
        self.bending_spin = QDoubleSpinBox()
        self.bending_spin.setRange(0.8, 0.99)
        self.bending_spin.setSingleStep(0.01)
        self.bending_spin.setDecimals(2)
        self.bending_spin.valueChanged.connect(self.on_param_change)
        light_layout.addWidget(self.bending_spin, 0, 2)
        
        # 多普勒效应
        light_layout.addWidget(QLabel("多普勒强度:"), 1, 0)
        self.doppler_slider = QSlider(Qt.Horizontal)
        self.doppler_slider.setRange(0, 100)
        self.doppler_slider.valueChanged.connect(self.on_param_change)
        light_layout.addWidget(self.doppler_slider, 1, 1)
        self.doppler_spin = QDoubleSpinBox()
        self.doppler_spin.setRange(0.0, 1.0)
        self.doppler_spin.setSingleStep(0.01)
        self.doppler_spin.setDecimals(2)
        self.doppler_spin.valueChanged.connect(self.on_param_change)
        light_layout.addWidget(self.doppler_spin, 1, 2)
        
        layout.addWidget(light_group)
        
        # 预设按钮
        self.presets_combo = QComboBox()
        self.presets_combo.addItems(["银河系中心", "M87中心", "天鹅座-X1", "自定义"])
        self.presets_combo.currentIndexChanged.connect(self.apply_preset)
        layout.addWidget(self.presets_combo)
        
        # 重置按钮
        self.reset_btn = QPushButton("重置参数")
        self.reset_btn.clicked.connect(self.reset_parameters)
        layout.addWidget(self.reset_btn)
        
        layout.addStretch(1)
    
    def update_controls(self):
        """用当前模拟参数更新控件"""
        # 仅更新控件但不触发信号
        self.blockSignals(True)
        
        # 更新黑洞参数
        mass = self.simulator.black_hole_mass
        mass_log = log10(mass)
        self.mass_slider.setValue(int((mass_log - 4) * 100 / (10-4)))
        self.mass_spin.setValue(mass)
        
        self.spin_slider.setValue(int(self.simulator.spin * 100))
        self.spin_spin.setValue(self.simulator.spin)
        
        self.accretion_slider.setValue(int(self.simulator.accretion_rate * 100))
        self.accretion_spin.setValue(self.simulator.accretion_rate)
        
        # 更新吸积盘参数
        self.inner_radius_slider.setValue(int(self.simulator.accretion_disk_inner_radius * 100))
        self.inner_radius_spin.setValue(self.simulator.accretion_disk_inner_radius)
        
        self.outer_radius_slider.setValue(int(self.simulator.accretion_disk_outer_radius * 50))
        self.outer_radius_spin.setValue(self.simulator.accretion_disk_outer_radius)
        
        temp_log = log10(self.simulator.accretion_disk_temp) - 4
        self.temp_slider.setValue(int(temp_log * 100))
        self.temp_spin.setValue(self.simulator.accretion_disk_temp)
        
        self.turbulence_slider.setValue(int(self.simulator.accretion_disk_turbulence * 100))
        self.turbulence_spin.setValue(self.simulator.accretion_disk_turbulence)
        
        # 更新光线参数
        self.bending_slider.setValue(int(self.simulator.light_bending_strength * 100))
        self.bending_spin.setValue(self.simulator.light_bending_strength)
        
        self.doppler_slider.setValue(int(self.simulator.doppler_factor * 100))
        self.doppler_spin.setValue(self.simulator.doppler_factor)
        
        self.blockSignals(False)
    
    def on_param_change(self):
        """当任何参数变化时发送新的参数设置"""
        params = {
            'mass': self.mass_spin.value(),
            'spin': self.spin_spin.value(),
            'accretion_rate': self.accretion_spin.value(),
            'disk_inner_radius': self.inner_radius_spin.value(),
            'disk_outer_radius': self.outer_radius_spin.value(),
            'disk_temp': self.temp_spin.value(),
            'disk_turbulence': self.turbulence_spin.value(),
            'light_bending': self.bending_spin.value(),
            'doppler_effect': self.doppler_spin.value()
        }
        self.parametersChanged.emit(params)
    
    def apply_preset(self, index):
        """应用的预设参数"""
        presets = {
            0: {  # 银河系中心 - Sagittarius A*
                'mass': 4.3e6,
                'spin': 0.65,
                'accretion_rate': 0.005,
                'disk_inner_radius': 3.0,
                'disk_outer_radius': 30.0,
                'disk_temp': 1e6,
                'disk_turbulence': 0.15,
                'light_bending': 0.92,
                'doppler_effect': 0.6
            },
            1: {  # M87中心黑洞
                'mass': 6.5e9,
                'spin': 0.90,
                'accretion_rate': 0.08,
                'disk_inner_radius': 5.0,
                'disk_outer_radius': 40.0,
                'disk_temp': 5e6,
                'disk_turbulence': 0.25,
                'light_bending': 0.97,
                'doppler_effect': 0.75
            },
            2: {  # 天鹅座-X1
                'mass': 15.0,
                'spin': 0.85,
                'accretion_rate': 0.2,
                'disk_inner_radius': 2.5,
                'disk_outer_radius': 15.0,
                'disk_temp': 3e6,
                'disk_turbulence': 0.20,
                'light_bending': 0.93,
                'doppler_effect': 0.7
            }
        }
        
        if index != 3:  # 3是"自定义"
            self.apply_parameters(presets[index])
    
    def apply_parameters(self, params):
        """应用一组参数并更新UI"""
        self.blockSignals(True)
        
        # 设置UI控件
        self.mass_spin.setValue(params['mass'])
        self.spin_spin.setValue(params['spin'])
        self.accretion_spin.setValue(params['accretion_rate'])
        self.inner_radius_spin.setValue(params['disk_inner_radius'])
        self.outer_radius_spin.setValue(params['disk_outer_radius'])
        self.temp_spin.setValue(params['disk_temp'])
        self.turbulence_spin.setValue(params['disk_turbulence'])
        self.bending_spin.setValue(params['light_bending'])
        self.doppler_spin.setValue(params['doppler_effect'])
        
        self.blockSignals(False)
        
        # 触发参数变化
        self.parametersChanged.emit(params)
    
    def reset_parameters(self):
        """重置为初始参数"""
        params = {
            'mass': 4.3e6,
            'spin': 0.7,
            'accretion_rate': 0.01,
            'disk_inner_radius': 3.0,
            'disk_outer_radius': 20.0,
            'disk_temp': 1e6,
            'disk_turbulence': 0.15,
            'light_bending': 0.95,
            'doppler_effect': 0.65
        }
        self.apply_parameters(params)
        
        # 设置预设为"银河系中心"
        if self.presets_combo.currentIndex() != 0:
            self.presets_combo.setCurrentIndex(0)
