"""
Backend API Server for AI Hardware Designer
Uses FastAPI to expose the hardware design pipeline
"""
import os
import shutil
from typing import Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from intent_parser import IntentParser
from circuit_designer import CircuitDesigner
from component_selector import ComponentSelector
from kicad_generator import KiCadGenerator
from manufacturing import ManufacturingExporter
from models import CircuitGraph

app = FastAPI(title="AI Hardware Designer API")

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Output directory for generated files
OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Serve static files for downloads
app.mount("/downloads", StaticFiles(directory=OUTPUT_DIR), name="downloads")

class GenerateRequest(BaseModel):
    prompt: str
    project_name: str = "design"

class GenerateResponse(BaseModel):
    status: str
    message: str
    circuit: Optional[CircuitGraph] = None
    files: dict = {}

def run_pipeline(prompt: str, project_name: str):
    """Run the hardware design pipeline"""
    try:
        # 1. Parse Intent
        intent_parser = IntentParser()
        intent = intent_parser.parse(prompt)
        
        # 2. Design Circuit
        circuit_designer = CircuitDesigner()
        circuit = circuit_designer.design(intent)
        
        # 3. Select Components
        component_selector = ComponentSelector()
        circuit = component_selector.enrich(circuit)
        
        # 4. Generate KiCad Files
        kicad_generator = KiCadGenerator(output_dir=OUTPUT_DIR)
        sch_path = kicad_generator.generate_schematic(circuit, f"{project_name}.kicad_sch")
        pcb_path = kicad_generator.generate_pcb(circuit, f"{project_name}.kicad_pcb")
        
        # 5. Export Manufacturing Files
        mfg_exporter = ManufacturingExporter(output_dir=OUTPUT_DIR)
        bom_path = mfg_exporter.export_bom(circuit, f"{project_name}_BOM.csv")
        pnp_path = mfg_exporter.export_pick_and_place(circuit, f"{project_name}_PickAndPlace.csv")
        
        return circuit, {
            "schematic": sch_path,
            "pcb": pcb_path,
            "bom": bom_path,
            "pnp": pnp_path
        }
    except Exception as e:
        print(f"Pipeline error: {e}")
        raise e

@app.post("/generate", response_model=GenerateResponse)
async def generate_hardware(request: GenerateRequest):
    """Trigger the hardware design pipeline"""
    if not request.prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
    
    try:
        circuit, files = run_pipeline(request.prompt, request.project_name)
        
        return GenerateResponse(
            status="success",
            message="Hardware design generated successfully",
            circuit=circuit,
            files={k: f"/downloads/{os.path.basename(v)}" for k, v in files.items()}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
