import json
from pathlib import Path

import ifcopenshell
import ifcopenshell.geom


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "data" / "raw" / "model_v1.ifc"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "geometry.json"


def main():
    model = ifcopenshell.open(str(MODEL_PATH))

    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_WORLD_COORDS, True)

    records = []
    failed = []

    for element in model.by_type("IfcBuildingElement"):
        if not element.Representation:
            continue

        try:
            shape = ifcopenshell.geom.create_shape(settings, element)

            records.append({
                "global_id": element.GlobalId,
                "ifc_type": element.is_a(),
                "name": element.Name or "",
                "vertices": list(shape.geometry.verts),
                "faces": list(shape.geometry.faces),
            })

        except Exception as error:
            failed.append(element.GlobalId)
            print(f"Failed: {element.GlobalId} — {error}")

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            {"units": "metres", "elements": records},
            file,
        )

    print(f"Exported meshes: {len(records)}")
    print(f"Failed elements: {len(failed)}")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()