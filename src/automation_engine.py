"""
Tekron Robotics — Roofing Automation System (Single-File Version)
Author: Bryan C. Spruce

This file contains:
- RoofingAutomationEngine
- Roof Measurement Module
- Material Estimator Module
- Damage Detection Module
- Proposal Generator Module
- Full module registration

This is a complete, production-ready automation system in ONE file.
"""

import traceback
from typing import Dict, Any


# ============================================================
# CORE ENGINE
# ============================================================

class RoofingAutomationEngine:
    def __init__(self):
        self.registry = {}

    def register(self, task_name: str, handler):
        self.registry[task_name] = handler

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            task = payload.get("task")
            data = payload.get("input", {})

            if not task:
                return self._error("Missing 'task' in payload.")

            if task not in self.registry:
                return self._error(f"Unknown task '{task}'.")

            handler = self.registry[task]
            result = handler(data)
            return self._success(task, result)

        except Exception as e:
            return self._exception(e)

    def _success(self, task: str, result: Any) -> Dict[str, Any]:
        return {"status": "success", "task": task, "result": result}

    def _error(self, message: str) -> Dict[str, Any]:
        return {"status": "error", "message": message}

    def _exception(self, e: Exception) -> Dict[str, Any]:
        return {
            "status": "exception",
            "message": str(e),
            "trace": traceback.format_exc()
        }


engine = RoofingAutomationEngine()


# ============================================================
# MODULE 1 — ROOF MEASUREMENT
# ============================================================

def measure_roof(input_data: Dict[str, Any]) -> Dict[str, Any]:
    length = float(input_data.get("length", 0))
    width = float(input_data.get("width", 0))
    pitch = float(input_data.get("pitch", 0))
    waste_factor = float(input_data.get("waste_factor", 0.10))

    base_area = length * width
    pitch_multiplier = 1 + (pitch / 12) ** 2
    pitch_adjusted_area = base_area * pitch_multiplier
    total_with_waste = pitch_adjusted_area * (1 + waste_factor)

    return {
        "base_area_sqft": round(base_area, 2),
        "pitch_adjusted_area_sqft": round(pitch_adjusted_area, 2),
        "total_area_with_waste_sqft": round(total_with_waste, 2),
        "inputs_used": {
            "length": length,
            "width": width,
            "pitch": pitch,
            "waste_factor": waste_factor
        }
    }


# ============================================================
# MODULE 2 — MATERIAL ESTIMATOR
# ============================================================

def estimate_materials(input_data: Dict[str, Any]) -> Dict[str, Any]:
    area = float(input_data.get("total_area_sqft", 0))
    waste_factor = float(input_data.get("waste_factor", 0.10))

    adjusted_area = area * (1 + waste_factor)
    squares = adjusted_area / 100
    shingle_bundles = squares * 3
    underlayment_rolls = adjusted_area / 400
    ridge_caps = squares * 1.1
    nails_lbs = squares * 2.5

    return {
        "adjusted_area_sqft": round(adjusted_area, 2),
        "roofing_squares": round(squares, 2),
        "shingle_bundles": round(shingle_bundles, 1),
        "underlayment_rolls": round(underlayment_rolls, 1),
        "ridge_cap_bundles": round(ridge_caps, 1),
        "nails_lbs": round(nails_lbs, 1),
        "inputs_used": {
            "total_area_sqft": area,
            "waste_factor": waste_factor
        }
    }


# ============================================================
# MODULE 3 — DAMAGE DETECTION
# ============================================================

def detect_damage(input_data: Dict[str, Any]) -> Dict[str, Any]:
    missing = int(input_data.get("missing_shingles", 0))
    cracked = int(input_data.get("cracked_shingles", 0))
    granules = float(input_data.get("granule_loss_percent", 0))
    soft_spots = int(input_data.get("soft_spots", 0))
    hail = int(input_data.get("hail_marks", 0))
    age = int(input_data.get("age_years", 0))

    severity_score = (
        missing * 2 +
        cracked * 1.5 +
        (granules / 10) +
        soft_spots * 4 +
        hail * 0.5 +
        (age / 5)
    )

    if severity_score < 10:
        severity = "Low"
        recommendation = "Minor repairs recommended."
    elif severity_score < 25:
        severity = "Moderate"
        recommendation = "Repairs needed soon."
    else:
        severity = "High"
        recommendation = "Full replacement recommended."

    return {
        "severity_score": round(severity_score, 2),
        "severity_level": severity,
        "recommendation": recommendation,
        "insurance_flag": severity_score >= 20,
        "inputs_used": {
            "missing_shingles": missing,
            "cracked_shingles": cracked,
            "granule_loss_percent": granules,
            "soft_spots": soft_spots,
            "hail_marks": hail,
            "age_years": age
        }
    }


# ============================================================
# MODULE 4 — PROPOSAL GENERATOR
# ============================================================

def generate_proposal(input_data: Dict[str, Any]) -> Dict[str, Any]:
    measurement = input_data.get("measurement", {})
    materials = input_data.get("materials", {})
    damage = input_data.get("damage", {})
    pricing = input_data.get("pricing", {})

    squares = materials.get("roofing_squares", 0)
    bundles = materials.get("shingle_bundles", 0)
    underlayment = materials.get("underlayment_rolls", 0)
    ridge_caps = materials.get("ridge_cap_bundles", 0)
    nails = materials.get("nails_lbs", 0)

    labor_rate = pricing.get("labor_per_square", 0)
    bundle_cost = pricing.get("shingle_bundle_cost", 0)
    underlayment_cost = pricing.get("underlayment_roll_cost", 0)
    ridge_cap_cost = pricing.get("ridge_cap_bundle_cost", 0)
    nail_cost = pricing.get("nail_cost_per_lb", 0)

    labor_total = squares * labor_rate
    shingles_total = bundles * bundle_cost
    underlayment_total = underlayment * underlayment_cost
    ridge_cap_total = ridge_caps * ridge_cap_cost
    nails_total = nails * nail_cost

    material_total = shingles_total + underlayment_total + ridge_cap_total + nails_total
    grand_total = labor_total + material_total

    return {
        "proposal_summary": {
            "total_area_sqft": measurement.get("total_area_with_waste_sqft"),
            "severity_level": damage.get("severity_level"),
            "recommendation": damage.get("recommendation"),
            "insurance_flag": damage.get("insurance_flag")
        },
        "cost_breakdown": {
            "labor_total": round(labor_total, 2),
            "shingles_total": round(shingles_total, 2),
            "underlayment_total": round(underlayment_total, 2),
            "ridge_cap_total": round(ridge_cap_total, 2),
            "nails_total": round(nails_total, 2),
            "material_total": round(material_total, 2),
            "grand_total": round(grand_total, 2)
        },
        "inputs_used": {
            "measurement": measurement,
            "materials": materials,
            "damage": damage,
            "pricing": pricing
        }
    }


# ============================================================
# MODULE REGISTRATION
# ============================================================

engine.register("roof_measurement", measure_roof)
engine.register("material_estimator", estimate_materials)
engine.register("damage_detection", detect_damage)
engine.register("proposal_generator", generate_proposal)
import json
from automation_engine import engine

payload = json.loads(input_data["payload"])
result = engine.run(payload)
return result
python automation_engine.py

  "task": "roof_measurement",
  "input": {
    "length": 40,
    "width": 30,
    "pitch": 6,
    "waste_factor": 0.10
  }automation_engine.py
})
