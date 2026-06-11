import sqlite3


class CyberSquadDB:

    def __init__(self):

        self.conn = sqlite3.connect(
            "cybersquad.db"
        )

        self.cursor = self.conn.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT,
            risk_score INTEGER,
            scan_time TEXT
        )
        """)

        self.conn.commit()

    def save_scan(
        self,
        target,
        risk_score,
        scan_time
    ):

        self.cursor.execute(
            """
            INSERT INTO scans(
                target,
                risk_score,
                scan_time
            )
            VALUES(?,?,?)
            """,
            (
                target,
                risk_score,
                scan_time
            )
        )

        self.conn.commit()

    def get_all_scans(self):

        self.cursor.execute(
            """
            SELECT *
            FROM scans
            ORDER BY id DESC
            """
        )

        return self.cursor.fetchall()