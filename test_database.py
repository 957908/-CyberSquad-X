from database.database import CyberSquadDB

db = CyberSquadDB()

db.save_scan(
    "https://www.cdac.in",
    60,
    "2026-06-12"
)

print("Saved")