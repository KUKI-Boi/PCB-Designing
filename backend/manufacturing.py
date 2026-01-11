"""
Manufacturing - Generate BOM and Gerber files
"""
import os
import csv
from typing import List
from models import CircuitGraph, Component


class ManufacturingExporter:
    """Export manufacturing files (BOM, Pick-and-Place, Gerbers)"""
    
    def __init__(self, output_dir: str = "output"):
        """Initialize exporter with output directory"""
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def export_bom(self, circuit: CircuitGraph, filename: str = "BOM.csv") -> str:
        """
        Export Bill of Materials as CSV
        
        Args:
            circuit: CircuitGraph with components
            filename: Output filename
            
        Returns:
            Path to BOM file
        """
        output_path = os.path.join(self.output_dir, filename)
        
        # Collect all components
        all_components: List[Component] = []
        for block in circuit.blocks:
            all_components.extend(block.components)
        
        # Group by value and footprint
        bom_items = self._group_components(all_components)
        
        # Write CSV
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'Item',
                'Qty',
                'References',
                'Value',
                'Footprint',
                'MPN',
                'Description',
                'Datasheet'
            ])
            
            # Data rows
            for idx, item in enumerate(bom_items, 1):
                writer.writerow([
                    idx,
                    item['qty'],
                    ', '.join(item['references']),
                    item['value'],
                    item['footprint'],
                    item['mpn'] or 'N/A',
                    item['description'],
                    item['datasheet'] or 'N/A'
                ])
        
        return output_path
    
    def export_pick_and_place(self, circuit: CircuitGraph, filename: str = "PickAndPlace.csv") -> str:
        """
        Export Pick-and-Place file for assembly
        
        Args:
            circuit: CircuitGraph with components
            filename: Output filename
            
        Returns:
            Path to P&P file
        """
        output_path = os.path.join(self.output_dir, filename)
        
        # Collect all components with positions (simplified - uses grid)
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header (standard P&P format)
            writer.writerow([
                'Designator',
                'Footprint',
                'Mid X',
                'Mid Y',
                'Rotation',
                'Layer',
                'Value',
                'MPN'
            ])
            
            # Simple grid placement
            x, y = 10.0, 10.0
            for block in circuit.blocks:
                for comp in block.components:
                    writer.writerow([
                        comp.reference,
                        comp.footprint,
                        f"{x:.2f}mm",
                        f"{y:.2f}mm",
                        "0",
                        "Top",
                        comp.value,
                        comp.mpn or 'N/A'
                    ])
                    
                    # Grid placement (same as PCB generator)
                    x += 15
                    if x > 70:
                        x = 10
                        y += 15
        
        return output_path
    
    def generate_gerbers(self, circuit: CircuitGraph) -> str:
        """
        Generate Gerber files using KiCad CLI
        Note: Requires KiCad to be installed
        
        Args:
            circuit: CircuitGraph
            
        Returns:
            Path to gerber directory
        """
        gerber_dir = os.path.join(self.output_dir, "gerbers")
        os.makedirs(gerber_dir, exist_ok=True)
        
        pcb_file = os.path.join(self.output_dir, "design.kicad_pcb")
        
        if not os.path.exists(pcb_file):
            raise FileNotFoundError(f"PCB file not found: {pcb_file}")
        
        # This would call kicad-cli to plot gerbers
        # For MVP, we create a placeholder
        readme_path = os.path.join(gerber_dir, "README.txt")
        with open(readme_path, 'w') as f:
            f.write("Gerber files would be generated here using:\n")
            f.write(f"kicad-cli pcb export gerbers {pcb_file} -o {gerber_dir}\n")
            f.write("\nLayers to plot:\n")
            f.write("  - F.Cu (Top Copper)\n")
            f.write("  - B.Cu (Bottom Copper)\n")
            f.write("  - F.SilkS (Top Silkscreen)\n")
            f.write("  - B.SilkS (Bottom Silkscreen)\n")
            f.write("  - F.Mask (Top Soldermask)\n")
            f.write("  - B.Mask (Bottom Soldermask)\n")
            f.write("  - Edge.Cuts (Board Outline)\n")
            f.write("  - F.Paste (Top Paste)\n")
            f.write("  - B.Paste (Bottom Paste)\n")
        
        return gerber_dir
    
    def _group_components(self, components: List[Component]) -> List[dict]:
        """Group components by value and footprint for BOM"""
        grouped = {}
        
        for comp in components:
            key = (comp.value, comp.footprint)
            
            if key not in grouped:
                grouped[key] = {
                    'value': comp.value,
                    'footprint': comp.footprint,
                    'mpn': comp.mpn,
                    'description': comp.description,
                    'datasheet': comp.datasheet,
                    'references': [],
                    'qty': 0
                }
            
            grouped[key]['references'].append(comp.reference)
            grouped[key]['qty'] += 1
        
        # Convert to list and sort by reference
        items = list(grouped.values())
        items.sort(key=lambda x: x['references'][0])
        
        return items


# CLI test function
if __name__ == "__main__":
    from intent_parser import IntentParser
    from circuit_designer import CircuitDesigner
    from component_selector import ComponentSelector
    from kicad_generator import KiCadGenerator
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python manufacturing.py 'your hardware description'")
        sys.exit(1)
    
    # Full pipeline
    parser = IntentParser()
    designer = CircuitDesigner()
    selector = ComponentSelector()
    generator = KiCadGenerator()
    exporter = ManufacturingExporter()
    
    prompt = " ".join(sys.argv[1:])
    
    intent = parser.parse(prompt)
    circuit = designer.design(intent)
    circuit = selector.enrich(circuit)
    
    # Generate KiCad files first
    generator.generate_schematic(circuit)
    generator.generate_pcb(circuit)
    
    # Export manufacturing files
    bom_path = exporter.export_bom(circuit)
    pnp_path = exporter.export_pick_and_place(circuit)
    gerber_dir = exporter.generate_gerbers(circuit)
    
    print(f"\nManufacturing Files:")
    print(f"  BOM: {bom_path}")
    print(f"  Pick-and-Place: {pnp_path}")
    print(f"  Gerbers: {gerber_dir}")
