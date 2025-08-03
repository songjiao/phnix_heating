# Phnix Heating System Integration for Home Assistant

这是一个用于Home Assistant的Phnix地暖主机集成，支持通过Phnix智能云平台控制地暖主机并获取设备状态数据。

## 功能特性

- 🌡️ **温度控制**: 支持制冷和制热模式，可设置目标温度
- 🔌 **电源控制**: 支持开关机控制
- 📊 **状态监控**: 提供30+个传感器实体，监控各种设备参数
- 🔍 **状态检测**: 提供20+个二进制传感器，检测设备运行状态
- 🔐 **安全认证**: 支持用户名密码登录，自动token管理
- 🔄 **自动重连**: Token过期时自动重新登录

## 支持的设备

- Phnix地暖主机系列
- 支持Phnix智能云平台的设备

## 安装方法

### 方法一：通过HACS安装（推荐）

1. 确保已安装[HACS](https://hacs.xyz/)
2. 在HACS中添加自定义仓库：
   - 仓库：`https://github.com/songjiao/phnix_heating`
   - 类别：集成
3. 搜索"Phnix Heating System"并安装
4. 重启Home Assistant

### 方法二：手动安装

1. 下载此仓库
2. 将`custom_components/phnix_heating`文件夹复制到您的Home Assistant配置目录下的`custom_components/`文件夹中
3. 重启Home Assistant

## 配置

### 通过UI配置（推荐）

1. 在Home Assistant中，进入**设置** > **设备与服务** > **集成**
2. 点击**添加集成**
3. 搜索"Phnix Heating System"
4. 填写配置信息：
   - **用户名**: 您的Phnix账户用户名（通常是手机号）
   - **密码**: 您的Phnix账户密码
   - **设备编码**: 您的设备编码（如：I012406020019）
   - **设备名称**: 自定义设备名称（可选）

### 通过YAML配置

```yaml
# configuration.yaml
phnix_heating:
  username: "18601276103"
  password: "your_password"
  device_code: "I012406020019"
  name: "地暖主机"
```

## 实体说明

### Climate实体

- **地暖主机**: 主要的温控实体，支持开关机、模式切换和温度设置

### Sensor实体（30+个）

#### 温度传感器
- 进水温度
- 出水温度
- 室内温度
- 环境温度
- 盘管温度
- 回气温度
- 排气温度
- 防冻温度
- 热水温度
- 增焓进温度
- 增焓出温度

#### 压力传感器
- 回气压力
- 排气压力

#### 流量传感器
- 水流量

#### 电气参数传感器
- AC输入电压
- AC输入电流
- 压缩机相电流
- DC母线电压
- IPM温度
- 电表输入功率
- 热泵能力
- COP

#### 运行参数传感器
- 压缩机频率
- 风机1转速
- 风机2转速
- 电子膨胀阀开度
- 增焓电子膨胀阀开度
- 压缩机运行时间
- 电表电量

#### 通信状态传感器
- DTU信号强度
- DTU在线标志
- 多机组通信状态

### Binary Sensor实体（20+个）

#### 输出状态
- 压缩机输出
- 二次泵输出
- 高风输出
- 低风输出
- 四通阀输出
- 热水三通阀输出
- 水泵输出
- 电加热输出
- 喷淋阀输出
- 防冻加热带输出
- 系统1曲轴加热带输出
- 补水阀输出
- 报警输出
- 制冷水阀输出
- 制热水阀输出

#### 安全开关
- 高压开关
- 低压开关
- 水流开关
- 电加热干烧开
- 模式输入
- 应急开关

## 使用示例

### 自动化示例

#### 根据室内温度自动调节
```yaml
automation:
  - alias: "自动调节地暖温度"
    trigger:
      platform: numeric_state
      entity_id: sensor.indoor_temperature
      above: 26
    action:
      - service: climate.set_temperature
        target:
          entity_id: climate.phnix_heating
        data:
          temperature: 22
```

#### 定时开关机
```yaml
automation:
  - alias: "早上开启地暖"
    trigger:
      platform: time
      at: "07:00:00"
    action:
      - service: climate.turn_on
        target:
          entity_id: climate.phnix_heating
      - service: climate.set_hvac_mode
        target:
          entity_id: climate.phnix_heating
        data:
          hvac_mode: heat
      - service: climate.set_temperature
        target:
          entity_id: climate.phnix_heating
        data:
          temperature: 24

  - alias: "晚上关闭地暖"
    trigger:
      platform: time
      at: "22:00:00"
    action:
      - service: climate.turn_off
        target:
          entity_id: climate.phnix_heating
```

#### 监控设备状态
```yaml
automation:
  - alias: "设备异常报警"
    trigger:
      platform: state
      entity_id: binary_sensor.high_pressure_switch
      to: "on"
    action:
      - service: notify.mobile_app
        data:
          message: "地暖主机高压开关异常，请检查设备"
```

### 仪表板示例

```yaml
# 创建一个简单的仪表板
views:
  - title: "地暖控制"
    path: heating
    type: custom:grid-layout
    badges: []
    cards:
      - type: thermostat
        entity: climate.phnix_heating
        layout: vertical
      - type: entities
        title: "温度监控"
        entities:
          - entity: sensor.inlet_water_temp
          - entity: sensor.outlet_water_temp
          - entity: sensor.indoor_temp
          - entity: sensor.ambient_temp
      - type: entities
        title: "设备状态"
        entities:
          - entity: binary_sensor.power
          - entity: binary_sensor.compressor_output
          - entity: binary_sensor.water_pump_output
```

## 获取认证信息

### 获取设备编码

1. 登录Phnix智能云平台 (http://yun.phnixsmart.com)
2. 在设备列表中找到您的地暖主机
3. 设备编码通常以"I"开头，如：I012406020019

### 获取用户名和密码

- **用户名**: 通常是您的注册手机号
- **密码**: 您的Phnix账户登录密码

## 故障排除

### 常见问题

**Q: 配置时提示"无法连接到设备"**
A: 请检查：
- 网络连接是否正常
- 用户名和密码是否正确
- 设备编码是否正确
- 设备是否在线

**Q: 设备状态不更新**
A: 请检查：
- 设备是否在线
- 网络连接是否稳定
- 账户是否有权限访问该设备

**Q: Token过期错误**
A: 集成会自动处理token过期问题，如果频繁出现，请检查账户状态

### 日志调试

在`configuration.yaml`中启用调试日志：

```yaml
logger:
  default: info
  logs:
    custom_components.phnix_heating: debug
```

## 贡献

欢迎提交Issue和Pull Request来改进这个集成。

## 致谢

感谢Phnix提供的API接口，让这个集成成为可能。

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件。 