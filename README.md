# AI Hardware Designer

> Convert natural language hardware ideas into real, manufacturable PCB designs

## Overview

AI Hardware Designer is a production-grade system that transforms text descriptions into complete PCB designs with schematics, layouts, and manufacturing files.

**Example:**
```bash
python backend/main.py "ESP32 based smart irrigation controller with soil sensor and relay"
```

**Output:**
- ✅ KiCad schematic (.kicad_sch)
- ✅ KiCad PCB layout (.kicad_pcb)
- ✅ Bill of Materials (BOM.csv)
- ✅ Pick-and-Place file
- ✅ Gerber files

## Features

- 🧠 **AI-Powered Intent Parsing** - Uses LLM to understand hardware requirements
- ⚡ **Automatic Circuit Design** - Generates complete circuits with proper support components
- 🔧 **Real Component Selection** - Includes actual MPNs, footprints, and datasheets
- 📐 **KiCad Integration** - Generates native KiCad schematic and PCB files
- 🏭 **Manufacturing Ready** - Exports BOM, Pick-and-Place, and Gerber files

## Installation

### Prerequisites
- Python 3.8+
- KiCad 7.0+ (optional, for opening generated files)

### Setup

1. **Clone or navigate to the project:**
```bash
cd "d:/Desktop/Personal projects/PCB AI"
```

2. **Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Install dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

4. **Configure API key:**
```bash
cp .env.example .env
# Edit .env and add your OpenRouter/OpenAI key
```

## Usage

### Basic Usage

```bash
python main.py "ESP32 based smart irrigation controller with soil sensor and relay"
```

### Advanced Options

```bash
# Custom output directory
python main.py "Arduino temperature logger with DHT22" -o my_project

# Custom project name
python main.py "STM32 motor controller" --name motor_ctrl

# Skip Gerber generation
python main.py "ESP32 WiFi sensor" --skip-gerbers
```

### Output Structure

```
output/
├── design.kicad_sch        # KiCad schematic
├── design.kicad_pcb        # KiCad PCB layout
├── design_BOM.csv          # Bill of Materials
├── design_PickAndPlace.csv # Pick-and-Place file
└── gerbers/                # Gerber files (if generated)
```

## Architecture

```
User Input (Text)
    ↓
Intent Parser (LLM)
    ↓
Circuit Designer
    ↓
Component Selector
    ↓
KiCad Generator
    ↓
Manufacturing Exporter
    ↓
Output Files
```

### Modules

- **`models.py`** - Pydantic data models for type safety
- **`intent_parser.py`** - Natural language → HardwareIntent
- **`circuit_designer.py`** - HardwareIntent → CircuitGraph
- **`component_selector.py`** - Enriches with real components
- **`kicad_generator.py`** - Generates .kicad_sch and .kicad_pcb
- **`manufacturing.py`** - Exports BOM, P&P, Gerbers
- **`main.py`** - CLI orchestrator

## Supported Components

### Microcontrollers
- ESP32-WROOM-32E (WiFi/Bluetooth)
- ATmega328P (Arduino)

### Sensors
- Soil moisture sensors
- DHT22 (Temperature/Humidity)

### Outputs
- Relays (with driver circuits)
- LEDs

### Power
- 12V/5V input with LDO regulation
- Automatic decoupling capacitors
- Reverse polarity protection

## AI Design Features

The system automatically adds:
- ✅ Decoupling capacitors (100nF, 10uF)
- ✅ Pull-up/pull-down resistors
- ✅ Flyback diodes for relays
- ✅ Voltage regulation (AMS1117-3.3)
- ✅ Crystal oscillators with load caps
- ✅ Reset and boot circuits

## API Keys

### OpenRouter (Recommended)
Free tier available: https://openrouter.ai/

```env
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

### Alternatives
- OpenAI API
- Anthropic Claude API

## Roadmap

- [x] Backend pipeline
- [x] MVP component library
- [ ] Advanced auto-routing
- [ ] Web-based UI (Flux-style)
- [ ] Octopart/LCSC integration
- [ ] 3D preview
- [ ] DRC/ERC automation
- [ ] Multi-layer PCB support (4-6 layers)

## Examples

### Example 1: ESP32 + Relay
```bash
python main.py "ESP32 based smart irrigation controller with soil sensor and relay"
```

Generates:
- ESP32-WROOM-32E module
- AMS1117-3.3 voltage regulator
- Soil moisture sensor interface
- 5V relay with NPN driver and flyback diode
- Power supply with protection
- All decoupling capacitors

### Example 2: Arduino Temperature Logger
```bash
python main.py "Arduino temperature logger with DHT22 sensor"
```

Generates:
- ATmega328P microcontroller
- 16MHz crystal with load caps
- DHT22 sensor with pull-up
- Power regulation
- Programming header

## License

MIT License - See LICENSE file

## Contributing

Contributions welcome! This is a production-grade system, not a mockup.

## Support

For issues or questions, open a GitHub issue.

---

**Built with:**
- Python 3.x
- OpenRouter AI
- KiCad 7.0
- Pydantic
