import csv
from pathlib import Path

from app.database import SessionLocal
from app.models.parking import Vehicle


CSV_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "vehicles"
    / "vehicles.csv"
)


def validate_vehicle(row):
    required_fields = [
        "manufacturer",
        "model",
        "vehicle_type",
        "length_mm",
        "width_mm",
        "height_mm",
    ]

    for field in required_fields:
        if not row.get(field):
            raise ValueError(f"Missing required field: {field}")

    length = float(row["length_mm"])
    width = float(row["width_mm"])
    height = float(row["height_mm"])

    if length <= 0 or width <= 0 or height <= 0:
        raise ValueError("Vehicle dimensions must be greater than zero")

    return length, width, height


def vehicle_exists(db, row):
    return (
        db.query(Vehicle)
        .filter(
            Vehicle.manufacturer == row["manufacturer"],
            Vehicle.model == row["model"],
            Vehicle.variant == row.get("variant", ""),
        )
        .first()
        is not None
    )


def import_vehicles():
    if not CSV_PATH.exists():
        raise FileNotFoundError(
            f"Vehicle dataset not found: {CSV_PATH}"
        )

    db = SessionLocal()

    imported = 0
    skipped = 0
    failed = 0

    try:
        with open(CSV_PATH, "r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            for row_number, row in enumerate(reader, start=2):

                try:
                    length, width, height = validate_vehicle(row)

                    if vehicle_exists(db, row):
                        print(
                            f"SKIPPED row {row_number}: "
                            f"{row['manufacturer']} {row['model']} "
                            f"already exists."
                        )
                        skipped += 1
                        continue

                    model_year = (
                        int(row["model_year"])
                        if row.get("model_year")
                        else None
                    )

                    wheelbase = (
                        float(row["wheelbase_mm"])
                        if row.get("wheelbase_mm")
                        else None
                    )

                    vehicle = Vehicle(
                        manufacturer=row["manufacturer"].strip(),
                        model=row["model"].strip(),
                        variant=row.get("variant", "").strip() or None,
                        model_year=model_year,
                        vehicle_type=row["vehicle_type"].strip(),

                        length_mm=length,
                        width_mm=width,
                        height_mm=height,
                        wheelbase_mm=wheelbase,

                        source_name=row.get("source_name", "").strip() or None,
                        source_url=row.get("source_url", "").strip() or None,
                        dimension_notes=(
                            row.get("dimension_notes", "").strip()
                            or None
                        ),
                    )

                    db.add(vehicle)
                    imported += 1

                    print(
                        f"IMPORTED: "
                        f"{vehicle.manufacturer} "
                        f"{vehicle.model}"
                    )

                except Exception as error:
                    failed += 1
                    print(
                        f"FAILED row {row_number}: {error}"
                    )

            db.commit()

        print("\n------------------------------")
        print("Vehicle import completed")
        print("------------------------------")
        print(f"Imported : {imported}")
        print(f"Skipped  : {skipped}")
        print(f"Failed   : {failed}")
        print("------------------------------")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    import_vehicles()