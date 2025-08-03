"""Constants for the Phnix Heating integration."""
from homeassistant.const import Platform

DOMAIN = "phnix_heating"
PLATFORMS = [Platform.CLIMATE, Platform.SENSOR, Platform.BINARY_SENSOR]

# API配置
BASE_URL = "https://server.phnixsmart.com"
LOGIN_URL = f"{BASE_URL}/crmservice/api/app/user/login"
CONTROL_URL = f"{BASE_URL}/crmservice/api/app/device/createDeviceControlConfigData"
STATUS_URL = f"{BASE_URL}/crmservice/api/app/device/getControlDetailStatusByDeviceCode"
CONFIG_URL = f"{BASE_URL}/crmservice/api/app/device/getControlParamConfigByDeviceCode"

# 默认请求头
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
    "sec-ch-ua-platform": '"Windows"',
}

# 登录请求参数
LOGIN_DATA = {
    "loginSource": "Web",
    "type": "1"
}

# 控制地址
POWER_ADDRESS = "1011"
MODE_ADDRESS = "1012"
COOL_TEMP_ADDRESS = "1158"
HEAT_TEMP_ADDRESS = "1159"

# 控制值
POWER_OFF = "0"
POWER_ON = "1"
MODE_COOL = "0"
MODE_HEAT = "1"

# 状态地址 - 温度传感器
TEMP_SENSORS = {
    "inlet_water_temp": "2045",
    "outlet_water_temp": "2046", 
    "indoor_temp": "2047",
    "ambient_temp": "2048",
    "coil_temp": "2049",
    "suction_temp": "2051",
    "exhaust_temp": "2053",
    "frost_temp": "2055",
    "hot_water_temp": "2056",
    "evi_inlet_temp": "2063",
    "evi_outlet_temp": "2064",
}

# 状态地址 - 压力传感器
PRESSURE_SENSORS = {
    "suction_pressure": "2070",
    "exhaust_pressure": "2071",
}

# 状态地址 - 流量传感器
FLOW_SENSORS = {
    "water_flow": "2057",
}

# 状态地址 - 电气参数传感器
ELECTRICAL_SENSORS = {
    "ac_voltage": "2038",
    "ac_current": "2039",
    "comp_current": "2040",
    "dc_bus_voltage": "2041",
    "ipm_temp": "2042",
    "power_input": "2031",
    "heat_pump_capacity": "2032",
    "cop": "2033",
}

# 状态地址 - 运行参数传感器
RUNNING_SENSORS = {
    "comp_freq": "2025",
    "fan1_speed": "2029",
    "fan2_speed": "2030",
    "eev_opening": "2020",
    "evi_eev_opening": "2021",
    "comp_runtime": "2043",
    "electricity": "2035",
}

# 状态地址 - 通信状态传感器
COMMUNICATION_SENSORS = {
    "dtu_signal": "2037",
    "dtu_online": "2130",
    "multi_unit_comm": "2059",
}

# 状态地址 - 输出状态
OUTPUT_ADDRESS = "2019"
OUTPUT_NAMES = {
    "O01": "压缩机输出",
    "O02": "二次泵输出", 
    "O03": "高风输出",
    "O04": "低风输出",
    "O05": "四通阀输出",
    "O06": "热水三通阀输出",
    "O07": "水泵输出",
    "O08": "电加热输出",
    "O09": "喷淋阀输出",
    "O10": "防冻加热带输出",
    "O11": "系统1曲轴加热带输出",
    "bit11": "补水阀输出",
    "O13": "报警输出",
    "bit13": "制冷水阀输出",
    "bit14": "制热水阀输出",
}

# 状态地址 - 安全开关
SAFETY_ADDRESS = "2034"
SAFETY_NAMES = {
    "S01": "高压开关",
    "S03": "低压开关",
    "S04": "水流开关",
    "S05": "电加热干烧开",
    "S06": "模式输入",
    "S09": "应急开关",
} 