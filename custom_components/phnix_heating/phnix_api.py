"""API client for Phnix Heating system."""
import logging
import hashlib
import aiohttp
from typing import Any, Dict, List, Optional

from .const import (
    LOGIN_URL, CONTROL_URL, STATUS_URL, CONFIG_URL,
    DEFAULT_HEADERS, LOGIN_DATA, POWER_ADDRESS, MODE_ADDRESS,
    COOL_TEMP_ADDRESS, HEAT_TEMP_ADDRESS, POWER_OFF, POWER_ON,
    MODE_COOL, MODE_HEAT
)

_LOGGER = logging.getLogger(__name__)

class PhnixAPIError(Exception):
    """Exception raised for Phnix API errors."""
    pass

class PhnixAPI:
    """Phnix Heating API client."""
    
    def __init__(self, username: str, password: str, device_code: str):
        """Initialize the API client."""
        self.username = username
        self.password = password
        self.device_code = device_code
        self.token: Optional[str] = None
        self.session: Optional[aiohttp.ClientSession] = None
        self._protocol_id: Optional[str] = None
        
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    def _hash_password(self, password: str) -> str:
        """Hash password using MD5."""
        return hashlib.md5(password.encode()).hexdigest()
    
    async def login(self) -> None:
        """Login and get token."""
        try:
            session = await self._get_session()
            
            # 准备登录数据
            login_data = {
                **LOGIN_DATA,
                "userName": self.username,
                "password": self._hash_password(self.password)
            }
            
            _LOGGER.debug("正在登录...")
            
            async with session.post(
                LOGIN_URL,
                headers=DEFAULT_HEADERS,
                json=login_data
            ) as response:
                if response.status != 200:
                    raise PhnixAPIError(f"登录失败，HTTP状态码: {response.status}")
                
                data = await response.json()
                
                if not data.get("isReusltSuc"):
                    error_msg = data.get("error_msg", "未知错误")
                    raise PhnixAPIError(f"登录失败: {error_msg}")
                
                # 获取token
                object_result = data.get("objectResult", {})
                self.token = object_result.get("x-token")
                
                if not self.token:
                    raise PhnixAPIError("登录成功但未获取到token")
                
                _LOGGER.debug("登录成功，获取到token")
                
        except aiohttp.ClientError as e:
            raise PhnixAPIError(f"网络连接错误: {e}")
        except Exception as e:
            raise PhnixAPIError(f"登录过程中发生错误: {e}")
    
    async def _ensure_token(self) -> None:
        """Ensure we have a valid token."""
        if not self.token:
            await self.login()
    
    async def _make_request(
        self, 
        url: str, 
        data: Dict[str, Any], 
        retry_on_auth_error: bool = True
    ) -> Dict[str, Any]:
        """Make API request with token handling."""
        try:
            await self._ensure_token()
            
            session = await self._get_session()
            headers = {**DEFAULT_HEADERS, "x-token": self.token}
            
            async with session.post(url, headers=headers, json=data) as response:
                if response.status == 401 and retry_on_auth_error:
                    _LOGGER.warning("Token可能已过期，尝试重新登录")
                    self.token = None
                    await self.login()
                    headers = {**DEFAULT_HEADERS, "x-token": self.token}
                    
                    async with session.post(url, headers=headers, json=data) as retry_response:
                        if retry_response.status != 200:
                            raise PhnixAPIError(f"API请求失败，HTTP状态码: {retry_response.status}")
                        return await retry_response.json()
                
                if response.status != 200:
                    raise PhnixAPIError(f"API请求失败，HTTP状态码: {response.status}")
                
                return await response.json()
                
        except aiohttp.ClientError as e:
            raise PhnixAPIError(f"网络连接错误: {e}")
        except Exception as e:
            raise PhnixAPIError(f"API请求过程中发生错误: {e}")
    
    async def _get_protocol_id(self) -> str:
        """Get protocol ID for the device."""
        if self._protocol_id:
            return self._protocol_id
            
        # 使用默认协议ID
        self._protocol_id = "1679324789907087360"
        return self._protocol_id
    
    async def set_power(self, power: bool) -> None:
        """Set device power state."""
        protocol_id = await self._get_protocol_id()
        value = POWER_ON if power else POWER_OFF
        
        data = {
            "deviceCode": self.device_code,
            "protocalId": protocol_id,
            "address": POWER_ADDRESS,
            "value": value
        }
        
        result = await self._make_request(CONTROL_URL, data)
        
        if not result.get("isReusltSuc"):
            error_msg = result.get("error_msg", "未知错误")
            raise PhnixAPIError(f"设置电源状态失败: {error_msg}")
    
    async def set_mode(self, mode: str) -> None:
        """Set device mode (cool/heat)."""
        protocol_id = await self._get_protocol_id()
        value = MODE_COOL if mode == "cool" else MODE_HEAT
        
        data = {
            "deviceCode": self.device_code,
            "protocalId": protocol_id,
            "address": MODE_ADDRESS,
            "value": value
        }
        
        result = await self._make_request(CONTROL_URL, data)
        
        if not result.get("isReusltSuc"):
            error_msg = result.get("error_msg", "未知错误")
            raise PhnixAPIError(f"设置工作模式失败: {error_msg}")
    
    async def set_temperature(self, temperature: float, mode: str) -> None:
        """Set target temperature."""
        protocol_id = await self._get_protocol_id()
        address = COOL_TEMP_ADDRESS if mode == "cool" else HEAT_TEMP_ADDRESS
        
        data = {
            "deviceCode": self.device_code,
            "protocalId": protocol_id,
            "address": address,
            "value": str(int(temperature))
        }
        
        result = await self._make_request(CONTROL_URL, data)
        
        if not result.get("isReusltSuc"):
            error_msg = result.get("error_msg", "未知错误")
            raise PhnixAPIError(f"设置温度失败: {error_msg}")
    
    async def get_device_status(self) -> List[Dict[str, Any]]:
        """Get complete device status."""
        protocol_id = await self._get_protocol_id()
        
        data = {
            "protocalId": protocol_id,
            "pageIndex": 1,
            "pageSize": 9999,
            "deviceCode": self.device_code,
            "content": "",
            "num": ""
        }
        
        result = await self._make_request(STATUS_URL, data)
        
        if not result.get("isReusltSuc"):
            error_msg = result.get("error_msg", "未知错误")
            raise PhnixAPIError(f"获取设备状态失败: {error_msg}")
        
        object_result = result.get("objectResult", {})
        data_list = object_result.get("dataList", [])
        
        return data_list
    
    async def get_device_config(self, address: str) -> List[Dict[str, Any]]:
        """Get device configuration for specific address."""
        protocol_id = await self._get_protocol_id()
        
        data = {
            "deviceCode": self.device_code,
            "pageIndex": 1,
            "pageSize": 10,
            "address": address
        }
        
        result = await self._make_request(CONFIG_URL, data)
        
        if not result.get("isReusltSuc"):
            error_msg = result.get("error_msg", "未知错误")
            raise PhnixAPIError(f"获取设备配置失败: {error_msg}")
        
        object_result = result.get("objectResult", {})
        data_list = object_result.get("dataList", [])
        
        return data_list
    
    async def close(self) -> None:
        """Close the API client."""
        if self.session and not self.session.closed:
            await self.session.close() 