# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Home Assistant custom integration for Phnix heating systems. Communicates with Phnix cloud platform (`server.phnixsmart.com`) via async HTTP API to provide temperature control and device monitoring.

## Architecture

```
custom_components/phnix_heating/
├── __init__.py       # Integration entry point, loads platforms
├── phnix_api.py      # Async API client (login, control, status)
├── config_flow.py    # UI configuration flow
├── const.py          # API endpoints, device addresses, constants
├── climate.py        # Thermostat entity (on/off, heat/cool, temperature)
├── sensor.py         # 30+ sensor entities (temps, pressures, power)
├── binary_sensor.py  # 20+ binary sensors (outputs, safety switches)
└── translations/     # en.json, zh-Hans.json
```

**Data Flow:** ConfigFlow → PhnixAPI → Platform Entities (climate/sensor/binary_sensor)

**Key Design Patterns:**
- All API calls go through `PhnixAPI` class with automatic token refresh and re-login on 401
- Device state is fetched via address-based system (e.g., `2011` = power, `2047` = indoor temp)
- Control commands use different addresses (e.g., `1011` = power control, `1158/1159` = temp setpoints)

## Development

This is a Home Assistant integration - no build system or package manager.

**Local Testing:**
1. Copy `custom_components/phnix_heating/` to your HA config directory
2. Restart Home Assistant
3. Enable debug logging:
```yaml
logger:
  logs:
    custom_components.phnix_heating: debug
```

**No existing test suite.** Consider adding pytest with `pytest-homeassistant-custom-component`.

## Key Constants (const.py)

**API Endpoints:**
- Login: `/crmservice/api/app/user/login`
- Control: `/crmservice/api/app/device/createDeviceControlConfigData`
- Status: `/crmservice/api/app/device/getControlDetailStatusByDeviceCode`

**Important Device Addresses:**
- Read: `2011` (power), `2012` (mode), `2047` (indoor temp)
- Write: `1011` (power), `1012` (mode), `1158` (cool temp), `1159` (heat temp)

## API Authentication

- Uses MD5 hashed password
- Token generated client-side from login response
- Auto re-login when receiving 401 or "请重新登录" message
