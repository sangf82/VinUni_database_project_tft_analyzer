#!/usr/bin/env python3
"""
Simplified TFT Game Assets Test
Tests static game data APIs and creates sample data for testing
"""

import requests
import json
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def test_data_dragon_apis():
    """Test Data Dragon APIs for game assets"""
    print("🎮 Testing TFT Game Assets APIs")
    print("="*50)
    
    try:
        # Get latest version
        print("📥 Fetching latest version...")
        response = requests.get("https://ddragon.leagueoflegends.com/api/versions.json", timeout=10)
        response.raise_for_status()
        version = response.json()[0]
        print(f"✅ Latest version: {version}")
        
        # Test Little Legends (Pets)
        print("\n🐾 Testing Little Legends/Pets...")
        ll_url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/tft-tactician.json"
        ll_response = requests.get(ll_url, timeout=10)
        
        if ll_response.status_code == 200:
            ll_data = ll_response.json()
            pets = ll_data.get('data', {})
            print(f"✅ Found {len(pets)} Little Legends")
            
            # Show first 3 pets with details
            for i, (pet_id, pet_info) in enumerate(pets.items()):
                if i < 3:
                    print(f"  🐾 {pet_info.get('name', 'Unknown')}")
                    print(f"     ID: {pet_id}")
                    print(f"     Species: {pet_info.get('species', 'Unknown')}")
                    print(f"     Image: https://ddragon.leagueoflegends.com/cdn/{version}/img/tft-tactician/{pet_info.get('image', {}).get('full', '')}")
        else:
            print(f"❌ Little Legends API failed: {ll_response.status_code}")
        
        # Test Traits
        print("\n⚡ Testing Traits...")
        traits_url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/tft-trait.json"
        traits_response = requests.get(traits_url, timeout=10)
        
        if traits_response.status_code == 200:
            traits_data = traits_response.json()
            traits = traits_data.get('data', {})
            print(f"✅ Found {len(traits)} Traits")
            
            # Show first 3 traits with details
            for i, (trait_id, trait_info) in enumerate(traits.items()):
                if i < 3:
                    print(f"  ⚡ {trait_info.get('name', 'Unknown')}")
                    print(f"     ID: {trait_id}")
                    print(f"     Image: https://ddragon.leagueoflegends.com/cdn/{version}/img/tft-trait/{trait_info.get('image', {}).get('full', '')}")
        else:
            print(f"❌ Traits API failed: {traits_response.status_code}")
        
        # Test Items (includes some augments)
        print("\n🔮 Testing Items...")
        items_url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/tft-item.json"
        items_response = requests.get(items_url, timeout=10)
        
        if items_response.status_code == 200:
            items_data = items_response.json()
            items = items_data.get('data', {})
            print(f"✅ Found {len(items)} Items")
            
            # Show first 3 items with details
            for i, (item_id, item_info) in enumerate(items.items()):
                if i < 3:
                    print(f"  🔮 {item_info.get('name', 'Unknown')}")
                    print(f"     ID: {item_id}")
                    print(f"     Image: https://ddragon.leagueoflegends.com/cdn/{version}/img/tft-item/{item_info.get('image', {}).get('full', '')}")
        else:
            print(f"❌ Items API failed: {items_response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing APIs: {e}")
        return False

