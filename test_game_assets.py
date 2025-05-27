#!/usr/bin/env python3
"""
TFT Game Assets Test Module
Tests functionality for:
- Pet/Little Legend images and names
- Augments images and data
- Traits images and data
- User pet usage tracking
- Static game data integration
"""

import os
import sys
import json
import requests
import mysql.connector
from dotenv import load_dotenv
from datetime import datetime
import time

# Load environment variables
load_dotenv()

def test_database_connection():
    """Test database connection"""
    try:
        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            port=int(os.environ.get("DB_PORT")),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME")
        )
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def get_latest_tft_version():
    """Get the latest TFT/LoL version from Data Dragon"""
    try:
        response = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
        response.raise_for_status()
        versions = response.json()
        print(f"✅ Latest TFT version: {versions[0]}")
        return versions[0]
    except Exception as e:
        print(f"❌ Error fetching version: {e}")
        return "15.10.1"  # Fallback version

def fetch_little_legends_data(version):
    """Fetch Little Legend/Pet data from Data Dragon"""
    try:
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/tft-tactician.json"
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Fetched {len(data.get('data', {}))} Little Legends")
        
        # Save to file for debugging
        with open("little_legends_data.json", "w") as f:
            json.dump(data, f, indent=2)
            
        return data
    except Exception as e:
        print(f"❌ Error fetching Little Legends: {e}")
        return None

def fetch_traits_data(version):
    """Fetch Traits data from Data Dragon"""
    try:
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/tft-trait.json"
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        print(f"✅ Fetched {len(data.get('data', {}))} Traits")
        
        # Save to file for debugging
        with open("traits_data.json", "w") as f:
            json.dump(data, f, indent=2)
            
        return data
    except Exception as e:
        print(f"❌ Error fetching Traits: {e}")
        return None

def fetch_augments_data():
    """
    Fetch Augments data from Community Dragon (since Data Dragon doesn't have augments)
    """
    try:
        # Try Community Dragon for augments
        url = "https://raw.communitydragon.org/latest/cdragon/tft/en_us.json"
        response = requests.get(url)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract augments from the community dragon data
        augments = {}
        if 'items' in data:
            for item_id, item_data in data['items'].items():
                if item_data.get('loadoutsIcon', '').find('augment') != -1 or \
                   item_data.get('name', '').lower().find('augment') != -1:
                    augments[item_id] = item_data
        
        print(f"✅ Fetched {len(augments)} Augments from Community Dragon")
        
        # Save to file for debugging
        with open("augments_data.json", "w") as f:
            json.dump(augments, f, indent=2)
            
        return augments
    except Exception as e:
        print(f"❌ Error fetching Augments: {e}")
        # Try alternative approach with specific augment endpoint
        try:
            # Alternative: Try MetaTFT API for augments
            url = "https://api.metatft.com/tft/units"
            response = requests.get(url)
            if response.status_code == 200:
                print("✅ Found alternative augment source")
                return response.json()
        except:
            pass
        return None

def get_pet_names_and_images(little_legends_data, version):
    """Extract pet names and image URLs from Little Legends data"""
    if not little_legends_data or 'data' not in little_legends_data:
        print("❌ No Little Legends data available")
        return {}
    
    pets = {}
    for pet_id, pet_data in little_legends_data['data'].items():
        pets[pet_id] = {
            'name': pet_data.get('name', 'Unknown Pet'),
            'species': pet_data.get('species', ''),
            'image_url': f"https://ddragon.leagueoflegends.com/cdn/{version}/img/tft-tactician/{pet_data.get('image', {}).get('full', '')}",
            'description': pet_data.get('description', ''),
            'tier': pet_data.get('tier', 1)
        }
    
    print(f"✅ Processed {len(pets)} pet names and images")
    return pets

def get_trait_names_and_images(traits_data, version):
    """Extract trait names and image URLs from Traits data"""
    if not traits_data or 'data' not in traits_data:
        print("❌ No Traits data available")
        return {}
    
    traits = {}
    for trait_id, trait_data in traits_data['data'].items():
        traits[trait_id] = {
            'name': trait_data.get('name', 'Unknown Trait'),
            'description': trait_data.get('description', ''),
            'image_url': f"https://ddragon.leagueoflegends.com/cdn/{version}/img/tft-trait/{trait_data.get('image', {}).get('full', '')}",
            'sets': trait_data.get('sets', [])
        }
    
    print(f"✅ Processed {len(traits)} trait names and images")
    return traits

