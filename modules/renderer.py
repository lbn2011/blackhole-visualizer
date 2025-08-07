import numpy as np
from math import cos, sin, pi, exp, log10, sqrt
from PyQt5.QtWidgets import QOpenGLWidget, QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush
from PyQt5.QtCore import Qt, QTimer

class BlackHoleRenderer(QWidget):
    def __init__(self, simulator, parent=None):
        super().__init__(parent)
        self.simulator = simulator
        self.setMinimumSize(600, 400)
        self.setObjectName("RenderWindow")
        
        # 渲染参数
        self.resolution = 512
        self.render_buffer = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_render)
        self.timer.start(100)  # 10 FPS
        
        # 视角参数
        self.view_angle = 45.0  # 视角角度（度）
        self.zoom = 1.0
        
        # 初始化渲染缓冲区
        self.update_render()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 绘制背景
        bg_color = QColor(10, 12, 25)
        painter.fillRect(self.rect(), bg_color)
        
        # 绘制背景星空
        self.draw_starfield(painter)
        
        # 绘制黑洞渲染
        if self.render_buffer is not None:
            # 居中绘制
            w, h = self.width(), self.height()
            size = min(w, h) * 0.9
            x_offset = (w - size) / 2
            y_offset = (h - size) * 0.6
            
            # 抗锯齿缩放
            painter.save()
            painter.translate(x_offset, y_offset)
            painter.scale(size / self.resolution, size / self.resolution)
            
            # 绘制每个像素
            for y in range(self.resolution):
                for x in range(self.resolution):
                    r, g, b = self.render_buffer[y][x]
                    if r > 0 or g > 0 or b > 0:
                        painter.setPen(QColor(r, g, b))
                        painter.drawPoint(x, y)
            
            painter.restore()
        
        # 绘制信息文本
        info_text = "黑洞渲染   |   视界半径: {:.1f} km   |   观测角度: {:.0f}°".format(
            self.simulator.schwarzschild_radius, self.view_angle
        )
        painter.setPen(QColor(200, 200, 240))
        painter.setFont(self.font())
        painter.drawText(15, self.height() - 15, info_text)
    
    def draw_starfield(self, painter):
        """绘制背景星空"""
        w, h = self.width(), self.height()
        
        painter.setPen(Qt.NoPen)
        
        # 不同亮度的星星
        for _ in range(200):
            x = np.random.randint(0, w)
            y = np.random.randint(0, h)
            size = np.random.uniform(0.5, 2.0)
            brightness = np.random.randint(200, 255)
            
            # 按黑洞位置减弱亮度
            dist = sqrt((x - w/2)**2 + (y - h*0.6)**2)
            if dist < w/3 * 1.5:
                brightness = max(30, int(brightness * (dist / (w/3 * 1.5))**0.5))
            
            star_color = QColor(brightness, brightness, brightness)
            offset = max(0.5, size * 0.5)
            
            # 绘制星星
            painter.setBrush(QBrush(star_color))
            painter.drawEllipse(x - offset, y - offset, size, size)
            
            # 随机辉光
            if np.random.random() > 0.9:
                painter.setBrush(Qt.NoBrush)
                painter.setPen(QColor(brightness, brightness, min(255, brightness+50), 80))
                painter.drawEllipse(x - size*2, y - size*2, size*4, size*4)
    
    def update_simulation(self):
        """当参数变化时更新渲染"""
        self.generate_render()
        self.update()
    
    def update_render(self):
        """更新渲染 - 动画旋转"""
        self.view_angle = (self.view_angle + 0.5) % 360
        self.generate_render()
        self.update()
    
    def generate_render(self):
        """生成黑洞渲染图像（简化版）"""
        size = self.resolution
        self.render_buffer = np.zeros((size, size, 3), dtype=np.uint8)
        
        # 旋转角度（弧度）
        angle = np.radians(self.view_angle)
        view_cos = cos(angle)
        view_sin = sin(angle)
        
        # 渲染范围（以事件视界半径为单位）
        schwarz_radius = self.simulator.schwarzschild_radius
        render_radius = self.simulator.accretion_disk_outer_radius * schwarz_radius * self.zoom
        
        # 渲染每个像素
        for y in range(size):
            sy = 2.0 * (y - size/2) / size * render_radius
            for x in range(size):
                sx = 2.0 * (x - size/2) / size * render_radius
                
                # 应用旋转（围绕y轴）
                rx = sx * view_cos
                rz = sx * view_sin  # 旋转轴
                ry = sy
                
                # 模拟引力透镜效应
                lensed_x, lensed_y, intensity = self.simulator.simulate_gravitational_lens(rx, ry)
                
                # 在偏折位置采样吸积盘
                disk_intensity, disk_color = self.simulator.sample_accretion_disk(lensed_x, lensed_y)
                
                # 如果强度大于0，则渲染吸积盘
                if disk_intensity > 0:
                    # 添加旋转效果
                    ri = min(1.0, disk_intensity * intensity)
                    r = min(255, int(disk_color[0] * ri))
                    g = min(255, int(disk_color[1] * ri))
                    b = min(255, int(disk_color[2] * ri))
                else:
                    r, g, b = 0, 0, 0
                
                # 保存到缓冲区
                self.render_buffer[y, x] = np.array([r, g, b])
        
        return self.render_buffer
