"""
Circuit Designer - Hardware Intent to Circuit Blocks
Converts HardwareIntent into CircuitGraph with standard blocks
"""
from typing import List, Dict
from models import HardwareIntent, CircuitGraph, CircuitBlock, Component, NetConnection


class CircuitDesigner:
    """Design circuit architecture from hardware intent"""
    
    def __init__(self):
        """Initialize circuit designer with standard block templates"""
        self.component_counter = {
            'U': 0, 'R': 0, 'C': 0, 'D': 0, 'L': 0, 
            'J': 0, 'K': 0, 'Q': 0, 'SW': 0
        }
    
    def design(self, intent: HardwareIntent) -> CircuitGraph:
        """
        Convert HardwareIntent into complete CircuitGraph
        
        Args:
            intent: Structured hardware requirements
            
        Returns:
            CircuitGraph with all circuit blocks
        """
        circuit = CircuitGraph(intent=intent, global_nets=["GND", "VCC", "+3V3", "+5V"])
        
        # Add power supply block
        power_block = self._create_power_block(intent)
        circuit.blocks.append(power_block)
        
        # Add MCU block if specified
        if intent.mcu:
            mcu_block = self._create_mcu_block(intent)
            circuit.blocks.append(mcu_block)
        
        # Add sensor blocks
        for sensor in intent.sensors:
            sensor_block = self._create_sensor_block(sensor, intent)
            circuit.blocks.append(sensor_block)
        
        # Add output blocks (relays, LEDs, etc)
        for output in intent.outputs:
            output_block = self._create_output_block(output, intent)
            circuit.blocks.append(output_block)
        
        # Add input blocks (buttons, switches)
        for input_dev in intent.inputs:
            input_block = self._create_input_block(input_dev, intent)
            circuit.blocks.append(input_block)
        
        return circuit
    
    def _next_ref(self, prefix: str) -> str:
        """Generate next reference designator"""
        self.component_counter[prefix] += 1
        return f"{prefix}{self.component_counter[prefix]}"
    
    def _create_power_block(self, intent: HardwareIntent) -> CircuitBlock:
        """Create power regulation block"""
        block = CircuitBlock(name="Power Supply", notes="Voltage regulation and protection")
        
        # Input connector
        block.components.append(Component(
            reference=self._next_ref('J'),
            value=intent.power_input,
            footprint="Connector_BarrelJack:BarrelJack_Horizontal",
            description="Power input connector"
        ))
        
        # If we need 3.3V from higher voltage
        if "12V" in intent.power_input or "5V" in intent.power_input:
            # Add LDO regulator for 3.3V
            block.components.append(Component(
                reference=self._next_ref('U'),
                value="AMS1117-3.3",
                footprint="Package_TO_SOT_SMD:SOT-223-3_TabPin2",
                mpn="AMS1117-3.3",
                description="3.3V LDO Regulator"
            ))
            
            # Input capacitor
            block.components.append(Component(
                reference=self._next_ref('C'),
                value="10uF",
                footprint="Capacitor_SMD:C_0805_2012Metric",
                description="Input decoupling capacitor"
            ))
            
            # Output capacitor
            block.components.append(Component(
                reference=self._next_ref('C'),
                value="22uF",
                footprint="Capacitor_SMD:C_0805_2012Metric",
                description="Output stabilization capacitor"
            ))
        
        # Protection diode
        block.components.append(Component(
            reference=self._next_ref('D'),
            value="1N4007",
            footprint="Diode_SMD:D_SOD-123",
            description="Reverse polarity protection"
        ))
        
        return block
    
    def _create_mcu_block(self, intent: HardwareIntent) -> CircuitBlock:
        """Create microcontroller block"""
        block = CircuitBlock(name="Microcontroller", notes=f"{intent.mcu} with support circuitry")
        
        if "ESP32" in intent.mcu.upper():
            # ESP32 module
            block.components.append(Component(
                reference=self._next_ref('U'),
                value="ESP32-WROOM-32E",
                footprint="RF_Module:ESP32-WROOM-32",
                mpn="ESP32-WROOM-32E",
                description="ESP32 WiFi/BLE Module"
            ))
            
            # Decoupling capacitors
            for i in range(3):
                block.components.append(Component(
                    reference=self._next_ref('C'),
                    value="100nF",
                    footprint="Capacitor_SMD:C_0603_1608Metric",
                    description="Decoupling capacitor"
                ))
            
            # Boot/Reset buttons
            block.components.append(Component(
                reference=self._next_ref('SW'),
                value="RESET",
                footprint="Button_Switch_SMD:SW_SPST_CK_RS282G05A3",
                description="Reset button"
            ))
            
            block.components.append(Component(
                reference=self._next_ref('SW'),
                value="BOOT",
                footprint="Button_Switch_SMD:SW_SPST_CK_RS282G05A3",
                description="Boot mode button"
            ))
            
            # Pull-up resistors
            block.components.append(Component(
                reference=self._next_ref('R'),
                value="10k",
                footprint="Resistor_SMD:R_0603_1608Metric",
                description="EN pull-up"
            ))
            
        elif "ATMEGA328" in intent.mcu.upper():
            # Arduino-style AVR
            block.components.append(Component(
                reference=self._next_ref('U'),
                value="ATmega328P",
                footprint="Package_QFP:TQFP-32_7x7mm_P0.8mm",
                mpn="ATMEGA328P-AU",
                description="8-bit AVR Microcontroller"
            ))
            
            # Crystal
            block.components.append(Component(
                reference=self._next_ref('Y'),
                value="16MHz",
                footprint="Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm",
                description="System clock crystal"
            ))
            
            # Crystal load caps
            for i in range(2):
                block.components.append(Component(
                    reference=self._next_ref('C'),
                    value="22pF",
                    footprint="Capacitor_SMD:C_0603_1608Metric",
                    description="Crystal load capacitor"
                ))
        
        return block
    
    def _create_sensor_block(self, sensor: str, intent: HardwareIntent) -> CircuitBlock:
        """Create sensor interface block"""
        sensor_lower = sensor.lower()
        block = CircuitBlock(name=f"Sensor: {sensor}", notes=f"Interface for {sensor}")
        
        # Soil moisture sensor
        if "soil" in sensor_lower or "moisture" in sensor_lower:
            block.components.append(Component(
                reference=self._next_ref('J'),
                value="Soil_Sensor_Connector",
                footprint="Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical",
                description="Capacitive soil moisture sensor connector"
            ))
            
            # Pull-up for digital output
            block.components.append(Component(
                reference=self._next_ref('R'),
                value="10k",
                footprint="Resistor_SMD:R_0603_1608Metric",
                description="Signal pull-up"
            ))
        
        # DHT22 temperature/humidity
        elif "dht22" in sensor_lower or "temperature" in sensor_lower or "humidity" in sensor_lower:
            block.components.append(Component(
                reference=self._next_ref('U'),
                value="DHT22",
                footprint="Sensor:Aosong_DHT22_5.08x5.8mm",
                description="Temperature and humidity sensor"
            ))
            
            # Pull-up resistor for data line
            block.components.append(Component(
                reference=self._next_ref('R'),
                value="4.7k",
                footprint="Resistor_SMD:R_0603_1608Metric",
                description="Data line pull-up"
            ))
        
        return block
    
    def _create_output_block(self, output: str, intent: HardwareIntent) -> CircuitBlock:
        """Create output driver block"""
        output_lower = output.lower()
        block = CircuitBlock(name=f"Output: {output}", notes=f"Driver for {output}")
        
        # Relay
        if "relay" in output_lower:
            block.components.append(Component(
                reference=self._next_ref('K'),
                value="5V_RELAY",
                footprint="Relay_THT:Relay_SPDT_Omron-G5LE-1",
                description="5V SPDT Relay"
            ))
            
            # Driver transistor
            block.components.append(Component(
                reference=self._next_ref('Q'),
                value="2N2222",
                footprint="Package_TO_SOT_SMD:SOT-23",
                description="NPN switching transistor"
            ))
            
            # Base resistor
            block.components.append(Component(
                reference=self._next_ref('R'),
                value="1k",
                footprint="Resistor_SMD:R_0603_1608Metric",
                description="Base current limiting"
            ))
            
            # Flyback diode
            block.components.append(Component(
                reference=self._next_ref('D'),
                value="1N4148",
                footprint="Diode_SMD:D_SOD-123",
                description="Flyback protection diode"
            ))
        
        # LED
        elif "led" in output_lower:
            block.components.append(Component(
                reference=self._next_ref('D'),
                value="LED",
                footprint="LED_SMD:LED_0805_2012Metric",
                description="Status LED"
            ))
            
            block.components.append(Component(
                reference=self._next_ref('R'),
                value="330",
                footprint="Resistor_SMD:R_0603_1608Metric",
                description="LED current limiting"
            ))
        
        return block
    
    def _create_input_block(self, input_dev: str, intent: HardwareIntent) -> CircuitBlock:
        """Create input interface block"""
        input_lower = input_dev.lower()
        block = CircuitBlock(name=f"Input: {input_dev}", notes=f"Interface for {input_dev}")
        
        # Button
        if "button" in input_lower:
            block.components.append(Component(
                reference=self._next_ref('SW'),
                value="BUTTON",
                footprint="Button_Switch_SMD:SW_SPST_CK_RS282G05A3",
                description="User input button"
            ))
            
            # Pull-down resistor
            block.components.append(Component(
                reference=self._next_ref('R'),
                value="10k",
                footprint="Resistor_SMD:R_0603_1608Metric",
                description="Pull-down resistor"
            ))
        
        return block


# CLI test function
if __name__ == "__main__":
    from intent_parser import IntentParser
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python circuit_designer.py 'your hardware description'")
        sys.exit(1)
    
    # Parse intent first
    parser = IntentParser()
    prompt = " ".join(sys.argv[1:])
    intent = parser.parse(prompt)
    
    # Design circuit
    designer = CircuitDesigner()
    circuit = designer.design(intent)
    
    print(f"\nCircuit Design for: {intent.application}")
    print(f"Blocks: {len(circuit.blocks)}")
    for block in circuit.blocks:
        print(f"\n{block.name}:")
        print(f"  Components: {len(block.components)}")
        for comp in block.components:
            print(f"    - {comp.reference}: {comp.value} ({comp.description})")
