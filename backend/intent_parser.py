"""
Intent Parser - Natural Language to Hardware Specification
Uses LLM to convert user prompts into structured HardwareIntent
"""
import os
import json
from typing import Dict
from openai import OpenAI
from dotenv import load_dotenv
from models import HardwareIntent

# Load environment variables
load_dotenv()


class IntentParser:
    """Parse natural language hardware descriptions into structured format"""
    
    def __init__(self, demo_mode: bool = False):
        """Initialize the LLM client"""
        self.demo_mode = demo_mode or os.getenv("DEMO_MODE", "false").lower() == "true"
        
        if self.demo_mode:
            print("[DEMO MODE] Using pre-configured responses instead of API calls")
            self.client = None
            self.model = None
            return
        
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY not found in environment")
        
        # OpenRouter uses OpenAI-compatible API
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        
        # Use free tier model on OpenRouter
        # Options: qwen/qvq-72b-preview, meta-llama/llama-3.2-3b-instruct:free
        self.model = "qwen/qvq-72b-preview"
    
    def parse(self, user_prompt: str) -> HardwareIntent:
        """
        Parse user prompt into HardwareIntent structure
        
        Args:
            user_prompt: Natural language hardware description
            
        Returns:
            HardwareIntent object with structured requirements
        """
        # Demo mode bypass
        if self.demo_mode:
            return self._get_demo_intent(user_prompt)
        
        system_prompt = self._build_system_prompt()
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,  # Lower temperature for more consistent parsing
            max_tokens=2000
        )
        
        # Extract JSON from response
        content = response.choices[0].message.content
        
        # Parse JSON and validate with Pydantic
        try:
            # Try to extract JSON from markdown code blocks if present
            if "```json" in content:
                json_str = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                json_str = content.split("```")[1].split("```")[0].strip()
            else:
                json_str = content.strip()
            
            intent_data = json.loads(json_str)
            return HardwareIntent(**intent_data)
        except Exception as e:
            raise ValueError(f"Failed to parse LLM response: {e}\nResponse: {content}")
    
    def _build_system_prompt(self) -> str:
        """Build the system prompt for hardware intent parsing"""
        return """You are an expert hardware design AI. Your task is to parse natural language hardware descriptions into structured JSON.

Given a user's hardware idea, extract:
1. Application purpose
2. Microcontroller (if mentioned or implied - default to ESP32 for IoT, Arduino-style projects)
3. Sensors needed
4. Output devices (relays, motors, LEDs, displays)
5. Input devices (buttons, switches)
6. Communication requirements (WiFi, Bluetooth, UART, I2C, SPI)
7. Power requirements (input voltage, battery vs adapter)
8. PCB constraints (size if mentioned)

IMPORTANT RULES:
- If MCU not specified but WiFi/IoT mentioned → use ESP32
- If simple Arduino project → use ATmega328P
- If sensors mention temperature/humidity → use DHT22 or similar
- If "relay" mentioned → assume 5V relay with driver
- Always include decoupling capacitors requirement
- Default to 2-layer PCB, 80x60mm if not specified
- Infer missing components based on common practices

OUTPUT FORMAT: Return ONLY valid JSON matching this schema:
{
  "application": "string",
  "mcu": "string or null",
  "sensors": ["string"],
  "outputs": ["string"],
  "inputs": ["string"],
  "communication": ["string"],
  "power_input": "string",
  "power_output_voltage": "string or null",
  "pcb_size": "string",
  "layers": number,
  "additional_notes": "string"
}

Example input: "ESP32 based smart irrigation controller with soil sensor and relay"
Example output:
{
  "application": "smart irrigation controller",
  "mcu": "ESP32",
  "sensors": ["soil moisture sensor"],
  "outputs": ["relay"],
  "inputs": [],
  "communication": ["WiFi"],
  "power_input": "12V DC adapter",
  "power_output_voltage": "3.3V",
  "pcb_size": "80x60mm",
  "layers": 2,
  "additional_notes": "Requires relay driver circuit, voltage regulation from 12V to 3.3V for ESP32"
}

Respond with ONLY the JSON, no other text."""
    
    def _get_demo_intent(self, user_prompt: str) -> HardwareIntent:
        """Return demo intent for testing without API calls"""
        prompt_lower = user_prompt.lower()
        
        # Match common patterns
        if "esp32" in prompt_lower and "relay" in prompt_lower:
            return HardwareIntent(
                application="smart irrigation controller",
                mcu="ESP32",
                sensors=["soil moisture sensor"],
                outputs=["relay"],
                inputs=[],
                communication=["WiFi"],
                power_input="12V DC adapter",
                power_output_voltage="3.3V",
                pcb_size="80x60mm",
                layers=2,
                additional_notes="Requires relay driver circuit, voltage regulation from 12V to 3.3V for ESP32"
            )
        elif "dht22" in prompt_lower or "temperature" in prompt_lower:
            return HardwareIntent(
                application="temperature and humidity logger",
                mcu="ATmega328P",
                sensors=["DHT22"],
                outputs=["LED"],
                inputs=[],
                communication=[],
                power_input="5V USB",
                power_output_voltage="5V",
                pcb_size="60x40mm",
                layers=2,
                additional_notes="Simple temperature logging with DHT22 sensor"
            )
        else:
            # Generic ESP32 project
            return HardwareIntent(
                application="IoT device",
                mcu="ESP32",
                sensors=[],
                outputs=["LED"],
                inputs=["button"],
                communication=["WiFi"],
                power_input="5V USB",
                power_output_voltage="3.3V",
                pcb_size="80x60mm",
                layers=2,
                additional_notes="Generic ESP32 IoT device with WiFi connectivity"
            )


# CLI test function
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python intent_parser.py 'your hardware description'")
        sys.exit(1)
    
    parser = IntentParser()
    prompt = " ".join(sys.argv[1:])
    
    print(f"Parsing: {prompt}\n")
    intent = parser.parse(prompt)
    print("\nParsed Intent:")
    print(intent.model_dump_json(indent=2))