def get_augment_names_and_images(augments_data):
    """Extract augment names and image URLs from Augments data"""
    if not augments_data:
        print("❌ No Augments data available")
        return {}
    
    augments = {}
    for aug_id, aug_data in augments_data.items():
        # Handle different data structures from different sources
        image_url = ""
        if 'loadoutsIcon' in aug_data:
            image_url = aug_data['loadoutsIcon']
        elif 'icon' in aug_data:
            image_url = aug_data['icon']
        
        augments[aug_id] = {
            'name': aug_data.get('name', 'Unknown Augment'),
            'description': aug_data.get('description', ''),
            'image_url': image_url,
            'tier': aug_data.get('tier', 1)
        }
    
    print(f"✅ Processed {len(augments)} augment names and images")
    return augments

def get_user_pet_usage():
    """Get which users use which pets from the database"""
    if not test_database_connection():
        return {}
    
    try:
        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            port=int(os.environ.get("DB_PORT")),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME")
        )
        cursor = conn.cursor()
        
        # Query to get user pet usage
        query = """
        SELECT 
            u.username,
            c.content_id,
            c.skin_id,
            COUNT(*) as usage_count,
            AVG(c.placement) as avg_placement,
            MIN(c.match_timestamp) as first_used,
            MAX(c.match_timestamp) as last_used
        FROM tft_match_companion c
        JOIN user u ON c.puuid = u.id
        GROUP BY u.username, c.content_id, c.skin_id
        ORDER BY u.username, usage_count DESC
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        user_pets = {}
        for row in results:
            username, content_id, skin_id, usage_count, avg_placement, first_used, last_used = row
            
            if username not in user_pets:
                user_pets[username] = []
            
            user_pets[username].append({
                'content_id': content_id,
                'skin_id': skin_id,
                'usage_count': usage_count,
                'avg_placement': round(avg_placement, 2) if avg_placement else 0,
                'first_used': first_used,
                'last_used': last_used
            })
        
        cursor.close()
        conn.close()
        
        print(f"✅ Found pet usage data for {len(user_pets)} users")
        return user_pets
        
    except Exception as e:
        print(f"❌ Error fetching user pet usage: {e}")
        return {}

def get_most_popular_pets():
    """Get the most popular pets across all users"""
    if not test_database_connection():
        return []
    
    try:
        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST"),
            port=int(os.environ.get("DB_PORT")),
            user=os.environ.get("DB_USER"),
            password=os.environ.get("DB_PASSWORD"),
            database=os.environ.get("DB_NAME")
        )
        cursor = conn.cursor()
        
        # Query to get most popular pets
        query = """
        SELECT 
            content_id,
            skin_id,
            COUNT(*) as total_usage,
            COUNT(DISTINCT puuid) as unique_users,
            AVG(placement) as avg_placement,
            ROUND(AVG(CASE WHEN placement <= 4 THEN 1 ELSE 0 END) * 100, 1) as win_rate
        FROM tft_match_companion
        GROUP BY content_id, skin_id
        HAVING total_usage >= 5
        ORDER BY total_usage DESC
        LIMIT 20
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        popular_pets = []
        for row in results:
            content_id, skin_id, total_usage, unique_users, avg_placement, win_rate = row
            popular_pets.append({
                'content_id': content_id,
                'skin_id': skin_id,
                'total_usage': total_usage,
                'unique_users': unique_users,
                'avg_placement': round(avg_placement, 2) if avg_placement else 0,
                'win_rate': win_rate if win_rate else 0
            })
        
        cursor.close()
        conn.close()
        
        print(f"✅ Found {len(popular_pets)} popular pets")
        return popular_pets
        
    except Exception as e:
        print(f"❌ Error fetching popular pets: {e}")
        return []

