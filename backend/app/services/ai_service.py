import json
import logging
import requests
from typing import Dict, Any, List
from app.config import settings
from app.models.material import RecommendationReport, MaterialItem, CostOptimizationTip

logger = logging.getLogger("ai_service")

USD_TO_INR = 86.5

def format_inr(usd_val: float) -> float:
    return round(usd_val * USD_TO_INR, 2)

# Engineering Database with Low-Budget Cost Effective Materials
PRESET_ENGINEERING_DATA: Dict[str, Dict[str, Any]] = {
    "hydraulic lift": {
        "project_name": "Hydraulic Lift",
        "category": "Fluid Power & Material Handling",
        "project_summary": "Cost-effective scissor lifting platform optimized with commercial grade IS 2062 mild steel profiles, standard hydraulic cylinders, and self-lubricating polymer bushings.",
        "operating_environment": "Industrial Workshop / High Load",
        "materials": [
            {
                "item_name": "Structural Scissor Arms",
                "grade": "IS 2062 Grade E250 ERW Rectangular Hollow Section",
                "dimensions": "100mm x 50mm x 4.5mm Wall, 1500mm Length",
                "quantity": "4 pieces",
                "purpose": "Primary scissor linkage transferring hydraulic thrust into vertical lifting motion",
                "alternatives": ["ASTM A36 Steel", "Structural Angle Channel"],
                "low_budget_option": "ERW Mild Steel RHS (E250) - 35% cheaper than seamless ST52 tubes",
                "unit_cost_usd": 68.0,
                "total_cost_usd": 272.0,
                "unit_cost_inr": format_inr(68.0),
                "total_cost_inr": format_inr(272.0),
                "cost_note": "₹5,882 / profile section using commercial ERW mild steel"
            },
            {
                "item_name": "Hydraulic Cylinder & CK45 Chrome Rod",
                "grade": "Standard Agricultural ISO 6020 Hydraulic Cylinder",
                "dimensions": "Bore 70mm, Rod 40mm, Stroke 500mm",
                "quantity": "2 units",
                "purpose": "Converts 160 Bar hydraulic pressure into linear lifting force",
                "alternatives": ["Custom Heavy Honed Cylinder"],
                "low_budget_option": "Standard Off-the-Shelf Agricultural Cylinder - Saves 45% vs custom CNC cylinder",
                "unit_cost_usd": 180.0,
                "total_cost_usd": 360.0,
                "unit_cost_inr": format_inr(180.0),
                "total_cost_inr": format_inr(360.0),
                "cost_note": "₹15,570 / mass-produced off-the-shelf cylinder unit"
            },
            {
                "item_name": "Pivot Pins & Self-Lubricating Bushings",
                "grade": "EN8 (080M40) Medium Carbon Steel Pins + Igus Polymer Bushes",
                "dimensions": "Pin Dia 30mm x 160mm; Bush 30mm ID",
                "quantity": "8 sets",
                "purpose": "Rotational pivot joints connecting scissor arms to base guide tracks",
                "alternatives": ["AISI 4140 Hardened Chrome-Moly"],
                "low_budget_option": "EN8 turned pins with Igutex self-lubricating polymer bushes (eliminates grease nipples)",
                "unit_cost_usd": 18.0,
                "total_cost_usd": 144.0,
                "unit_cost_inr": format_inr(18.0),
                "total_cost_inr": format_inr(144.0),
                "cost_note": "₹1,557 / turned EN8 pin & engineering polymer bush set"
            },
            {
                "item_name": "Base Channel Frame & Top Deck Plate",
                "grade": "ISMC 100 Structural Steel Channel & 4mm Mild Steel Sheet",
                "dimensions": "Frame: 1800x900mm; Plate 4mm thickness",
                "quantity": "1 assembly",
                "purpose": "Provides rigid structural base and load platform",
                "alternatives": ["ASTM A36 Heavy Channel"],
                "low_budget_option": "ISMC 100 Channel frame with stiffener ribs - Reduces plate thickness from 6mm to 4mm",
                "unit_cost_usd": 240.0,
                "total_cost_usd": 240.0,
                "unit_cost_inr": format_inr(240.0),
                "total_cost_inr": format_inr(240.0),
                "cost_note": "₹20,760 / ISMC channel steel frame & stiffened sheet deck"
            },
            {
                "item_name": "Hydraulic Power Pack Unit",
                "grade": "2.2kW Single-Phase Motor & 160 Bar Gear Pump",
                "dimensions": "15-Liter Reservoir, 3.5 L/min flow",
                "quantity": "1 complete unit",
                "purpose": "Generates hydraulic fluid pressure for cylinder actuation",
                "alternatives": ["3kW 3-Phase Industrial Pack"],
                "low_budget_option": "2.2kW single-phase compact AC power pack - Saves ₹18,000 in electrical wiring",
                "unit_cost_usd": 380.0,
                "total_cost_usd": 380.0,
                "unit_cost_inr": format_inr(380.0),
                "total_cost_inr": format_inr(380.0),
                "cost_note": "₹32,870 / compact single-phase hydraulic power pack"
            }
        ],
        "tools_and_equipment": [
            "MIG Welder (180A-200A Single Phase)",
            "Angle Grinder with Cutting & Grinding Wheels",
            "Bench Drill Press",
            "Vernier Caliper & Hand Wrench Set"
        ],
        "manufacturing_processes": [
            "Manual Abrasive Saw Profile Cutting",
            "MIG Joint Welding (ER70S-6 wire)",
            "Drilling & Reaming of Pivot Holes",
            "Anti-Rust Primer & Epoxy Paint Spraying"
        ],
        "safety_precautions": [
            "Install mechanical safety lock pin before working under platform",
            "Equip hydraulic flow restrictor valve on cylinder outlet port",
            "Apply anti-slip tape on top deck surface"
        ],
        "assembly_procedure": [
            "Step 1: Cut ISMC channel frame members to length and tack-weld base rectangle.",
            "Step 2: Drill scissor arm pivot holes using a drilling template to ensure alignment.",
            "Step 3: Press Igus polymer bushes into arm pivot eyes.",
            "Step 4: Connect scissor arm links to base guide channels with EN8 pins.",
            "Step 5: Mount hydraulic cylinders and connect flexible hoses to power pack."
        ],
        "raw_material_subtotal_usd": 1396.0,
        "estimated_machining_and_labor_usd": 190.0,
        "total_estimated_cost_usd": 1586.0,
        "raw_material_subtotal_inr": format_inr(1396.0),
        "estimated_machining_and_labor_inr": format_inr(190.0),
        "total_estimated_cost_inr": format_inr(1586.0),
        "cost_saving_strategies": [
            {"category": "Structural Steel", "tip": "Use commercial IS 2062 ERW hollow sections instead of seamless alloy tubing to save ~35%.", "estimated_savings_inr": 15000.0},
            {"category": "Hydraulics", "tip": "Select standard off-the-shelf agricultural hydraulic cylinders rather than custom bored cylinders to save ~45%.", "estimated_savings_inr": 28000.0},
            {"category": "Bushings", "tip": "Use self-lubricating Igus engineering polymer bushings to eliminate expensive greasing manifolds and bronze machining.", "estimated_savings_inr": 8500.0}
        ],
        "key_design_considerations": [
            "Load distribution across stiffened 4mm top deck plate",
            "Pin shear stress analysis on EN8 pivot shafts",
            "Buckling resistance of 70mm bore hydraulic cylinder"
        ]
    },
    "robotic arm": {
        "project_name": "Robotic Arm",
        "category": "Mechatronics & Robotics",
        "project_summary": "Ultra cost-effective 6-Axis robotic arm constructed using 3D-printed PETG/PLA arm joints, NEMA 17/23 stepper motors with 10:1 planetary gearboxes, and open-source Arduino/ESP32 controllers.",
        "operating_environment": "Educational / Prototyping Workshop",
        "materials": [
            {
                "item_name": "3D-Printed Arm Links & Base Structural Housings",
                "grade": "PETG (Polyethylene Terephthalate Glycol) High Infill",
                "dimensions": "4mm Wall, 50% Gyroid Infill",
                "quantity": "6 links (2.5 kg filament)",
                "purpose": "Lightweight structural arm segments printed on FDM 3D printer",
                "alternatives": ["CNC Aluminum 6061"],
                "low_budget_option": "3D printed PETG filament - Saves 80% cost compared to 5-axis CNC aluminum machining",
                "unit_cost_usd": 30.0,
                "total_cost_usd": 75.0,
                "unit_cost_inr": format_inr(30.0),
                "total_cost_inr": format_inr(75.0),
                "cost_note": "₹6,487 / 2.5 kg PETG filament spool total for all 6 arm links"
            },
            {
                "item_name": "High-Torque Stepper Motors & Planetary Gearboxes",
                "grade": "NEMA 17 / NEMA 23 Stepper Motors + 10:1 Epicyclic Planetary Gearboxes",
                "dimensions": "Holding Torque 1.2 Nm to 3.0 Nm",
                "quantity": "6 units",
                "purpose": "Actuates arm joints with high precision and low backlash",
                "alternatives": ["Harmonic Drive Speed Reducers"],
                "low_budget_option": "NEMA Stepper motors with planetary gearboxes - Saves 85% compared to harmonic drive reducers",
                "unit_cost_usd": 45.0,
                "total_cost_usd": 270.0,
                "unit_cost_inr": format_inr(45.0),
                "total_cost_inr": format_inr(270.0),
                "cost_note": "₹23,355 / 6 stepper motors with gearboxes"
            },
            {
                "item_name": "Closed-Loop Encoder Drivers & ESP32 Controller Board",
                "grade": "TMC2209 Silent Stepper Drivers + ESP32 32-bit Microcontroller",
                "dimensions": "Dual Core 240MHz microcontroller",
                "quantity": "1 kit",
                "purpose": "Provides quiet step execution and kinematics calculation",
                "alternatives": ["Industrial CANopen Servo Drives"],
                "low_budget_option": "ESP32 micro-controller with TMC2209 drivers - Cost effective open-source electronics",
                "unit_cost_usd": 40.0,
                "total_cost_usd": 40.0,
                "unit_cost_inr": format_inr(40.0),
                "total_cost_inr": format_inr(40.0),
                "cost_note": "₹3,460 / ESP32 development board & TMC2209 driver shield"
            },
            {
                "item_name": "Servo Gripper End Effector",
                "grade": "SG90 Micro Servo + 3D Printed Parallel Jaws",
                "dimensions": "50mm Stroke Gripper",
                "quantity": "1 unit",
                "purpose": "Lightweight grasping mechanism",
                "alternatives": ["Pneumatic Gripper Assembly"],
                "low_budget_option": "3D printed gripper with SG90 micro servo - Costs under ₹600",
                "unit_cost_usd": 12.0,
                "total_cost_usd": 12.0,
                "unit_cost_inr": format_inr(12.0),
                "total_cost_inr": format_inr(12.0),
                "cost_note": "₹1,038 / printed gripper mechanism & servo motor"
            }
        ],
        "tools_and_equipment": [
            "FDM 3D Printer (Ender 3 / Bambu Lab)",
            "Precision Hex Key Driver Set",
            "Soldering Iron & Wire Stripper"
        ],
        "manufacturing_processes": [
            "FDM 3D Printing with PETG filament",
            "Threaded Brass Insert Heat-Pressing",
            "Modular Joint Snap Assembly"
        ],
        "safety_precautions": [
            "Limit joint motor current to prevent excessive squeeze force",
            "Provide emergency stop button on main power DC bus"
        ],
        "assembly_procedure": [
            "Step 1: 3D print arm joint links using 50% gyroid infill for optimal rigidity.",
            "Step 2: Melt brass M3 threaded inserts into printed link mounting bosses.",
            "Step 3: Bolt NEMA stepper motors to joint gearboxes.",
            "Step 4: Route wiring through hollow printed link arm channels.",
            "Step 5: Flash ESP32 inverse kinematics firmware and perform home axis calibration."
        ],
        "raw_material_subtotal_usd": 397.0,
        "estimated_machining_and_labor_usd": 45.0,
        "total_estimated_cost_usd": 442.0,
        "raw_material_subtotal_inr": format_inr(397.0),
        "estimated_machining_and_labor_inr": format_inr(45.0),
        "total_estimated_cost_inr": format_inr(442.0),
        "cost_saving_strategies": [
            {"category": "Structural Arm", "tip": "Use FDM 3D printed PETG with heat-set brass inserts instead of 5-axis CNC aluminum to save >80%.", "estimated_savings_inr": 85000.0},
            {"category": "Gearbox", "tip": "Replace expensive harmonic strain-wave gearing with 10:1 NEMA planetary gearboxes to save ~85%.", "estimated_savings_inr": 115000.0}
        ],
        "key_design_considerations": [
            "Infill density vs flexural strength in printed PETG joint arms",
            "Heat dissipation from stepper motors into printed plastic mounts"
        ]
    }
}

