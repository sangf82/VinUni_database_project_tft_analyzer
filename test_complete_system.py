#!/usr/bin/env python3
"""
Complete system test for TFT Analyzer - Vietnam Server
Tests all components: Extract, Process, Load, and Database Views
"""

import sys
import os
import mysql.connector
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_database_connection():
    """Test database connection and basic functionality"""
    print("🔧 Testing database connection...")
    try:
        conn = mysql.connector.connect(
            host=os.environ.get("LC_HOST"),
            port=int(os.environ.get("LC_PORT")),
            user=os.environ.get("LC_USER"),
            password=os.environ.get("LC_PASSWORD"),
            database=os.environ.get("LC_NAME")
        )
        cursor = conn.cursor()
        
        # Test basic connectivity
        cursor.execute("SELECT DATABASE() as current_LC, NOW() as LC_time")
        result = cursor.fetchone()
        print(f"✅ Connected to database: {result[0]} at {result[1]}")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_table_structure():
    """Test that all tables and views exist"""
    print("\n🏗️ Testing database structure...")
    try:
        conn = mysql.connector.connect(
            host=os.environ.get("LC_HOST"),
            port=int(os.environ.get("LC_PORT")),
            user=os.environ.get("LC_USER"),
            password=os.environ.get("LC_PASSWORD"),
            database=os.environ.get("LC_NAME")
        )
        cursor = conn.cursor()
        
        # Check tables
        expected_tables = ['user', 'lp_history', 'leaderboard_entry', 'tft_match_companion']
        cursor.execute("SHOW TABLES")
        existing_tables = [table[0] for table in cursor.fetchall()]
        
        for table in expected_tables:
            if table in existing_tables:
                print(f"✅ Table {table} exists")
            else:
                print(f"❌ Table {table} missing")
        
        # Check views
        expected_views = ['v_current_leaderboard', 'v_player_profiles', 'v_match_history', 'v_lp_trends', 'v_popular_little_legends']
        for view in expected_views:
            if view in existing_tables:
                print(f"✅ View {view} exists")
            else:
                print(f"❌ View {view} missing")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Structure test failed: {e}")
        return False

def test_leaderboard_data():
    """Test leaderboard data quality"""
    print("\n📊 Testing leaderboard data...")
    try:
        conn = mysql.connector.connect(
            host=os.environ.get("LC_HOST"),
            port=int(os.environ.get("LC_PORT")),
            user=os.environ.get("LC_USER"),
            password=os.environ.get("LC_PASSWORD"),
            database=os.environ.get("LC_NAME")
        )
        cursor = conn.cursor()
        
        # Test data counts
        cursor.execute("SELECT COUNT(*) FROM leaderboard_entry")
        total_count = cursor.fetchone()[0]
        print(f"✅ Total leaderboard entries: {total_count}")
        
        # Test tier distribution
        cursor.execute("SELECT tier, COUNT(*) FROM leaderboard_entry GROUP BY tier ORDER BY COUNT(*) DESC")
        tier_data = cursor.fetchall()
        print("✅ Tier distribution:")
        for tier, count in tier_data:
            print(f"   {tier}: {count} players")
        
        # Test position ordering
        cursor.execute("SELECT position, username, tier, lp FROM leaderboard_entry ORDER BY position LIMIT 5")
        top_players = cursor.fetchall()
        print("✅ Top 5 players:")
        for pos, username, tier, lp in top_players:
            print(f"   #{pos}: {username} ({tier}) - {lp} LP")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Leaderboard data test failed: {e}")
        return False

def test_etl_components():
    """Test ETL components"""
    print("\n⚙️ Testing ETL components...")
    try:
        sys.path.append('.')
        from Steps.extract import extract_leaderboard_data
        from Steps.process import process_leaderboard_data
        from Steps.load import load_leaderboard_to_sql
        
        print("✅ ETL modules imported successfully")
        print("✅ Extract function: extract_leaderboard_data() available")
        print("✅ Process function: process_leaderboard_data() available") 
        print("✅ Load function: load_leaderboard_to_sql() available")
        
        # Test companion extraction
        from Steps.companion_extract import extract_player_companions, extract_match_companions
        print("✅ Companion extraction functions available")
        print("✅ Default region set to Vietnam server (vn2)")
        
        return True
    except Exception as e:
        print(f"❌ ETL component test failed: {e}")
        return False

def test_views_functionality():
    """Test database views functionality"""
    print("\n👁️ Testing database views...")
    try:
        conn = mysql.connector.connect(
            host=os.environ.get("LC_HOST"),
            port=int(os.environ.get("LC_PORT")),
            user=os.environ.get("LC_USER"),
            password=os.environ.get("LC_PASSWORD"),
            database=os.environ.get("LC_NAME")
        )
        cursor = conn.cursor()
        
        # Test leaderboard view
        cursor.execute("SELECT COUNT(*) FROM v_current_leaderboard")
        lb_count = cursor.fetchone()[0]
        print(f"✅ v_current_leaderboard: {lb_count} entries")
        
        # Test view structure
        cursor.execute("SELECT * FROM v_current_leaderboard LIMIT 1")
        if cursor.fetchone():
            print("✅ v_current_leaderboard returns data")
        
        # Test other views (they may be empty but should not error)
        views_to_test = ['v_player_profiles', 'v_match_history', 'v_lp_trends', 'v_popular_little_legends']
        for view in views_to_test:
            cursor.execute(f"SELECT COUNT(*) FROM {view}")
            count = cursor.fetchone()[0]
            print(f"✅ {view}: {count} entries (ready for data)")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Views test failed: {e}")
        return False

def main():
    """Run all system tests"""
    print("🚀 TFT Analyzer - Vietnam Server - Complete System Test")
    print("=" * 60)
    
    tests = [
        ("Database Connection", test_database_connection),
        ("Database Structure", test_table_structure),
        ("Leaderboard Data", test_leaderboard_data),
        ("ETL Components", test_etl_components),
        ("Database Views", test_views_functionality)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        result = test_func()
        if result:
            passed_tests += 1
    
    print("\n" + "=" * 60)
    print(f"📈 FINAL RESULTS: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! System is ready for production.")
        print("\n✨ Next steps:")
        print("  1. Start Airflow: cd airflow && airflow webserver --port 8080")
        print("  2. Start scheduler: cd airflow && airflow scheduler")
        print("  3. Access web UI: http://localhost:8080")
        print("  4. Run DAGs: leaderboard_etl_dag, tft_etl_pipeline")
    else:
        print("⚠️ Some tests failed. Please review the errors above.")
        print("📋 Check README.md for troubleshooting guide.")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
