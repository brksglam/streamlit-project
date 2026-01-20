import csv
import os
from datetime import datetime

def test_csv_write():
    print("Testing CSV Write...")
    file_path = "leads.csv"
    
    # Clean up before test
    if os.path.exists(file_path):
        os.remove(file_path)
        
    # Test Data
    name = "Test User"
    phone = "555-0000"
    note = "TEST ENTRY"
    
    # Simulate App Logic
    try:
        exists = os.path.isfile(file_path)
        with open(file_path, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if not exists: w.writerow(["Date", "Name", "Phone", "Note"])
            w.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), name, phone, note])
        print("✅ Write Successful")
    except Exception as e:
        print(f"❌ Write Failed: {e}")
        return

    # Verify Read
    print("Testing CSV Read...")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            rows = list(csv.reader(f))
            if len(rows) >= 2 and rows[-1][1] == name:
                print("✅ Read Successful (Data Matches)")
            else:
                print("❌ Read Failed (Data Mismatch)")
    except Exception as e:
         print(f"❌ Read Failed: {e}")

if __name__ == "__main__":
    test_csv_write()