def generate_recommendation(project_name: str, environment: str = "Standard", budget_level: str = "Standard") -> RecommendationReport:
    """Generates full recommendation report with low-budget options and cost savings strategies."""
    clean_name = project_name.strip().lower()
    is_low_budget = "economy" in budget_level.lower() or "low" in budget_level.lower() or "cheap" in budget_level.lower()

    if settings.GEMINI_API_KEY:
        try:
            logger.info("Calling Gemini API for low budget cost-effective recommendation...")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
            prompt = f"""
You are a Senior Mechanical & Materials Engineer. Provide a COST-EFFECTIVE LOW-BUDGET material pricing in Indian Rupees (INR ₹) for: "{project_name}".
Operating Environment: {environment}
Target Budget Level: Low Budget / Economy Cost Effective

Return a valid JSON object matching this schema EXACTLY without markdown wrappers:
{{
    "project_name": "{project_name}",
    "project_summary": "A 2-sentence cost-effective engineering breakdown.",
    "category": "Engineering Sub-domain",
    "operating_environment": "{environment}",
    "materials": [
        {{
            "item_name": "Cost-effective material component name",
            "grade": "Commercial standard grade (e.g. IS 2062, ERW steel, PETG)",
            "dimensions": "Sizing or thickness",
            "quantity": "Quantity required",
            "purpose": "Engineering function",
            "alternatives": ["Alternative 1"],
            "low_budget_option": "Specific low cost substitute note",
            "unit_cost_inr": 3500.0,
            "total_cost_inr": 10500.0,
            "unit_cost_usd": 40.0,
            "total_cost_usd": 120.0,
            "cost_note": "Cost-effective supplier note in INR"
        }}
    ],
    "tools_and_equipment": ["Tool 1", "Tool 2"],
    "manufacturing_processes": ["Process 1", "Process 2"],
    "safety_precautions": ["Precaution 1"],
    "assembly_procedure": ["Step 1: ...", "Step 2: ..."],
    "raw_material_subtotal_inr": 10500.0,
    "estimated_machining_and_labor_inr": 1800.0,
    "total_estimated_cost_inr": 12300.0,
    "raw_material_subtotal_usd": 120.0,
    "estimated_machining_and_labor_usd": 20.0,
    "total_estimated_cost_usd": 140.0,
    "cost_saving_strategies": [
        {{"category": "Material", "tip": "Use commercial IS 2062 steel profiles", "estimated_savings_inr": 8000.0}}
    ],
    "key_design_considerations": ["Consideration 1"]
}}
"""
            resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=20)
            if resp.status_code == 200:
                text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0].strip()
                elif "```" in text:
                    text = text.split("```")[1].split("```")[0].strip()
                parsed = json.loads(text)
                return RecommendationReport(**parsed)
        except Exception as e:
            logger.error(f"Gemini API call error: {e}")

    for key in PRESET_ENGINEERING_DATA:
        if key in clean_name or clean_name in key:
            return RecommendationReport(**PRESET_ENGINEERING_DATA[key])

    title = project_name.strip().title()
    items = [
        MaterialItem(
            item_name=f"{title} Main Structural Frame",
            grade="IS 2062 Mild Steel Angle & Hollow Section (ERW)",
            dimensions="40mm x 40mm x 3mm Angle Iron, 2000mm Length",
            quantity="6 bars",
            purpose="Rigid low-cost structural frame structure.",
            alternatives=["Commercial Steel Tubing"],
            low_budget_option="IS 2062 Angle Iron - Saves 45% compared to seamless alloy tubing",
            unit_cost_usd=22.0,
            total_cost_usd=132.0,
            unit_cost_inr=format_inr(22.0),
            total_cost_inr=format_inr(132.0),
            cost_note="₹1,903 / 2-meter commercial mild steel angle iron"
        ),
        MaterialItem(
            item_name="Drive Shaft & Power Transmission",
            grade="EN8 (080M40) Cold Drawn Carbon Steel Rod",
            dimensions="Diameter 20mm Shaft, 1000mm Length",
            quantity="2 shafts",
            purpose="Transmits mechanical torque across primary drive axes.",
            alternatives=["AISI 1045 Precision Ground Shaft"],
            low_budget_option="EN8 cold drawn bar stock - Saves 35% compared to ground alloy shafts",
            unit_cost_usd=32.0,
            total_cost_usd=64.0,
            unit_cost_inr=format_inr(32.0),
            total_cost_inr=format_inr(64.0),
            cost_note="₹2,768 / 1-meter cold drawn EN8 steel shaft"
        ),
        MaterialItem(
            item_name="Pillow Block Bushings (UC204)",
            grade="Cast Iron Housing with Rubber Sealed Insert Bearings",
            dimensions="20mm Shaft Bore",
            quantity="4 units",
            purpose="Smooth rotational support for main shafting.",
            alternatives=["Bronze Bushing"],
            low_budget_option="Standard UC204 pillow blocks - Saves 40% vs custom flange units",
            unit_cost_usd=10.0,
            total_cost_usd=40.0,
            unit_cost_inr=format_inr(10.0),
            total_cost_inr=format_inr(40.0),
            cost_note="₹865 / mounted bearing block"
        ),
        MaterialItem(
            item_name="Fasteners & Mounting Hardware Kit",
            grade="Commercial Grade 4.8 Galvanized Hex Bolts & Nuts",
            dimensions="M8 x 35mm Hex Head Bolts",
            quantity="1 kit (100 fasteners)",
            purpose="Secures frame members and mounting brackets.",
            alternatives=["Stainless Steel A2 Fasteners"],
            low_budget_option="Commercial galvanized grade 4.8 bolts - Saves 50% vs stainless hardware",
            unit_cost_usd=15.0,
            total_cost_usd=15.0,
            unit_cost_inr=format_inr(15.0),
            total_cost_inr=format_inr(15.0),
            cost_note="₹1,298 / 100-piece galvanized bolt kit"
        )
    ]
    raw_subtotal_usd = sum(i.total_cost_usd for i in items)
    labor_usd = round(raw_subtotal_usd * 0.15, 2)
    grand_usd = round(raw_subtotal_usd + labor_usd, 2)

    tips = [
        CostOptimizationTip(category="Structural Framing", tip="Substitute heavy alloy profiles with standard IS 2062 angle iron or ERW hollow tubing to cut raw metal costs by 45%.", estimated_savings_inr=12000.0),
        CostOptimizationTip(category="Fasteners & Hardware", tip="Use commercial galvanized grade 4.8 fasteners instead of stainless steel grade A4 fasteners.", estimated_savings_inr=4500.0),
        CostOptimizationTip(category="Transmission", tip="Opt for standard off-the-shelf EN8 cold drawn shafting instead of precision ground 4140 alloy steel.", estimated_savings_inr=8500.0)
    ]

    return RecommendationReport(
        project_name=title,
        category="Cost-Effective Mechanical Fabrication",
        project_summary=f"Ultra low-budget, cost-effective mechanical material specification tailored for {title} using commercial IS standards and off-the-shelf hardware.",
        operating_environment=environment,
        materials=items,
        tools_and_equipment=[
            "Standard Arc / MIG Welder",
            "Angle Grinder & Cut-Off Discs",
            "Hand Drill & Drill Bit Set",
            "Wrench & Caliper Set"
        ],
        manufacturing_processes=[
            "Manual Hack Saw / Abrasive Cutting",
            "Arc / MIG Joint Welding",
            "Hand Drilling & Deburring",
            "Anti-Rust Primer Coating"
        ],
        safety_precautions=[
            "Enforce 2.0:1 minimum safety factor on structural yield stress",
            "De-burr all cut metal edges prior to assembly"
        ],
        assembly_procedure=[
            "Step 1: Cut angle iron frame members to length using abrasive saw.",
            "Step 2: Square and tack-weld main chassis frame.",
            "Step 3: Drill mounting holes for pillow block bearings.",
            "Step 4: Mount drive shaft and verify free rotation.",
            "Step 5: Apply anti-rust primer coat."
        ],
        raw_material_subtotal_usd=raw_subtotal_usd,
        estimated_machining_and_labor_usd=labor_usd,
        total_estimated_cost_usd=grand_usd,
        raw_material_subtotal_inr=format_inr(raw_subtotal_usd),
        estimated_machining_and_labor_inr=format_inr(labor_usd),
        total_estimated_cost_inr=format_inr(grand_usd),
        cost_saving_strategies=tips,
        key_design_considerations=[
            "Load distribution on angle iron frame welds",
            "Corrosion protection with low-cost anti-rust primer"
        ]
    )

