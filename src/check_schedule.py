
from pathlib import Path
import ifcopenshell

ROOT = Path(__file__).resolve().parents[1]
model = ifcopenshell.open(
    str(ROOT / "data/raw/model_v1.ifc")
)

for entity in ["IfcTask", "IfcWorkSchedule", "IfcWorkPlan"]:
    try:
        items = model.by_type(entity)
        print(f"{entity}: {len(items)}")
    except RuntimeError:
        print(f"{entity}: not supported in this IFC schema")
