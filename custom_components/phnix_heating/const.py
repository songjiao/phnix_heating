"""Constants for the Phnix Heating integration."""
from typing import Final

DOMAIN: Final = "phnix_heating"

# 配置项
CONF_DEVICE_CODE = "device_code"
CONF_PROTOCOL_ID = "protocol_id"
CONF_TOKEN = "token"
CONF_SCAN_INTERVAL = "scan_interval"

# 默认值
DEFAULT_SCAN_INTERVAL = 30
DEFAULT_PROTOCOL_ID = "1679324789907087360"

# API相关
API_BASE_URL = "https://server.phnixsmart.com"
API_CONTROL_ENDPOINT = "/crmservice/api/app/device/createDeviceControlConfigData"
API_STATUS_ENDPOINT = "/crmservice/api/app/device/getControlDetailStatusByDeviceCode"
API_CONFIG_ENDPOINT = "/crmservice/api/app/device/getControlParamConfigByDeviceCode"

# 请求头
DEFAULT_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "http://yun.phnixsmart.com",
    "Pragma": "no-cache",
    "Referer": "http://yun.phnixsmart.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"'
}

# 控制地址
ADDRESS_POWER = "1011"  # 开关机控制
ADDRESS_MODE = "1012"   # 工作模式
ADDRESS_COOL_TEMP = "1158"  # 制冷温度设定
ADDRESS_HEAT_TEMP = "1159"  # 制热温度设定

# 状态地址
ADDRESS_POWER_STATUS = "2011"  # 开关机状态
ADDRESS_MODE_STATUS = "2012"   # 运行模式
ADDRESS_FUNCTION = "2013"      # 运行功能

# 温度传感器地址
ADDRESS_INLET_WATER_TEMP = "2045"   # 进水温度
ADDRESS_OUTLET_WATER_TEMP = "2046"  # 出水温度
ADDRESS_INDOOR_TEMP = "2047"        # 室内温度
ADDRESS_AMBIENT_TEMP = "2048"       # 环境温度
ADDRESS_COIL_TEMP = "2049"          # 盘管温度
ADDRESS_SUCTION_TEMP = "2051"       # 回气温度
ADDRESS_EXHAUST_TEMP = "2053"       # 排气温度
ADDRESS_FROST_TEMP = "2055"         # 防冻温度
ADDRESS_HOT_WATER_TEMP = "2056"     # 热水温度
ADDRESS_EVI_INLET_TEMP = "2063"     # 增焓进温度
ADDRESS_EVI_OUTLET_TEMP = "2064"    # 增焓出温度

# 压力和流量地址
ADDRESS_SUCTION_PRESSURE = "2070"   # 回气压力
ADDRESS_EXHAUST_PRESSURE = "2071"   # 排气压力
ADDRESS_WATER_FLOW = "2057"         # 水流量

# 电气参数地址
ADDRESS_AC_VOLTAGE = "2038"         # AC输入电压
ADDRESS_AC_CURRENT = "2039"         # AC输入电流
ADDRESS_COMP_CURRENT = "2040"       # 压缩机相电流
ADDRESS_DC_BUS_VOLTAGE = "2041"     # DC母线电压
ADDRESS_IPM_TEMP = "2042"           # IPM温度
ADDRESS_POWER_INPUT = "2031"        # 电表输入功率
ADDRESS_HEAT_PUMP_CAPACITY = "2032" # 热泵能力
ADDRESS_COP = "2033"                # COP

# 运行参数地址
ADDRESS_COMP_FREQ = "2025"          # 压缩机频率
ADDRESS_FAN1_SPEED = "2029"         # 风机1转速
ADDRESS_FAN2_SPEED = "2030"         # 风机2转速
ADDRESS_EEV_OPENING = "2020"        # 电子膨胀阀开度
ADDRESS_EVI_EEV_OPENING = "2021"    # 增焓电子膨胀阀开度
ADDRESS_COMP_RUNTIME = "2043"       # 压缩机运行时间
ADDRESS_ELECTRICITY = "2035"        # 电表电量

# 通信状态地址
ADDRESS_DTU_SIGNAL = "2037"         # DTU信号强度
ADDRESS_DTU_ONLINE = "2130"         # DTU在线标志
ADDRESS_MULTI_UNIT_COMM = "2059"    # 回水多机组并联通信状态

# 输出状态地址 (address: 2019)
OUTPUT_COMPRESSOR = "O01"           # 压缩机输出
OUTPUT_SECONDARY_PUMP = "O02"       # 二次泵输出
OUTPUT_HIGH_FAN = "O03"             # 高风输出
OUTPUT_LOW_FAN = "O04"              # 低风输出
OUTPUT_FOUR_WAY_VALVE = "O05"       # 四通阀输出
OUTPUT_HOT_WATER_VALVE = "O06"      # 热水三通阀输出
OUTPUT_WATER_PUMP = "O07"           # 水泵输出
OUTPUT_ELECTRIC_HEAT = "O08"        # 电加热输出
OUTPUT_SPRAY_VALVE = "O09"          # 喷淋阀输出
OUTPUT_FROST_HEAT = "O10"           # 防冻加热带输出
OUTPUT_CRANKCASE_HEAT = "O11"       # 系统1曲轴加热带输出
OUTPUT_WATER_SUPPLY = "bit11"       # 补水阀输出
OUTPUT_ALARM = "O13"                # 报警输出
OUTPUT_COOL_WATER_VALVE = "bit13"   # 制冷水阀输出
OUTPUT_HEAT_WATER_VALVE = "bit14"   # 制热水阀输出

# 安全开关地址 (address: 2034)
SWITCH_HIGH_PRESSURE = "S01"        # 高压开关
SWITCH_LOW_PRESSURE = "S03"         # 低压开关
SWITCH_WATER_FLOW = "S04"           # 水流开关
SWITCH_DRY_BURN = "S05"             # 电加热干烧开关
SWITCH_MODE_INPUT = "S06"           # 模式输入
SWITCH_EMERGENCY = "S09"            # 应急开关

# 模式值
MODE_COOL = "0"  # 制冷
MODE_HEAT = "1"  # 制热

# 开关值
POWER_OFF = "0"  # 关机
POWER_ON = "1"   # 开机

# 温度范围
COOL_TEMP_MIN = 5
COOL_TEMP_MAX = 25
HEAT_TEMP_MIN = 25
HEAT_TEMP_MAX = 60

# 实体类型
ENTITY_TYPE_CLIMATE = "climate"
ENTITY_TYPE_SENSOR = "sensor"
ENTITY_TYPE_BINARY_SENSOR = "binary_sensor" 