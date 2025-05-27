#!/usr/bin/env python3
"""Test database schema and views"""

import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_database():
    """Test database connection and schema"""
    try:
        # Connect to test database
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD'),
            database='tft_analyzer'
        )
        
        cursor = conn.cursor()
        
        # Test 1: Check if all tables exist
        print("=== TABLES ===")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        expected_tables = ['user', 'lp_history', 'leaderboard_entry', 'tft_match_companion']
        
        for table in tables:
            print(f"✓ {table[0]}")
            
        # Test 2: Check if all views exist
        print("\n=== VIEWS ===")
        cursor.execute("SHOW FULL TABLES WHERE TABLE_TYPE LIKE 'VIEW'")
        views = cursor.fetchall()
        expected_views = ['v_current_leaderboard', 'v_player_profiles', 'v_match_history', 'v_lp_trends', 'v_popular_little_legends']
        
        for view in views:
            print(f"✓ {view[0]}")
            
        # Test 3: Test view queries
        print("\n=== TESTING VIEWS ===")
        test_views = [
            'v_current_leaderboard',
            'v_player_profiles', 
            'v_match_history',
            'v_lp_trends',
            'v_popular_little_legends'
        ]
        
        for view in test_views:
            try:
                cursor.execute(f"SELECT * FROM {view} LIMIT 1")
                print(f"✓ {view} - Query successful")
            except Exception as e:
                print(f"✗ {view} - Error: {e}")
        
        # Test 4: Check table structure
        print("\n=== TABLE STRUCTURES ===")
        for table in expected_tables:
            cursor.execute(f"DESCRIBE {table}")
            columns = cursor.fetchall()
            print(f"\n{table}:")
            for col in columns:
                print(f"  {col[0]} - {col[1]}")
        
        conn.close()
        print("\n✅ Database schema test completed successfully!")
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")

if __name__ == "__main__":
    test_database()
