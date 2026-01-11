"""
AI Hardware Designer - Main CLI Entry Point
Complete pipeline from text to manufacturing files
"""
import sys
import argparse
from intent_parser import IntentParser
from circuit_designer import CircuitDesigner
from component_selector import ComponentSelector
from kicad_generator import KiCadGenerator
from manufacturing import ManufacturingExporter


def main():
    """Main entry point for AI Hardware Designer"""
    parser = argparse.ArgumentParser(
        description='AI Hardware Designer - Convert text to PCB designs',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python main.py "ESP32 based smart irrigation controller with soil sensor and relay"
  python main.py "Arduino temperature logger with DHT22 and SD card"
  python main.py -o my_design "STM32 motor controller with H-bridge"
        '''
    )
    
    parser.add_argument(
        'description',
        type=str,
        help='Natural language hardware description'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default='output',
        help='Output directory (default: output)'
    )
    
    parser.add_argument(
        '--name',
        type=str,
        default='design',
        help='Project name (default: design)'
    )
    
    parser.add_argument(
        '--skip-gerbers',
        action='store_true',
        help='Skip Gerber generation'
    )
    
    args = parser.parse_args()
    
    print("=" * 70)
    print("AI Hardware Designer")
    print("=" * 70)
    print(f"\nInput: {args.description}\n")
    
    # Initialize pipeline
    intent_parser = IntentParser()
    circuit_designer = CircuitDesigner()
    component_selector = ComponentSelector()
    kicad_generator = KiCadGenerator(output_dir=args.output)
    manufacturing_exporter = ManufacturingExporter(output_dir=args.output)
    
    # Step 1: Parse Intent
    print("Step 1: Parsing Hardware Intent...")
    intent = intent_parser.parse(args.description)
    print(f"  ✓ Application: {intent.application}")
    print(f"  ✓ MCU: {intent.mcu}")
    print(f"  ✓ Sensors: {', '.join(intent.sensors) if intent.sensors else 'None'}")
    print(f"  ✓ Outputs: {', '.join(intent.outputs) if intent.outputs else 'None'}")
    print(f"  ✓ Power: {intent.power_input}")
    print()
    
    # Step 2: Design Circuit
    print("Step 2: Designing Circuit Architecture...")
    circuit = circuit_designer.design(intent)
    print(f"  ✓ Created {len(circuit.blocks)} circuit blocks")
    total_components = sum(len(block.components) for block in circuit.blocks)
    print(f"  ✓ Total components: {total_components}")
    print()
    
    # Step 3: Select Components
    print("Step 3: Selecting Real Components...")
    circuit = component_selector.enrich(circuit)
    mpn_count = sum(1 for block in circuit.blocks for comp in block.components if comp.mpn)
    print(f"  ✓ Enriched {mpn_count} components with MPNs")
    print()
    
    # Step 4: Generate KiCad Files
    print("Step 4: Generating KiCad Files...")
    sch_file = f"{args.name}.kicad_sch"
    pcb_file = f"{args.name}.kicad_pcb"
    
    sch_path = kicad_generator.generate_schematic(circuit, sch_file)
    pcb_path = kicad_generator.generate_pcb(circuit, pcb_file)
    print(f"  ✓ Schematic: {sch_path}")
    print(f"  ✓ PCB: {pcb_path}")
    print()
    
    # Step 5: Export Manufacturing Files
    print("Step 5: Exporting Manufacturing Files...")
    bom_path = manufacturing_exporter.export_bom(circuit, f"{args.name}_BOM.csv")
    pnp_path = manufacturing_exporter.export_pick_and_place(circuit, f"{args.name}_PickAndPlace.csv")
    print(f"  ✓ BOM: {bom_path}")
    print(f"  ✓ Pick-and-Place: {pnp_path}")
    
    if not args.skip_gerbers:
        gerber_dir = manufacturing_exporter.generate_gerbers(circuit)
        print(f"  ✓ Gerbers: {gerber_dir}")
    
    print()
    print("=" * 70)
    print("✓ DESIGN COMPLETE")
    print("=" * 70)
    print(f"\nAll files saved to: {args.output}/")
    print("\nNext Steps:")
    print(f"  1. Open {sch_path} in KiCad Schematic Editor")
    print(f"  2. Open {pcb_path} in KiCad PCB Editor")
    print("  3. Run DRC/ERC checks")
    print("  4. Manually route critical signals if needed")
    print(f"  5. Review {bom_path} for component sourcing")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