def generate_chat_answer(project_name: str, question: str, report_summary: str = "") -> Dict[str, Any]:
    """Generates AI assistant answers for follow-up engineering queries."""
    if settings.GEMINI_API_KEY:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
            prompt = f"""
You are an expert Senior Mechanical Engineer AI assistant specializing in LOW-BUDGET COST EFFECTIVE material selection.
Project Name: "{project_name}"
Report Context: "{report_summary}"
User Question: "{question}"

Provide a concise, technically detailed answer formatted in markdown highlighting low-budget cost-effective material substitutes in Indian Rupees (INR ₹), followed by 2 suggested follow-up questions.
Format JSON:
{{
  "answer": "Your detailed answer...",
  "suggested_followups": ["Question 1?", "Question 2?"]
}}
"""
            resp = requests.post(url, json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=15)
            if resp.status_code == 200:
                text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
                if "```json" in text:
                    text = text.split("```json")[1].split("```")[0].strip()
                elif "```" in text:
                    text = text.split("```")[1].split("```")[0].strip()
                return json.loads(text)
        except Exception as e:
            logger.error(f"Chat AI error: {e}")

    q_lower = question.lower()
    if "low budget" in q_lower or "cost effective" in q_lower or "cheap" in q_lower or "save" in q_lower:
        ans = f"To achieve the most **low-budget, cost-effective design** for **{project_name}**:\n\n1. **Structural Material**: Replace custom machined aluminum or alloy tubing with standard IS 2062 ERW mild steel profiles (saves ~35-45%).\n2. **Shafts & Hardware**: Use cold drawn EN8 steel rods and commercial grade 4.8 fasteners instead of ground chrome pins and stainless hardware (saves ~40%).\n3. **Bearings**: Use self-lubricating Igus engineering polymer bushings or off-the-shelf UC204 pillow blocks."
        followups = ["What are the cheapest structural steel profiles in India?", "How much can I save by 3D printing non-critical brackets?"]
    else:
        ans = f"Regarding **{question}** for **{project_name}**: By selecting cost-effective commercial IS grade materials and standard off-the-shelf hardware, you can reduce total fabrication costs by 40% while maintaining safety factors."
        followups = ["What low-budget welding wire is recommended?", "Where to buy raw steel at wholesale prices in India?"]

    return {"answer": ans, "suggested_followups": followups}
