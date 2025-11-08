"""
Migration script to add job_id column to Resume table
"""
from app import app, db
from sqlalchemy import text

def add_job_id_column():
    with app.app_context():
        try:
            with db.engine.connect() as conn:
                # Check if column already exists
                result = conn.execute(text("PRAGMA table_info(resume)"))
                columns = [row[1] for row in result]
                
                if 'job_id' not in columns:
                    # Add the column
                    conn.execute(text('ALTER TABLE resume ADD COLUMN job_id INTEGER REFERENCES "Job"(id)'))
                    conn.commit()
                    print("[OK] Successfully added job_id column to Resume table")
                else:
                    print("[INFO] job_id column already exists in Resume table")
        except Exception as e:
            print(f"[ERROR] Error: {e}")

if __name__ == '__main__':
    add_job_id_column()

