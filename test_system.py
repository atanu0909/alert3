#!/usr/bin/env python3
"""
Test script for the attendance system
"""

import os
import sys
from datetime import datetime, date
from attendance_system import AttendanceSystem

def test_database_connection():
    """Test database connection"""
    print("Testing database connection...")
    try:
        system = AttendanceSystem()
        conn = system.get_database_connection()
        print("✓ Database connection successful")
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def test_attendance_query():
    """Test attendance data retrieval"""
    print("\nTesting attendance data retrieval...")
    try:
        system = AttendanceSystem()
        df = system.get_daily_attendance()
        print(f"✓ Retrieved {len(df)} attendance records")
        if not df.empty:
            print("Sample data:")
            print(df.head())
        return True
    except Exception as e:
        print(f"✗ Attendance query failed: {e}")
        return False

def test_report_generation():
    """Test Excel report generation"""
    print("\nTesting report generation...")
    try:
        system = AttendanceSystem()
        df = system.get_daily_attendance()
        if not df.empty:
            filepath = system.create_attendance_report(df, date.today())
            print(f"✓ Report generated: {filepath}")
            # Clean up
            if os.path.exists(filepath):
                os.remove(filepath)
            return True
        else:
            print("⚠ No data to generate report")
            return True
    except Exception as e:
        print(f"✗ Report generation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=== Attendance System Test Suite ===\n")
    
    tests = [
        test_database_connection,
        test_attendance_query,
        test_report_generation
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {sum(results)}/{len(results)}")
    
    if all(results):
        print("All tests passed! ✓")
        sys.exit(0)
    else:
        print("Some tests failed! ✗")
        sys.exit(1)

if __name__ == "__main__":
    main()
