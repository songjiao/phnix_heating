"""API client for Phnix Heating System."""
import logging
import aiohttp
from typing import Any, Dict, List, Optional
from .const import (
    API_BASE_URL, API_CONTROL_ENDPOINT, API_STATUS_ENDPOINT, API_CONFIG_ENDPOINT,
    DEFAULT_HEADERS, DEFAULT_PROTOCOL_ID
)

_LOGGER = logging.getLogger(__name__)

class PhnixAPIError(Exception):
    """Exception raised for Phnix API errors."""
    pass

class PhnixAPI:
    """API client for Phnix Heating System."""
    
    def __init__(self, token: str, device_code: str, protocol_id: str = DEFAULT_PROTOCOL_ID):
        """Initialize the API client."""
        self.token = token
        self.device_code = device_code
        self.protocol_id = protocol_id
        self.session: Optional[aiohttp.ClientSession] = None
        
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
        return self.session
    
    async def _make_request(self, endpoint: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make API request."""
        session = await self._get_session()
        headers = {**DEFAULT_HEADERS, "x-token": self.token}
        
        try:
            async with session.post(
                f"{API_BASE_URL}{endpoint}",
                headers=headers,
                json=data,
                timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status != 200:
                    raise PhnixAPIError(f"HTTP {response.status}: {response.reason}")
                
                result = await response.json()
                
                if not result.get("isReusltSuc", False):
                    error_msg = result.get("error_msg", "Unknown error")
                    error_code = result.get("error_code", "Unknown")
                    raise PhnixAPIError(f"API Error {error_code}: {error_msg}")
                
                return result
                
        except aiohttp.ClientError as e:
            raise PhnixAPIError(f"Network error: {e}")
        except Exception as e:
            raise PhnixAPIError(f"Unexpected error: {e}")
    
    async def set_power(self, power: bool) -> bool:
        """Set device power state."""
        value = "1" if power else "0"
        data = {
            "deviceCode": self.device_code,
            "protocalId": self.protocol_id,
            "address": "1011",
            "value": value
        }
        
        result = await self._make_request(API_CONTROL_ENDPOINT, data)
        _LOGGER.debug("Set power result: %s", result)
        return True
    
    async def set_mode(self, mode: str) -> bool:
        """Set device mode (0=制冷, 1=制热)."""
        data = {
            "deviceCode": self.device_code,
            "protocalId": self.protocol_id,
            "address": "1012",
            "value": mode
        }
        
        result = await self._make_request(API_CONTROL_ENDPOINT, data)
        _LOGGER.debug("Set mode result: %s", result)
        return True
    
    async def set_temperature(self, temp: float, is_cooling: bool) -> bool:
        """Set temperature for cooling or heating mode."""
        address = "1158" if is_cooling else "1159"
        data = {
            "deviceCode": self.device_code,
            "protocalId": self.protocol_id,
            "address": address,
            "value": str(int(temp))
        }
        
        result = await self._make_request(API_CONTROL_ENDPOINT, data)
        _LOGGER.debug("Set temperature result: %s", result)
        return True
    
    async def get_device_status(self) -> Dict[str, Any]:
        """Get complete device status."""
        data = {
            "protocalId": self.protocol_id,
            "pageIndex": 1,
            "pageSize": 9999,
            "deviceCode": self.device_code,
            "content": "",
            "num": ""
        }
        
        result = await self._make_request(API_STATUS_ENDPOINT, data)
        return result.get("objectResult", {}).get("dataList", [])
    
    async def get_control_config(self, address: str) -> Dict[str, Any]:
        """Get control configuration for specific address."""
        data = {
            "deviceCode": self.device_code,
            "pageIndex": 1,
            "pageSize": 10,
            "address": address
        }
        
        result = await self._make_request(API_CONFIG_ENDPOINT, data)
        return result.get("objectResult", {}).get("dataList", [])
    
    async def close(self):
        """Close the API session."""
        if self.session and not self.session.closed:
            await self.session.close() 