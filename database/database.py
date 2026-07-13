import sqlite3
from api.auth.password import hash_password

class CyberSquadDB:

    def __init__(self):
        self.conn = sqlite3.connect(
            "cybersquad.db",
            check_same_thread=False
        )
        self.cursor = self.conn.cursor()

        # Scans Table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS scans(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT,
            risk_score INTEGER,
            scan_time TEXT
        )
        """)

        # Users Table
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users(
            username TEXT PRIMARY KEY,
            password_hash TEXT,
            first_name TEXT,
            last_name TEXT,
            work_organization TEXT,
            mobile_number TEXT,
            role TEXT
        )
        """)

        self.conn.commit()
        self._seed_default_users()

    def _seed_default_users(self):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM users")
            if self.cursor.fetchone()[0] == 0:
                default_users = [
                    ("admin", hash_password("admin123"), "Admin", "User", "CyberSquad", "1234567890", "admin"),
                    ("analyst", hash_password("analyst123"), "Security", "Analyst", "CyberSquad", "1234567890", "analyst"),
                    ("viewer", hash_password("viewer123"), "Guest", "Viewer", "CyberSquad", "1234567890", "viewer")
                ]
                self.cursor.executemany("""
                INSERT INTO users(username, password_hash, first_name, last_name, work_organization, mobile_number, role)
                VALUES(?,?,?,?,?,?,?)
                """, default_users)
                self.conn.commit()
        except Exception as e:
            print("Error seeding default users:", str(e))

    def save_scan(self, target, risk_score, scan_time):
        self.cursor.execute(
            """
            INSERT INTO scans(
                target,
                risk_score,
                scan_time
            )
            VALUES(?,?,?)
            """,
            (target, risk_score, scan_time)
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

    # User Management Helpers
    def get_user(self, username):
        self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = self.cursor.fetchone()
        if row:
            return {
                "username": row[0],
                "password": row[1],
                "first_name": row[2],
                "last_name": row[3],
                "work_organization": row[4],
                "mobile_number": row[5],
                "role": row[6]
            }
        return None

    def create_user(self, username, password_hash, first_name, last_name, work_organization, mobile_number, role="user"):
        try:
            self.cursor.execute("""
            INSERT INTO users(username, password_hash, first_name, last_name, work_organization, mobile_number, role)
            VALUES(?,?,?,?,?,?,?)
            """, (username, password_hash, first_name, last_name, work_organization, mobile_number, role))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def update_password(self, username, new_password_hash):
        self.cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", (new_password_hash, username))
        self.conn.commit()
        return self.cursor.rowcount > 0