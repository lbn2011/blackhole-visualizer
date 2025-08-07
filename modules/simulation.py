import numpy as np
import math

class BlackHoleSimulator:
    def __init__(self):
        # 黑洞参数
        self.black_hole_mass = 4.3e6  # 太阳质量 (M☉) - 以银河系中心黑洞为例
        self.spin = 0.7              # 自旋参数 (0.0 - 0.99)
        self.accretion_rate = 0.01    # 吸积率 (0.0 - 1.0)
        
        # 吸积盘参数
        self.accretion_disk_inner_radius = 3.0  # 吸积盘内半径 (以视界半径为单位)
        self.accretion_disk_outer_radius = 20.0 # 吸积盘外半径 (以视界半径为单位)
        self.accretion_disk_temp = 1e6          # 吸积盘温度 (K)
        self.accretion_disk_turbulence = 0.15    # 吸积盘湍流强度
        
        # 光线参数
        self.light_bending_strength = 0.95       # 光线弯曲强度 (0.9 - 1.0)
        self.doppler_factor = 0.65               # 多普勒效应强度
        
        # 物理常数
        self.G = 6.67430e-11    # 万有引力常数 (m^3 kg^-1 s^-2)
        self.c = 299792458.0    # 光速 (m/s)
        self.M_sun = 1.989e30   # 太阳质量 (kg)
        
        # 计算属性 (只读)
        self._event_horizon_radius = None
        self._schwarzschild_radius = None
        self.update_params()
        
        # 用于监控的数据
        self.observation_data = []
        self.max_data_points = 500
    
    @property
    def event_horizon_radius(self):
        """计算事件视界半径 (km)"""
        if self._event_horizon_radius is None:
            self.update_params()
        return self._event_horizon_radius
    
    @property
    def schwarzschild_radius(self):
        """计算史瓦西半径 (km)"""
        if self._schwarzschild_radius is None:
            mass_kg = self.black_hole_mass * self.M_sun
            rs = (2 * self.G * mass_kg) / (self.c ** 2)
            self._schwarzschild_radius = rs / 1000.0  # 转换为公里
        return self._schwarzschild_radius
    
    def set_params(self, params):
        """更新模拟参数"""
        # 更新主参数
        self.black_hole_mass = params.get('mass', self.black_hole_mass)
        self.spin = params.get('spin', self.spin)
        self.accretion_rate = params.get('accretion_rate', self.accretion_rate)
        
        # 更新吸积盘参数
        self.accretion_disk_inner_radius = params.get('disk_inner_radius', self.accretion_disk_inner_radius)
        self.accretion_disk_outer_radius = params.get('disk_outer_radius', self.accretion_disk_outer_radius)
        self.accretion_disk_temp = params.get('disk_temp', self.accretion_disk_temp)
        self.accretion_disk_turbulence = params.get('disk_turbulence', self.accretion_disk_turbulence)
        
        # 更新光线参数
        self.light_bending_strength = params.get('light_bending', self.light_bending_strength)
        self.doppler_factor = params.get('doppler_effect', self.doppler_factor)
        
        self.update_params()
    
    def update_params(self):
        """更新计算得到的属性值"""
        mass_kg = self.black_hole_mass * self.M_sun
        rs = self.schwarzschild_radius * 1000.0  # 转换为米
        
        # Kerr黑洞的事件视界半径
        r_plus = rs * (1 + math.sqrt(1 - self.spin**2))
        self._event_horizon_radius = r_plus / 1000.0  # 转换为公里
        
        # 更新吸积盘物理属性
        # 吸积盘内半径 (米)
        inner_r = self.accretion_disk_inner_radius * (rs * 1000)
        outer_r = self.accretion_disk_outer_radius * (rs * 1000)
        
        # 清空缓存参数
        self._event_horizon_radius = None
        self._schwarzschild_radius = None
    
    def simulate_gravitational_lens(self, x, y):
        """
        模拟引力透镜效应
        :param x: 观察平面的x坐标
        :param y: 观察平面的y坐标
        :return: (lensed_x, lensed_y, intensity, color)
        """
        # 计算到黑洞中心的距离
        r = math.sqrt(x*x + y*y)
        
        # 避免除以零
        if r < 1e-10:
            r = 1e-10
            
        # 基本光线偏折
        deflection_angle = (self.light_bending_strength * 2 * self.schwarzschild_radius) / r
        
        # 计算偏折后的坐标
        theta = math.atan2(y, x)
        lensed_x = x - deflection_angle * math.cos(theta) * r
        lensed_y = y - deflection_angle * math.sin(theta) * r
        
        # 计算强度 (随距离递减)
        intensity = 1.0 - math.atan(r / self.accretion_disk_inner_radius) * 0.5
        
        return lensed_x, lensed_y, intensity
    
    def sample_accretion_disk(self, x, y):
        """在特定点采样吸积盘"""
        r = math.sqrt(x*x + y*y)
        
        # 检查是否在吸积盘范围内
        if r < self.accretion_disk_inner_radius or r > self.accretion_disk_outer_radius:
            return 0.0, (0, 0, 0)
        
        # 温度分布 (随半径递减)
        temp = self.accretion_disk_temp * (self.accretion_disk_inner_radius / r) ** 0.75
        
        # 辐射强度 (普朗克辐射定律)
        intensity = (temp / self.accretion_disk_temp) ** 4
        
        # 多普勒效应 (假设吸积盘旋转)
        # 靠近黑洞的吸积盘旋转更快
        angular_velocity = math.sqrt(self.G * self.black_hole_mass * self.M_sun) / (r * 1000)
        doppler_shift = 1.0 + self.doppler_factor * angular_velocity / self.c * math.sin(math.atan2(y, x))
        
        # 温度颜色映射
        # 蓝色=热，红色=较冷
        if temp > 1e6:
            # 高温区域 (蓝色)
            blue_val = min(255, int(255 * (temp / self.accretion_disk_temp)))
            green_val = min(255, int(200 * (temp / self.accretion_disk_temp * 0.6)))
            red_val = min(255, int(120 * (temp / self.accretion_disk_temp * 0.4)))
        elif temp > 3e5:
            # 中温区域 (蓝绿色)
            blue_val = min(255, int(200 * (temp / self.accretion_disk_temp)))
            green_val = min(255, int(150 * (temp / self.accretion_disk_temp * 1.2)))
            red_val = min(255, int(80 * (temp / self.accretion_disk_temp * 0.8)))
        else:
            # 低温区域 (红色)
            blue_val = min(255, int(80 * (temp / (0.3 * self.accretion_disk_temp))))
            green_val = min(255, int(120 * (temp / (0.5 * self.accretion_disk_temp))))
            red_val = min(255, int(220 * (temp / (0.5 * self.accretion_disk_temp))))
        
        # 应用多普勒效应
        red_val = min(255, int(red_val * doppler_shift))
        blue_val = max(0, int(blue_val * (2.0 - doppler_shift)))
        
        return intensity, (red_val, green_val, blue_val)
    
    def update_monitoring_data(self):
        """更新用于监控的数据"""
        self.observation_data.append({
            'radius': self.schwarzschild_radius,
            'mass': self.black_hole_mass,
            'spin': self.spin,
            'accretion_rate': self.accretion_rate,
            'disk_temp': self.accretion_disk_temp
        })
        
        # 限制数据点数量
        if len(self.observation_data) > self.max_data_points:
            self.observation_data.pop(0)