def create_sample_companion_data():
    """Create sample companion data for testing user pet usage"""
    print("\n💾 Creating sample companion data...")
    
    try:
        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            port=int(os.environ.get("DB_PORT")),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME")
        )
        cursor = conn.cursor()
        
        # Sample companion data - representing different Little Legends
        sample_data = [
            # Format: (match_id, puuid, content_id, skin_id, placement, match_timestamp)
            ('VN2_1234567890', 'player1_puuid', 'TFT_PetSpiritBlossom', 1, 3, '2025-05-27 10:00:00'),
            ('VN2_1234567891', 'player1_puuid', 'TFT_PetSpiritBlossom', 1, 1, '2025-05-27 11:00:00'),
            ('VN2_1234567892', 'player2_puuid', 'TFT_PetArcane', 2, 4, '2025-05-27 10:30:00'),
            ('VN2_1234567893', 'player2_puuid', 'TFT_PetArcane', 2, 2, '2025-05-27 11:30:00'),
            ('VN2_1234567894', 'player3_puuid', 'TFT_PetPoolParty', 0, 5, '2025-05-27 12:00:00'),
            ('VN2_1234567895', 'player1_puuid', 'TFT_PetPoolParty', 1, 6, '2025-05-27 12:30:00'),
            ('VN2_1234567896', 'player3_puuid', 'TFT_PetSpiritBlossom', 2, 1, '2025-05-27 13:00:00'),
            ('VN2_1234567897', 'player4_puuid', 'TFT_PetDragonmancer', 0, 3, '2025-05-27 13:30:00'),
            ('VN2_1234567898', 'player4_puuid', 'TFT_PetDragonmancer', 0, 7, '2025-05-27 14:00:00'),
            ('VN2_1234567899', 'player5_puuid', 'TFT_PetArcane', 1, 2, '2025-05-27 14:30:00'),
        ]
        
        # Insert sample data
        insert_query = """
        INSERT INTO tft_match_companion 
        (match_id, puuid, content_id, skin_id, placement, match_timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        
        cursor.executemany(insert_query, sample_data)
        conn.commit()
        
        print(f"✅ Inserted {len(sample_data)} sample companion records")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        return False

def test_user_pet_usage():
    """Test user pet usage queries"""
    print("\n👥 Testing User Pet Usage...")
    
    try:
        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            port=int(os.environ.get("DB_PORT")),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME")
        )
        cursor = conn.cursor()
        
        # Query most popular pets
        cursor.execute("""
        SELECT 
            content_id,
            skin_id,
            COUNT(*) as usage_count,
            AVG(placement) as avg_placement,
            COUNT(DISTINCT puuid) as unique_users
        FROM tft_match_companion
        GROUP BY content_id, skin_id
        ORDER BY usage_count DESC
        """)
        
        popular_pets = cursor.fetchall()
        print(f"✅ Most Popular Pets:")
        for pet in popular_pets:
            content_id, skin_id, usage_count, avg_placement, unique_users = pet
            print(f"  🐾 {content_id} (skin: {skin_id})")
            print(f"     Usage: {usage_count} times by {unique_users} users")
            print(f"     Avg placement: {avg_placement:.1f}")
        
        # Query user pet preferences
        cursor.execute("""
        SELECT 
            puuid,
            content_id,
            skin_id,
            COUNT(*) as times_used,
            AVG(placement) as avg_placement
        FROM tft_match_companion
        GROUP BY puuid, content_id, skin_id
        ORDER BY puuid, times_used DESC
        """)
        
        user_pets = cursor.fetchall()
        print(f"\n✅ User Pet Preferences:")
        current_user = None
        for user_pet in user_pets:
            puuid, content_id, skin_id, times_used, avg_placement = user_pet
            if puuid != current_user:
                current_user = puuid
                print(f"  👤 User: {puuid}")
            print(f"     🐾 {content_id} (skin: {skin_id}) - {times_used} uses, avg: {avg_placement:.1f}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error testing user pet usage: {e}")
        return False

def test_database_views():
    """Test the database views with companion data"""
    print("\n👁️ Testing Database Views...")
    
    try:
        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            port=int(os.environ.get("DB_PORT")),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME")
        )
        cursor = conn.cursor()
        
        # Test popular little legends view
        cursor.execute("SELECT COUNT(*) FROM v_popular_little_legends")
        count = cursor.fetchone()[0]
        print(f"✅ v_popular_little_legends: {count} entries")
        
        if count > 0:
            cursor.execute("SELECT * FROM v_popular_little_legends LIMIT 3")
            results = cursor.fetchall()
            print("  Top Little Legends:")
            for row in results:
                print(f"    {row}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error testing database views: {e}")
        return False

def main():
    """Main test function"""
    print("🎮 TFT Game Assets Test - Simplified Version")
    print("="*60)
    
    # Test 1: Static game data APIs
    api_test = test_data_dragon_apis()
    
    # Test 2: Create sample companion data
    sample_data = create_sample_companion_data()
    
    # Test 3: Test user pet usage queries
    if sample_data:
        usage_test = test_user_pet_usage()
        
        # Test 4: Test database views
        view_test = test_database_views()
    
    print("\n" + "="*60)
    print("🎉 Test Summary:")
    print(f"✅ Static Game Data APIs: {'PASS' if api_test else 'FAIL'}")
    print(f"✅ Sample Companion Data: {'PASS' if sample_data else 'FAIL'}")
    if sample_data:
        print(f"✅ User Pet Usage Queries: {'PASS' if usage_test else 'FAIL'}")
        print(f"✅ Database Views: {'PASS' if view_test else 'FAIL'}")
    
    print("\n📋 Next Steps:")
    print("1. Run actual ETL DAGs to collect real companion data")
    print("2. Use extracted data to populate comprehensive pet usage analytics")
    print("3. Integrate static game data with user data for rich frontend experience")

if __name__ == "__main__":
    main()
