"""
Data models for AI Hardware Designer
Defines JSON schemas for internal data structures
"""
from typing import List, Dict, Optional
from pydantic import BaseModel, Field


class HardwareIntent(BaseModel):
    """Parsed user intent for hardware design"""
    application: str = Field(..., description="Main application purpose")
    mcu: Optional[str] = Field(None, description="Microcontroller type (e.g., ESP32, STM32)")
    sensors: List[str] = Field(default_factory=list, description="List of sensors")
    outputs: List[str] = Field(default_factory=list, description="Output devices (relays, LEDs, etc)")
    inputs: List[str] = Field(default_factory=list, description="Input devices (buttons, switches)")
    communication: List[str] = Field(default_factory=list, description="Communication protocols (WiFi, BLE, UART)")
    power_input: str = Field(default="5V USB", description="Primary power input")
    power_output_voltage: Optional[str] = Field(None, description="Required output voltage")
    pcb_size: str = Field(default="80x60mm", description="Target PCB dimensions")
    layers: int = Field(default=2, description="Number of PCB layers")
    additional_notes: str = Field(default="", description="Extra requirements")


class Component(BaseModel):
    """Electronic component specification"""
    reference: str = Field(..., description="Reference designator (e.g., U1, R1)")
    value: str = Field(..., description="Component value (e.g., 10k, 100nF)")
    footprint: str = Field(..., description="KiCad footprint library reference")
    mpn: Optional[str] = Field(None, description="Manufacturer Part Number")
    description: str = Field(default="", description="Component description")
    datasheet: Optional[str] = Field(None, description="Datasheet URL")


class NetConnection(BaseModel):
    """Net connection between component pins"""
    net_name: str = Field(..., description="Net name")
    connections: List[str] = Field(..., description="Pin connections (format: 'U1.1', 'R1.2')")


class CircuitBlock(BaseModel):
    """Logical circuit block (e.g., Power, MCU, Sensor interface)"""
    name: str = Field(..., description="Block name")
    components: List[Component] = Field(default_factory=list)
    nets: List[NetConnection] = Field(default_factory=list)
    notes: str = Field(default="", description="Design notes for this block")


class CircuitGraph(BaseModel):
    """Complete circuit design"""
    intent: HardwareIntent
    blocks: List[CircuitBlock] = Field(default_factory=list)
    global_nets: List[str] = Field(default_factory=list, description="Global nets like GND, VCC")


class PCBLayout(BaseModel):
    """PCB layout information"""
    board_width: float = Field(..., description="Board width in mm")
    board_height: float = Field(..., description="Board height in mm")
    layers: int = Field(default=2)
    components: List[Dict] = Field(default_factory=list, description="Component placements with x,y coords")
