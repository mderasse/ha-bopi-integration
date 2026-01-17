# BoPi Home Assistant Integration

[![GitHub Release](https://img.shields.io/github/release/mderasse/ha-bopi-integration.svg?style=flat-square)](https://github.com/mderasse/ha-bopi-integration/releases)
[![GitHub Activity](https://img.shields.io/github/commit-activity/y/mderasse/ha-bopi-integration.svg?style=flat-square)](https://github.com/mderasse/ha-bopi-integration/commits/main)
[![License](https://img.shields.io/github/license/mderasse/ha-bopi-integration.svg?style=flat-square)](LICENSE.md)
[![HACS](https://img.shields.io/badge/HACS-Default-orange.svg?style=flat-square)](https://github.com/hacs/integration)

A Home Assistant integration for [BoPi](https://meetbopi.com) swimming pool controller devices.

## About This Integration

This integration allows Home Assistant to communicate with BoPi controller devices via their local HTTP API. BoPi is a sophisticated pool automation system that monitors and controls various aspects of your swimming pool including:

- **Temperature Monitoring**: Track pool water and controller internal temperatures
- **Water Chemistry**: Monitor pH and ORP (redox) levels in real-time
- **Equipment Control**: Control pool pump and lighting systems
- **Relay Management**: Manage up to 4 independent relays for auxiliary equipment
- **Environmental Monitoring**: Track internal humidity and system uptime

## Features

### Sensors

The integration provides the following sensor entities:

| Sensor | Description | Device Class | Unit |
|--------|-------------|--------------|------|
| Water Temperature 1 | Primary pool water temperature | Temperature | °C |
| Water Temperature 2 | Secondary pool water temperature | Temperature | °C |
| Controller Temperature | Internal controller temperature | Temperature | °C |
| Controller Humidity | Internal controller humidity | Humidity | % |
| pH Level | Pool water pH value | pH | - |
| ORP Level | Pool water oxidation-reduction potential | - | mV |
| Uptime | Controller uptime | Duration | seconds |

> **Note**: Controller temperature, controller humidity, and uptime sensors are classified as diagnostic entities.

### Switches

The integration provides switch entities for equipment control:

| Switch | Description | Icon |
|--------|-------------|------|
| Pool Pump | Control the main pool pump | mdi:pump |
| Pool Lights | Control pool lighting | mdi:lightbulb |
| Relay 1-4 | Control auxiliary relays | mdi:electric-switch |

> **⚠️ Important**: Switch control is **read-only** in the current version. The switches display the current state of the relays but cannot be controlled yet. Attempting to toggle a switch will show a "not implemented" error. This feature will be added in a future release when the BoPi API supports relay control.

### Services

| Service | Description |
|---------|-------------|
| `bopi.refresh` | Immediately refresh all sensor data from the BoPi device |

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
3. Copy the `custom_components/bopi` folder to your Home Assistant `custom_components` directory
4. Restart Home Assistant

## Configuration

### Initial Setup

1. Go to **Settings** → **Devices & Services** → **Integrations**
2. Click **+ Add Integration**
3. Search for "BoPi"
4. Enter your BoPi device details:
   - **Host**: IP address or hostname of your BoPi device (e.g., `192.168.1.100`)
   - **Port**: API port (default: `80`, valid range: 1-65535)
   - **Timeout**: Request timeout in seconds (default: `30`, valid range: 1-300)
5. Click **Submit**

### Configuration Options

After setup, you can configure additional options:

| Option | Description | Default | Range |
|--------|-------------|---------|-------|
| Update Interval | How often to poll the BoPi device | 60 seconds | 60+ seconds |

To modify options: **Settings** → **Devices & Services** → **BoPi** → **Configure**

### Reconfiguration

To update connection settings without removing the integration:

1. Go to **Settings** → **Devices & Services** → **BoPi**
2. Click the three-dot menu (⋮)
3. Select **Reconfigure**
4. Update the settings as needed

## Supported Devices

This integration supports all BoPi controller devices with HTTP API support.

For more information about BoPi devices, visit [meetbopi.com](https://meetbopi.com)

## Troubleshooting

### Cannot Connect to BoPi Device

- Verify the BoPi device is powered on and connected to the network
- Check that the host IP address is correct
- Ensure the BoPi API port is accessible from your Home Assistant instance
- Check firewall rules - ensure the configured port is not blocked
- Try increasing the timeout value if you have a slow network

### Sensors Show Unavailable

- Check your network connection to the BoPi device
- Verify the device is responding to API requests
- Check the Home Assistant logs for error messages
- Try using the `bopi.refresh` service to force a data update

### Temperature/Chemistry Sensors Show Unknown

- These sensors will be `unknown` if the corresponding physical sensor is disconnected from the BoPi device
- Check BoPi device configuration to ensure sensors are properly connected
- A temperature value of -127°C typically indicates a disconnected temperature sensor

### High CPU/Network Usage

- The minimum scan interval is 60 seconds to prevent overloading the device
- If you need more frequent updates for specific scenarios, use the `bopi.refresh` service

## Entity Categories

Entities follow Home Assistant best practices:

- **Diagnostic entities**: Controller temperature, controller humidity, and uptime (hidden by default in entity lists)
- **Primary entities**: All water quality sensors and control switches

## Development

### Requirements

- Python 3.13+
- Home Assistant development environment
- [meetbopi](https://github.com/mderasse/python-bopi) library (installed as dependency)

### Project Structure

\`\`\`
custom_components/bopi/
├── __init__.py           # Integration setup and lifecycle
├── config_flow.py        # UI configuration and options flow
├── coordinator.py        # Data update coordinator
├── const.py              # Constants and defaults
├── sensor.py             # Sensor platform
├── switch.py             # Switch platform
├── services.py           # Service actions
├── services.yaml         # Service definitions
├── manifest.json         # Integration metadata
├── strings.json          # Base strings and translations
└── translations/         # Localized translations
    ├── en.json
    ├── es.json
    └── fr.json
\`\`\`

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create a feature branch (\`git checkout -b feature/amazing-feature\`)
3. Commit your changes (\`git commit -m 'Add amazing feature'\`)
4. Push to the branch (\`git push origin feature/amazing-feature\`)
5. Open a Pull Request

## Support

For issues, questions, or contributions:

- 📋 **Issues**: [GitHub Issues](https://github.com/mderasse/ha-bopi-integration/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/mderasse/ha-bopi-integration/discussions)

## License

This project is licensed under the MIT License - see [LICENSE.md](LICENSE.md) for details.

## Disclaimer

This is an unofficial integration. BoPi is a registered trademark of its respective owners. This integration is not affiliated with or endorsed by BoPi.

## Changelog

### Version 1.1.0

- Improved entity descriptions with icons
- Added entity categories (diagnostic) for controller sensors
- Refactored switch entities to use SwitchEntityDescription pattern
- Added data descriptions in config flow for better UX
- Improved translation files with full descriptions
- Added input validation for port (1-65535) and timeout (1-300) values
- Fixed service registration/unregistration on load/unload
- Improved state class for uptime sensor (TOTAL_INCREASING)
- Updated sensor names for clarity (Temperature → Water temperature)
- Code improvements following Home Assistant guidelines

### Version 1.0.0

- Initial release
- Support for temperature, humidity, pH, and ORP sensors
- Support for pool pump, pool lights, and relay switches
- UI-based configuration flow
- Configurable polling interval
- Multi-language support (EN, FR, ES)