def display_test_results(pets, traits, augments, user_pets, popular_pets):
    """Display comprehensive test results"""
    print("\n" + "="*80)
    print("🎮 TFT GAME ASSETS TEST RESULTS")
    print("="*80)
    
    # Display pet information
    print(f"\n🐾 LITTLE LEGENDS/PETS ({len(pets)} total)")
    print("-" * 50)
    for i, (pet_id, pet_info) in enumerate(pets.items()):
        if i < 5:  # Show first 5 pets
            print(f"ID: {pet_id}")
            print(f"Name: {pet_info['name']}")
            print(f"Species: {pet_info['species']}")
            print(f"Image: {pet_info['image_url']}")
            print(f"Tier: {pet_info['tier']}")
            print("-" * 30)
    
    # Display trait information  
    print(f"\n⚡ TRAITS ({len(traits)} total)")
    print("-" * 50)
    for i, (trait_id, trait_info) in enumerate(traits.items()):
        if i < 5:  # Show first 5 traits
            print(f"ID: {trait_id}")
            print(f"Name: {trait_info['name']}")
            print(f"Image: {trait_info['image_url']}")
            print("-" * 30)
    
    # Display augment information
    print(f"\n🔮 AUGMENTS ({len(augments)} total)")
    print("-" * 50)
    for i, (aug_id, aug_info) in enumerate(augments.items()):
        if i < 5:  # Show first 5 augments
            print(f"ID: {aug_id}")
            print(f"Name: {aug_info['name']}")
            print(f"Image: {aug_info['image_url']}")
            print("-" * 30)
    
    # Display user pet usage
    print(f"\n👥 USER PET USAGE ({len(user_pets)} users)")
    print("-" * 50)
    for i, (username, pets_used) in enumerate(user_pets.items()):
        if i < 3:  # Show first 3 users
            print(f"User: {username}")
            print(f"Pets used: {len(pets_used)}")
            if pets_used:
                most_used = pets_used[0]  # First item is most used due to ORDER BY
                print(f"Most used pet: {most_used['content_id']} (skin: {most_used['skin_id']})")
                print(f"Usage count: {most_used['usage_count']}")
                print(f"Avg placement: {most_used['avg_placement']}")
            print("-" * 30)
    
    # Display popular pets
    print(f"\n🏆 MOST POPULAR PETS ({len(popular_pets)} total)")
    print("-" * 50)
    for i, pet in enumerate(popular_pets[:5]):  # Show top 5
        print(f"#{i+1} Pet ID: {pet['content_id']} (skin: {pet['skin_id']})")
        print(f"Total usage: {pet['total_usage']}")
        print(f"Unique users: {pet['unique_users']}")
        print(f"Avg placement: {pet['avg_placement']}")
        print(f"Win rate: {pet['win_rate']}%")
        print("-" * 30)

def save_results_to_files(pets, traits, augments, user_pets, popular_pets):
    """Save all test results to JSON files for further analysis"""
    try:
        # Save pets data
        with open("test_results_pets.json", "w") as f:
            json.dump(pets, f, indent=2)
        
        # Save traits data
        with open("test_results_traits.json", "w") as f:
            json.dump(traits, f, indent=2)
        
        # Save augments data
        with open("test_results_augments.json", "w") as f:
            json.dump(augments, f, indent=2)
        
        # Save user pets data
        with open("test_results_user_pets.json", "w") as f:
            json.dump(user_pets, f, indent=2, default=str)
        
        # Save popular pets data
        with open("test_results_popular_pets.json", "w") as f:
            json.dump(popular_pets, f, indent=2, default=str)
        
        print("✅ All test results saved to JSON files")
        
    except Exception as e:
        print(f"❌ Error saving results: {e}")

def main():
    """Main test function"""
    print("🚀 Starting TFT Game Assets Test")
    print("Testing: Pet images, Augment images, Trait images, Pet names, User pet usage")
    print("=" * 80)
    
    # Get latest version
    version = get_latest_tft_version()
    
    # Fetch all static data
    print("\n📥 Fetching static game data...")
    little_legends_data = fetch_little_legends_data(version)
    traits_data = fetch_traits_data(version)
    augments_data = fetch_augments_data()
    
    # Process data
    print("\n⚙️ Processing game assets...")
    pets = get_pet_names_and_images(little_legends_data, version)
    traits = get_trait_names_and_images(traits_data, version)
    augments = get_augment_names_and_images(augments_data) if augments_data else {}
    
    # Get user data from database
    print("\n🔍 Fetching user pet usage data...")
    user_pets = get_user_pet_usage()
    popular_pets = get_most_popular_pets()
    
    # Display results
    display_test_results(pets, traits, augments, user_pets, popular_pets)
    
    # Save results
    print("\n💾 Saving results...")
    save_results_to_files(pets, traits, augments, user_pets, popular_pets)
    
    print("\n🎉 Test completed successfully!")
    print("\nFiles created:")
    print("- little_legends_data.json (Raw Little Legends data)")
    print("- traits_data.json (Raw Traits data)")
    print("- augments_data.json (Raw Augments data)")
    print("- test_results_pets.json (Processed Pet data)")
    print("- test_results_traits.json (Processed Trait data)")
    print("- test_results_augments.json (Processed Augment data)")
    print("- test_results_user_pets.json (User Pet usage)")
    print("- test_results_popular_pets.json (Popular Pets)")

if __name__ == "__main__":
    main()
