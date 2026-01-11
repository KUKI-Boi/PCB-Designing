"""
Component Selector - Enriches circuit with real components
For MVP: Uses local component database
Future: Integrate Octopart/LCSC API
"""
import json
from typing import Dict, List
from models import CircuitGraph, Component


class ComponentSelector:
    """Select real components with MPNs and footprints"""
    
    def __init__(self):
        """Initialize with local component database"""
        self.component_db = self._load_component_database()
    
    def enrich(self, circuit: CircuitGraph) -> CircuitGraph:
        """
        Enrich circuit components with specific MPNs and verified footprints
        
        Args:
            circuit: CircuitGraph with generic components
            
        Returns:
            CircuitGraph with enriched component data
        """
        for block in circuit.blocks:
            for component in block.components:
                # Look up component in database
                enriched_data = self._lookup_component(component.value, component.reference)
                
                if enriched_data:
                    # Update component with real data
                    if enriched_data.get('mpn') and not component.mpn:
                        component.mpn = enriched_data['mpn']
                    
                    if enriched_data.get('footprint'):
                        component.footprint = enriched_data['footprint']
                    
                    if enriched_data.get('datasheet'):
                        component.datasheet = enriched_data['datasheet']
        
        return circuit
    
    def _lookup_component(self, value: str, reference: str) -> Dict:
        """Look up component in database"""
        value_lower = value.lower()
        ref_prefix = reference[0] if reference else ""
        
        # Match by value and reference prefix
        for item in self.component_db:
            if item['value'].lower() == value_lower:
                return item
            
            # Fuzzy matching for common components
            if ref_prefix == 'C' and 'capacitor' in item.get('description', '').lower():
                if value in item['value']:
                    return item
            
            if ref_prefix == 'R' and 'resistor' in item.get('description', '').lower():
                if value in item['value']:
                    return item
        
        return {}
    
    def _load_component_database(self) -> List[Dict]:
        """Load component database (MVP: hardcoded, Future: JSON file or API)"""
        return [
            # Microcontrollers
            {
                "value": "ESP32-WROOM-32E",
                "mpn": "ESP32-WROOM-32E",
                "footprint": "RF_Module:ESP32-WROOM-32",
                "datasheet": "https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32e_datasheet_en.pdf",
                "description": "ESP32 WiFi/BLE Module",
                "supplier": "LCSC",
                "price": 2.50
            },
            {
                "value": "ATmega328P",
                "mpn": "ATMEGA328P-AU",
                "footprint": "Package_QFP:TQFP-32_7x7mm_P0.8mm",
                "datasheet": "https://ww1.microchip.com/downloads/en/DeviceDoc/ATmega328P-Datasheet.pdf",
                "description": "8-bit AVR Microcontroller",
                "supplier": "LCSC",
                "price": 1.80
            },
            
            # Voltage Regulators
            {
                "value": "AMS1117-3.3",
                "mpn": "AMS1117-3.3",
                "footprint": "Package_TO_SOT_SMD:SOT-223-3_TabPin2",
                "datasheet": "http://www.advanced-monolithic.com/pdf/ds1117.pdf",
                "description": "3.3V 1A LDO Regulator",
                "supplier": "LCSC",
                "price": 0.10
            },
            
            # Diodes
            {
                "value": "1N4007",
                "mpn": "1N4007",
                "footprint": "Diode_SMD:D_SOD-123",
                "datasheet": "https://www.vishay.com/docs/88503/1n4001.pdf",
                "description": "1A 1000V Rectifier Diode",
                "supplier": "LCSC",
                "price": 0.02
            },
            {
                "value": "1N4148",
                "mpn": "1N4148W",
                "footprint": "Diode_SMD:D_SOD-123",
                "datasheet": "https://www.vishay.com/docs/81857/1n4148.pdf",
                "description": "Fast Switching Diode",
                "supplier": "LCSC",
                "price": 0.01
            },
            
            # Transistors
            {
                "value": "2N2222",
                "mpn": "MMBT2222A",
                "footprint": "Package_TO_SOT_SMD:SOT-23",
                "datasheet": "https://www.onsemi.com/pdf/datasheet/mmbt2222alt1-d.pdf",
                "description": "NPN Switching Transistor",
                "supplier": "LCSC",
                "price": 0.03
            },
            
            # Capacitors (generic - actual MPNs would vary by exact value)
            {
                "value": "100nF",
                "mpn": "CL10B104KB8NNNC",
                "footprint": "Capacitor_SMD:C_0603_1608Metric",
                "description": "100nF Ceramic Capacitor X7R",
                "supplier": "LCSC",
                "price": 0.01
            },
            {
                "value": "10uF",
                "mpn": "CL21A106KAYNNNE",
                "footprint": "Capacitor_SMD:C_0805_2012Metric",
                "description": "10uF Ceramic Capacitor X5R",
                "supplier": "LCSC",
                "price": 0.05
            },
            {
                "value": "22uF",
                "mpn": "CL21A226MQQNNNE",
                "footprint": "Capacitor_SMD:C_0805_2012Metric",
                "description": "22uF Ceramic Capacitor X5R",
                "supplier": "LCSC",
                "price": 0.08
            },
            {
                "value": "22pF",
                "mpn": "CL10C220JB8NNNC",
                "footprint": "Capacitor_SMD:C_0603_1608Metric",
                "description": "22pF Ceramic Capacitor C0G",
                "supplier": "LCSC",
                "price": 0.01
            },
            
            # Resistors (generic)
            {
                "value": "10k",
                "mpn": "RC0603FR-0710KL",
                "footprint": "Resistor_SMD:R_0603_1608Metric",
                "description": "10k 1% Resistor",
                "supplier": "LCSC",
                "price": 0.01
            },
            {
                "value": "1k",
                "mpn": "RC0603FR-071KL",
                "footprint": "Resistor_SMD:R_0603_1608Metric",
                "description": "1k 1% Resistor",
                "supplier": "LCSC",
                "price": 0.01
            },
            {
                "value": "330",
                "mpn": "RC0603FR-07330RL",
                "footprint": "Resistor_SMD:R_0603_1608Metric",
                "description": "330 ohm 1% Resistor",
                "supplier": "LCSC",
                "price": 0.01
            },
            {
                "value": "4.7k",
                "mpn": "RC0603FR-074K7L",
                "footprint": "Resistor_SMD:R_0603_1608Metric",
                "description": "4.7k 1% Resistor",
                "supplier": "LCSC",
                "price": 0.01
            },
            
            # Sensors
            {
                "value": "DHT22",
                "mpn": "AM2302",
                "footprint": "Sensor:Aosong_DHT22_5.08x5.8mm",
                "datasheet": "https://www.sparkfun.com/datasheets/Sensors/Temperature/DHT22.pdf",
                "description": "Temperature and Humidity Sensor",
                "supplier": "LCSC",
                "price": 3.50
            }
        ]


# CLI test function
if __name__ == "__main__":
    from intent_parser import IntentParser
    from circuit_designer import CircuitDesigner
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python component_selector.py 'your hardware description'")
        sys.exit(1)
    
    # Full pipeline test
    parser = IntentParser()
    designer = CircuitDesigner()
    selector = ComponentSelector()
    
    prompt = " ".join(sys.argv[1:])
    
    intent = parser.parse(prompt)
    circuit = designer.design(intent)
    enriched_circuit = selector.enrich(circuit)
    
    print(f"\nEnriched Circuit for: {intent.application}\n")
    for block in enriched_circuit.blocks:
        print(f"{block.name}:")
        for comp in block.components:
            mpn_str = f" [MPN: {comp.mpn}]" if comp.mpn else ""
            print(f"  {comp.reference}: {comp.value}{mpn_str}")
            print(f"    Footprint: {comp.footprint}")
