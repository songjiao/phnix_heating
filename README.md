# Phnix Heating System Integration for Home Assistant

这是一个用于Home Assistant的Phnix地暖主机集成插件，支持控制地暖主机的开关机、模式切换、温度设定，以及监控各种运行参数。

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![maintainer](https://img.shields.io/badge/maintainer-%40songjiao-blue.svg)](https://github.com/songjiao)

## 功能特性

### 控制功能
- **开关机控制**: 支持远程开关机
- **模式切换**: 支持制冷和制热两种模式
- **温度设定**: 支持制冷温度(5-25℃)和制热温度(25-60℃)设定

### 监控功能
- **温度监控**: 进水温度、出水温度、室内温度、环境温度、盘管温度、回气温度、排气温度、防冻温度、热水温度、增焓进温度、增焓出温度
- **压力监控**: 回气压力、排气压力
- **流量监控**: 水流量
- **电气参数**: AC输入电压/电流、压缩机相电流、DC母线电压、IPM温度、电表输入功率、热泵能力、COP
- **运行参数**: 压缩机频率、风机转速、电子膨胀阀开度、压缩机运行时间、电表电量
- **通信状态**: DTU信号强度、DTU在线标志、多机组通信状态
- **输出状态**: 压缩机、水泵、风机、阀门等各种输出状态
- **安全开关**: 高压开关、低压开关、水流开关、干烧开关、应急开关等

## 安装方法

### 方法1: HACS安装（推荐）

1. 确保已安装[HACS](https://hacs.xyz/)
2. 在HACS中添加自定义仓库：
   - 仓库: `songjiao/phnix_heating`
   - 类别: `Integration`
3. 搜索"Phnix Heating System"并安装
4. 重启Home Assistant
5. 在配置 -> 设备与服务中添加集成

### 方法2: 手动安装

1. 下载插件文件到`config/custom_components/phnix_heating/`目录
2. 重启Home Assistant
3. 在配置 -> 设备与服务中添加集成

## 配置说明

### 必需参数
- **设备名称**: 为您的设备起一个名称
- **设备编码**: 您的Phnix设备编码（如：I012406020019）
- **认证令牌**: 从Phnix云平台获取的x-token

### 可选参数
- **协议ID**: 默认为1679324789907087360，通常不需要修改
- **扫描间隔**: 状态更新频率，默认30秒

### 获取认证令牌

1. 登录[Phnix云平台](http://yun.phnixsmart.com/)
2. 打开浏览器开发者工具（F12）
3. 在Network标签页中找到API请求
4. 复制请求头中的`x-token`值

## 使用方法

### 基本控制
1. 在Home Assistant的仪表板中添加Climate实体
2. 使用开关机按钮控制设备
3. 使用模式选择器切换制冷/制热模式
4. 使用温度滑块设定目标温度

### 监控面板
1. 添加各种传感器到仪表板
2. 创建自动化规则基于传感器状态
3. 设置告警通知

## 实体说明

### Climate实体
- **phnix_heating**: 主要的温控实体，集成开关机、模式、温度控制

### Sensor实体
- **温度传感器**: 各种温度监控
- **压力传感器**: 系统压力监控
- **电气传感器**: 电压、电流、功率监控
- **运行传感器**: 频率、转速、运行时间等

### Binary Sensor实体
- **状态传感器**: 开关机状态、运行模式等
- **输出传感器**: 各种设备输出状态
- **安全传感器**: 安全开关状态

## 自动化示例

### 温度控制自动化
```yaml
automation:
  - alias: "自动制热控制"
    trigger:
      platform: numeric_state
      entity_id: sensor.indoor_temp
      below: 18
    action:
      - service: climate.set_hvac_mode
        target:
          entity_id: climate.phnix_heating
        data:
          hvac_mode: heat
      - service: climate.set_temperature
        target:
          entity_id: climate.phnix_heating
        data:
          temperature: 22
```

### 安全告警自动化
```yaml
automation:
  - alias: "高压告警"
    trigger:
      platform: state
      entity_id: binary_sensor.high_pressure_switch
      to: "on"
    action:
      - service: notify.mobile_app
        data:
          message: "地暖主机高压告警！"
```

### 节能模式自动化
```yaml
automation:
  - alias: "夜间节能模式"
    trigger:
      platform: time
      at: "22:00:00"
    action:
      - service: climate.set_temperature
        target:
          entity_id: climate.phnix_heating
        data:
          temperature: 18
```

## 故障排除

### 常见问题
1. **连接失败**: 检查设备编码和令牌是否正确
2. **状态不更新**: 检查网络连接和扫描间隔设置
3. **控制无响应**: 确认设备在线且令牌有效

### 日志查看
在Home Assistant的开发者工具中查看日志：
```yaml
logger:
  custom_components.phnix_heating: debug
```

### 调试步骤
1. 检查设备是否在线
2. 验证API令牌是否过期
3. 确认网络连接正常
4. 查看Home Assistant日志

## 技术支持

如有问题，请：
1. 查看Home Assistant日志
2. 检查设备网络连接
3. 验证API令牌有效性
4. 在[GitHub Issues](https://github.com/songjiao/phnix_heating/issues)中报告问题

## 贡献

欢迎提交Issue和Pull Request来改进这个集成！

## 更新日志

### v1.0.0
- 初始版本发布
- 支持基本的开关机、模式、温度控制
- 支持全面的状态监控
- 支持中文界面
- 支持HACS安装

## 许可证

MIT License

## 致谢

感谢Phnix提供的API接口，让这个集成成为可能。 