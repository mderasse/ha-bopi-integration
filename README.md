# BoPi Home Assistant Integration

[![GitHub Release](https://img.shields.io/github/release/mderasse/ha-bopi-integration.svg?style=flat-square)](https://github.com/mderasse/ha-bopi-integration/releases)
[![GitHub Activity](https://img.shields.io/github/commit-activity/y/mderasse/ha-bopi-integration.svg?style=flat-square)](https://github.com/mderasse/ha-bopi-integration/commits/main)
[![License](https://img.shields.io/github/license/mderasse/ha-bopi-integration.svg?style=flat-square)](LICENSE.md)

A Home Assistant integration for [BoPi](https://meetbopi.com) swimming pool controller devices.

## About This Integration

This integration allows Home Assistant to communicate with BoPi controller devices via their local HTTP API. BoPi is a sophisticated pool automation system that monitors and controls various aspects of your swimming pool including:

- **Temperature Monitoring**: Track pool and internal box temperatures
- **Water Chemistry**: Monitor pH and redox (ORP) levels
- **Equipment Control**: Control pool pump and lighting systems
- **Relay Management**: Manage up to 4 independent relays for auxiliary equipment
- **Environmental Monitoring**: Track internal humidity and system uptime

## Features

### Sensors

The integration exposes the following sensor entities:

- **Temperature Sensors**

  - Pool Water Temperature 1
  - Pool Water Temperature 2
  - Internal Box Temperature

- **Chemistry Sensors**

  - pH Level (0-14)
  - Redox Value (0-1000 mV)

- **Environmental**
  - Internal Box Humidity
  - System Uptime

### Binary Sensors

The integration provides binary sensor entities for equipment status:

- Pool Pump Status (on/off)
- Pool Lights Status (on/off)
- Relay 1 Status (on/off)
- Relay 2 Status (on/off)
- Relay 3 Status (on/off)
- Relay 4 Status (on/off)

## Prerequisites

- Home Assistant 2024.1 or later
- BoPi device with HTTP API enabled
- Network connectivity between Home Assistant and BoPi device (local network)

## Installation

### Via HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to **Integrations**
3. Click **Explore & Download Repositories**
4. Search for "BoPi"
5. Click **Download**
6. Restart Home Assistant

### Manual Installation

1. Download the latest release from [GitHub Releases](https://github.com/mderasse/ha-bopi-integration/releases)
2. Extract the archive
3. Copy the `bopi` folder to your Home Assistant `custom_components` directory
4. Restart Home Assistant

## Configuration

### Setup via UI

1. Go to **Settings** → **Devices & Services** → **Integrations**
2. Click **Create Integration**
3. Search for "BoPi"
4. Enter your BoPi device details:
   - **Host**: IP address or hostname of your BoPi device (e.g., `192.168.1.100`)
   - **Port**: API port (default: `80`)
   - **Timeout**: Request timeout in seconds (default: `30`)
5. Click **Create**

### Configuration Options

After setup, you can adjust:

- **Scan Interval**: How often to poll the BoPi device (minimum 60 seconds, default 60 seconds)

Go to **Settings** → **Devices & Services** → **BoPi** → **Options** to modify.

## Supported Devices

This integration supports all BoPi controller devices with HTTP API support.

For more information about BoPi devices, visit [meetbopi.com](https://meetbopi.com)

## Troubleshooting

### Cannot Connect to BoPi Device

- Verify the BoPi device is powered on and connected to the network
- Check that the host IP address is correct
- Ensure the BoPi API port is accessible from your Home Assistant instance
- Check firewall rules - ensure port 80 (or your configured port) is not blocked

### Sensors Show Unavailable

- Check your network connection to the BoPi device
- Verify the device is responding to API requests
- Check the Home Assistant logs for error messages
- Try increasing the timeout value in configuration

### Temperature/Chemistry Sensors Always Null

- These sensors are expected to be null if the corresponding physical sensor is disconnected from the BoPi device
- Check BoPi device configuration to ensure sensors are properly connected
- Temperature value -127 indicates a disconnected sensor and is displayed as unavailable

## Entity Categories

Entities follow Home Assistant entity category best practices:

- Sensor entities are automatically categorized based on their type (diagnostic for uptime, none for measurements)
- Binary sensor entities use the appropriate device class for proper UI representation

## Integration Quality Scale

This integration is currently at the **Bronze** quality level, supporting:

- ✅ Config flow with UI configuration
- ✅ Entity unique IDs for proper tracking
- ✅ Device information with proper associations
- ✅ Basic error handling and validation

## Development

### Requirements

- Python 3.13+
- Home Assistant development environment
- [meetbopi](https://github.com/mderasse/python-bopi) library (installed as dependency)

### Project Structure

```
custom_components/bopi/
├── __init__.py           # Integration setup and lifecycle
├── config_flow.py        # UI configuration flow
├── coordinator.py        # Data update coordinator
├── const.py             # Constants and defaults
├── sensor.py            # Sensor platform
├── binary_sensor.py     # Binary sensor platform
├── manifest.json        # Integration metadata
├── strings.json         # User-facing strings and translations
└── quality_scale.yaml   # Quality scale status tracking
```

### Testing

To test this integration locally:

1. Clone the repository
2. Copy the `custom_components/bopi` folder to your Home Assistant `custom_components` directory
3. Restart Home Assistant
4. Add the integration via UI

## Support

For issues, questions, or contributions:

- 📋 **Issues**: [GitHub Issues](https://github.com/mderasse/ha-bopi-integration/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/mderasse/ha-bopi-integration/discussions)

## License

This project is licensed under the MIT License - see [LICENSE.md](LICENSE.md) for details.

## Disclaimer

This is an unofficial integration. BoPi is a registered trademark of its respective owners. This integration is not affiliated with or endorsed by BoPi.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Changelog

### Version 0.0.1

- Initial release
- Support for temperature, humidity, pH, and redox sensors
- Support for pool pump, pool lights, and relay binary sensors
- UI-based configuration flow
- Configurable polling interval
