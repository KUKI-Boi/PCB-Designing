"""
KiCad Generator - Generate KiCad schematic and PCB files
Uses S-expression format to create .kicad_sch and .kicad_pcb files
"""
import os
from typing import List, Tuple
from models import CircuitGraph, Component, CircuitBlock


class KiCadGenerator:
    """Generate KiCad schematic and PCB files from CircuitGraph"""
    
    def __init__(self, output_dir: str = "output"):
        """Initialize generator with output directory"""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # S-expression formatting helpers
        self.indent = "  "
    
    def generate_schematic(self, circuit: CircuitGraph, filename: str = "design.kicad_sch") -> str:
        """
        Generate KiCad schematic file
        
        Args:
            circuit: CircuitGraph to convert
            filename: Output filename
            
        Returns:
            Path to generated file
        """
        output_path = os.path.join(self.output_dir, filename)
        
        # Build S-expression
        sch_content = self._build_schematic_sexpr(circuit)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(sch_content)
        
        return output_path
    
    def generate_pcb(self, circuit: CircuitGraph, filename: str = "design.kicad_pcb") -> str:
        """
        Generate KiCad PCB file
        
        Args:
            circuit: CircuitGraph to convert
            filename: Output filename
            
        Returns:
            Path to generated file
        """
        output_path = os.path.join(self.output_dir, filename)
        
        # Build S-expression
        pcb_content = self._build_pcb_sexpr(circuit)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(pcb_content)
        
        return output_path
    
    def _build_schematic_sexpr(self, circuit: CircuitGraph) -> str:
        """Build schematic S-expression"""
        # KiCad 7.0 format
        lines = [
            '(kicad_sch (version 20211123) (generator ai_hardware_designer)',
            '  (uuid "00000000-0000-0000-0000-000000000000")',
            '  (paper "A4")',
            '',
            '  (lib_symbols',
        ]
        
        # Add symbol definitions (simplified - real symbols are more complex)
        symbol_types = set()
        for block in circuit.blocks:
            for comp in block.components:
                symbol_type = self._get_symbol_type(comp.reference)
                symbol_types.add(symbol_type)
        
        for symbol_type in symbol_types:
            lines.append(f'    (symbol "{symbol_type}" (power))')
        
        lines.append('  )')  # Close lib_symbols
        
        # Add symbol instances
        x, y = 50, 50
        for block in circuit.blocks:
            lines.append(f'  ; Block: {block.name}')
            
            for comp in block.components:
                symbol = self._get_symbol_type(comp.reference)
                lines.extend([
                    f'  (symbol (lib_id "{symbol}") (at {x} {y} 0)',
                    f'    (uuid "{self._generate_uuid()}")',
                    f'    (property "Reference" "{comp.reference}" (at {x} {y-5} 0))',
                    f'    (property "Value" "{comp.value}" (at {x} {y+5} 0))',
                    f'    (property "Footprint" "{comp.footprint}" (at {x} {y+10} 0))',
                    f'  )'
                ])
                
                y += 30  # Vertical spacing
                if y > 250:
                    y = 50
                    x += 80  # Next column
        
        lines.append(')')  # Close kicad_sch
        
        return '\n'.join(lines)
    
    def _build_pcb_sexpr(self, circuit: CircuitGraph) -> str:
        """Build PCB S-expression"""
        # Parse board size
        size = circuit.intent.pcb_size.replace('mm', '').split('x')
        width = float(size[0]) if len(size) > 0 else 80
        height = float(size[1]) if len(size) > 1 else 60
        
        lines = [
            '(kicad_pcb (version 20211014) (generator ai_hardware_designer)',
            '',
            '  (general',
            f'    (thickness {1.6 * circuit.intent.layers})',
            '  )',
            '',
            '  (page "A4")',
            '',
            '  (layers',
            '    (0 "F.Cu" signal)',
            '    (31 "B.Cu" signal)',
            '    (32 "B.Adhes" user)',
            '    (33 "F.Adhes" user)',
            '    (34 "B.Paste" user)',
            '    (35 "F.Paste" user)',
            '    (36 "B.SilkS" user)',
            '    (37 "F.SilkS" user)',
            '    (38 "B.Mask" user)',
            '    (39 "F.Mask" user)',
            '    (40 "Dwgs.User" user)',
            '    (44 "Edge.Cuts" user)',
            '  )',
            '',
            '  (setup',
            '    (pad_to_mask_clearance 0)',
            '    (pcbplotparams',
            '      (layerselection 0x00010fc_ffffffff)',
            '      (plot_on_all_layers_selection 0x0000000_00000000)',
            '    )',
            '  )',
            '',
            f'  ; Board outline: {width}x{height}mm',
            '  (gr_rect (start 0 0) (end {0} {1}) (layer "Edge.Cuts") (width 0.1))'.format(width, height),
            '',
        ]
        
        # Place footprints
        x, y = 10.0, 10.0
        for block in circuit.blocks:
            lines.append(f'  ; Block: {block.name}')
            
            for comp in block.components:
                lines.extend([
                    f'  (footprint "{comp.footprint}" (layer "F.Cu")',
                    f'    (at {x} {y})',
                    f'    (property "Reference" "{comp.reference}")',
                    f'    (property "Value" "{comp.value}")',
                    f'  )'
                ])
                
                # Simple grid placement
                x += 15
                if x > width - 10:
                    x = 10
                    y += 15
        
        lines.append(')')  # Close kicad_pcb
        
        return '\n'.join(lines)
    
    def _get_symbol_type(self, reference: str) -> str:
        """Get KiCad symbol type from reference"""
        prefix = reference[0]
        symbol_map = {
            'U': 'Device:C',  # Simplified
            'R': 'Device:R',
            'C': 'Device:C',
            'D': 'Device:D',
            'L': 'Device:L',
            'J': 'Connector:Conn_01x02',
            'K': 'Relay:Relay_SPDT',
            'Q': 'Device:Q_NPN_BCE',
            'SW': 'Switch:SW_Push',
            'Y': 'Device:Crystal'
        }
        return symbol_map.get(prefix, 'Device:R')
    
    def _generate_uuid(self) -> str:
        """Generate UUID for KiCad elements"""
        import uuid
        return str(uuid.uuid4())


# CLI test function
if __name__ == "__main__":
    from intent_parser import IntentParser
    from circuit_designer import CircuitDesigner
    from component_selector import ComponentSelector
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python kicad_generator.py 'your hardware description'")
        sys.exit(1)
    
    # Full pipeline
    parser = IntentParser()
    designer = CircuitDesigner()
    selector = ComponentSelector()
    generator = KiCadGenerator()
    
    prompt = " ".join(sys.argv[1:])
    
    intent = parser.parse(prompt)
    circuit = designer.design(intent)
    circuit = selector.enrich(circuit)
    
    sch_path = generator.generate_schematic(circuit)
    pcb_path = generator.generate_pcb(circuit)
    
    print(f"\nGenerated Files:")
    print(f"  Schematic: {sch_path}")
    print(f"  PCB: {pcb_path}")
