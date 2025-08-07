import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy
from PyQt5.QtCore import Qt

class TitleLabel(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setMinimumHeight(30)
        self.setObjectName("PanelTitle")

class MonitorPanel(QWidget):
    def __init__(self, simulator, parent=None):
        super().__init__(parent)
        self.simulator = simulator
        self.setObjectName("monitorPanel")
        
        # 初始化界面
        self.init_ui()
        
        # 更新计时器
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.update_monitor)
        self.timer.start(500)  # 每500ms更新一次
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # 标题
        layout.addWidget(TitleLabel("黑洞实时监控"))
        
        # 创建图表
        self.init_charts(layout)
        
        # 状态信息
        self.info_layout = QHBoxLayout()
        layout.addLayout(self.info_layout)
        
        self.mass_label = QLabel()
        self.mass_label.setAlignment(Qt.AlignCenter)
        self.info_layout.addWidget(self.mass_label)
        
        self.spin_label = QLabel()
        self.spin_label.setAlignment(Qt.AlignCenter)
        self.info_layout.addWidget(self.spin_label)
        
        self.disk_label = QLabel()
        self.disk_label.setAlignment(Qt.AlignCenter)
        self.info_layout.addWidget(self.disk_label)
        
        # 设置样式
        for label in [self.mass_label, self.spin_label, self.disk_label]:
            label.setObjectName("valueLabel")
    
    def init_charts(self, parent_layout):
        # 创建图表容器
        chart_layout = QHBoxLayout()
        
        # 温度图表
        self.temp_plot = pg.PlotWidget(title="吸积盘温度分布")
        self.temp_plot.setBackground('w')
        self.temp_plot.setMinimumHeight(200)
        self.temp_plot.showGrid(x=True, y=True, alpha=0.3)
        
        # 引力透镜图表
        self.lens_plot = pg.PlotWidget(title="引力透镜效应强度")
        self.lens_plot.setBackground('w')
        self.lens_plot.setMinimumHeight(200)
        self.lens_plot.showGrid(x=True, y=True, alpha=0.3)
        
        chart_layout.addWidget(self.temp_plot)
        chart_layout.addWidget(self.lens_plot)
        parent_layout.addLayout(chart_layout, 2)
        
        # 设置图表样式
        for plot in [self.temp_plot, self.lens_plot]:
            plot.setAntialiasing(True)
            plot.getPlotItem().getAxis('left').setTextPen('k')
            plot.getPlotItem().getAxis('bottom').setTextPen('k')
            plot.getPlotItem().setTitle(color='k', size='12pt')
    
    def update_monitor(self):
        """更新监控数据"""
        self.simulator.update_monitoring_data()
        
        # 更新状态信息
        self.mass_label.setText(f"黑洞质量: \n{self.simulator.black_hole_mass:.1e} M☉")
        self.spin_label.setText(f"自旋参数: \n{self.simulator.spin:.2f}")
        self.disk_label.setText(f"吸积盘温度: \n{self.simulator.accretion_disk_temp:.1e} K")
        
        # 更新温度分布图表
        self.update_temp_plot()
        
        # 更新引力透镜图表
        self.update_lens_plot()
    
    def update_temp_plot(self):
        """更新温度分布图表"""
        self.temp_plot.clear()
        
        # 创建半径范围
        r = np.linspace(self.simulator.accretion_disk_inner_radius,
                        self.simulator.accretion_disk_outer_radius,
                        100)
        
        # 计算温度分布
        temp = self.simulator.accretion_disk_temp * np.power(
            self.simulator.accretion_disk_inner_radius / r, 0.75
        )
        
        # 绘制温度曲线
        curve = self.temp_plot.plot(r, temp, pen=pg.mkPen(color='#e74c3c', width=3))
        
        # 设置轴标签
        self.temp_plot.setLabel('left', "温度 (K)", color='#333')
        self.temp_plot.setLabel('bottom', "半径 (事件视界半径倍数)", color='#333')
        
        # 添加填充
        temp_fill = pg.FillBetweenItem(
            curve, 
            pg.PlotCurveItem(y=np.zeros_like(temp)), 
            brush=pg.mkBrush('#e74c3c50')
        )
        self.temp_plot.addItem(temp_fill)
        
        # 设置范围
        self.temp_plot.setYRange(0.1e6, self.simulator.accretion_disk_temp * 1.2)
        self.temp_plot.setLogMode(y=True)
    
    def update_lens_plot(self):
        """更新引力透镜效应强度图表"""
        self.lens_plot.clear()
        
        # 创建距离范围 (从1倍到100倍事件视界半径)
        r = np.linspace(self.simulator.accretion_disk_inner_radius * 0.5,
                        self.simulator.accretion_disk_outer_radius * 5,
                        200)
        
        # 计算光线偏折角度 (简化模型)
        bending_strength = (2 * self.simulator.schwarzschild_radius * 1000)  # 转换为米
        deflection_angle = np.degrees(bending_strength / (r * self.simulator.schwarzschild_radius * 1000))
        
        # 绘制引力透镜曲线
        curve = self.lens_plot.plot(r, deflection_angle, pen=pg.mkPen(color='#3498db', width=3))
        
        # 设置轴标签
        self.lens_plot.setLabel('left', "偏折角 (度)", color='#333')
        self.lens_plot.setLabel('bottom', "距离 (事件视界半径倍数)", color='#333')
        
        # 添加事件视界指示线
        hor_line = pg.InfiniteLine(pos=self.simulator.accretion_disk_inner_radius, angle=90, 
                                  pen=pg.mkPen('#e67e22', width=2, style=Qt.DashLine))
        self.lens_plot.addItem(hor_line)
        
        # 添加图例
        self.lens_plot.addItem(
            pg.TextItem("事件视界", color='#e67e22', anchor=(0,1)), 
            self.simulator.accretion_disk_inner_radius, 
            max(deflection_angle)
        )
