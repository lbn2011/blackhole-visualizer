import sys
import os
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QLabel
from PyQt5.QtCore import Qt, QTimer, QSize
from PyQt5.QtGui import QIcon, QPixmap

# 导入自定义模块
from modules.controls import ControlPanel
from modules.renderer import BlackHoleRenderer
from modules.monitor import MonitorPanel
from modules.simulation import BlackHoleSimulator

# 确保资源路径正确
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class BlackHoleVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 初始化窗口
        self.setWindowTitle("BlackHole Visualizer")
        self.setWindowIcon(QIcon(resource_path("assets/icons/blackhole.png")))
        self.setGeometry(100, 100, 1400, 800)
        
        # 应用样式表
        self.load_style_sheet()
        
        # 创建状态标签
        self.status_label = QLabel("黑洞模拟器启动...")
        self.statusBar().addWidget(self.status_label)
        self.statusBar().setStyleSheet("background: rgba(20, 22, 33, 200); color: #a0a0ff; border-top: 1px solid #404050;")
        
        # 创建黑洞模拟器核心
        self.simulator = BlackHoleSimulator()
        
        # 创建主布局
        main_widget = QWidget()
        main_widget.setObjectName("mainWidget")
        main_layout = QHBoxLayout(main_widget)
        
        # 左侧控制面板
        control_panel = ControlPanel(self.simulator, self)
        control_panel.setObjectName("controlPanel")
        control_panel.setFixedWidth(400)
        main_layout.addWidget(control_panel)
        
        # 右侧区域
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        
        # 顶部渲染窗口
        self.renderer = BlackHoleRenderer(self.simulator, self)
        right_layout.addWidget(self.renderer, 4)
        
        # 底部监控窗口
        monitor_panel = MonitorPanel(self.simulator, self)
        monitor_panel.setFixedHeight(300)
        right_layout.addWidget(monitor_panel)
        
        main_layout.addWidget(right_panel, 1)
        
        self.setCentralWidget(main_widget)
        
        # 状态计时器
        self.status_timer = QTimer(self)
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(1000)
        
        # 参数更新连接
        control_panel.parametersChanged.connect(self.simulator.set_params)
        control_panel.parametersChanged.connect(self.renderer.update_simulation)
        control_panel.parametersChanged.connect(monitor_panel.update_monitor)
    
    def load_style_sheet(self):
        """加载样式表"""
        try:
            with open(resource_path("style.qss"), "r") as f:
                style = f.read()
                self.setStyleSheet(style)
        except Exception as e:
            print(f"加载样式表失败: {str(e)}")
            # 应用基本样式
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background: #111122;
                    color: #ffffff;
                    font-family: 'Segoe UI', Arial, sans-serif;
                }
                QLabel {
                    color: #a0a0ff;
                }
            """)
    
    def update_status(self):
        """更新状态栏信息"""
        status = f"黑洞质量: {self.simulator.black_hole_mass:.1e} M☉ | 视界半径: {self.simulator.event_horizon_radius:.1f} km | 温度: {self.simulator.accretion_disk_temp:.1e} K"
        self.status_label.setText(status)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # 设置应用ID以实现Windows任务栏独立图标
    try:
        from ctypes import windll
        windll.shell32.SetCurrentProcessExplicitAppUserModelID("BlackHole.Visualizer.1.0")
    except ImportError:
        pass
    
    # 设置默认字体
    font = app.font()
    font.setPointSize(9)
    app.setFont(font)
    
    window = BlackHoleVisualizer()
    window.show()
    sys.exit(app.exec_())
