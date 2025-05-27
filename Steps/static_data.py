#!/usr/bin/env python3
"""
Module for extracting, processing and loading TFT static data:
- Champions
- Items
- Augments
- Traits
- Little Legends (Pets/Tacticians)
"""

import os
import json
import requests
from dotenv import load_dotenv
import mysql.connector
from datetime import datetime

# Load environment variables
load_dotenv()

def get_latest_version():
    """
    Get the latest TFT data version from Data Dragon.
    
    Returns:
        str: Latest version string (e.g., "15.10.1")
    """
    try:
        response = requests.get("https://ddragon.leagueoflegends.com/api/versions.json")
        response.raise_for_status()
        versions = response.json()
        return versions[0]  # First entry is the latest version
    except Exception as e:
        print(f"Error fetching latest version: {e}")
        return None

def fetch_champions_data(version):
    """
    Fetch TFT champion data from Data Dragon.
    
    Args:
        version (str): Data Dragon version
        
    Returns:
        dict: TFT champion data
    """
    try:
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/tft-champion.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching champion data: {e}")
        return None

def fetch_tacticians_data(version):
    """
    Fetch TFT tactician (Little Legend/Pet) data from Data Dragon.
    
    Args:
        version (str): Data Dragon version
        
    Returns:
        dict: TFT tactician data
    """
    try:
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/tft-tactician.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching tactician data: {e}")
        return None

def fetch_items_data(version):
    """
    Fetch TFT item data from Data Dragon.
    
    Args:
        version (str): Data Dragon version
        
    Returns:
        dict: TFT item data
    """
    try:
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/tft-item.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching item data: {e}")
        return None

def fetch_traits_data(version):
    """
    Fetch TFT trait data from Data Dragon.
    
    Args:
        version (str): Data Dragon version
        
    Returns:
        dict: TFT trait data
    """
    try:
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/tft-trait.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching trait data: {e}")
        return None

def fetch_augments_data(version):
    """
    Fetch TFT augment data from Data Dragon if available.
    Note: Augments might not be available through standard Data Dragon endpoints.
    
    Args:
        version (str): Data Dragon version
        
    Returns:
        dict: TFT augment data or None if not available
    """
    try:
        # Try to fetch augments - this might not work as they're not always available in ddragon
        url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/tft-augment.json"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching augment data: {e} - Augments might not be available via Data Dragon")
        return None

def process_champions_data(champions_data, version):
    """
    Process champion data into format for database storage.
    
    Args:
        champions_data (dict): Raw champion data from Data Dragon
        version (str): Data Dragon version
        
    Returns:
        list: Processed champion entries
    """
    if not champions_data or 'data' not in champions_data:
        return []
    
    processed_champions = []
    
    for champ_id, champ_data in champions_data['data'].items():
        champion = {
            'champion_id': champ_id,
            'name': champ_data.get('name', ''),
            'tier': int(champ_data.get('tier', 0)),
            'cost': int(champ_data.get('tier', 0)),  # Cost is same as tier in TFT
            'image_url': f"https://ddragon.leagueoflegends.com/cdn/{version}/img/tft-champion/{champ_data.get('image', {}).get('full', '')}",
            'traits': ', '.join(champ_data.get('traits', [])),
            'version': version,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        processed_champions.append(champion)
    
    return processed_champions

def process_tacticians_data(tacticians_data, version):
    """
    Process tactician (Little Legend/Pet) data into format for database storage.
    
    Args:
        tacticians_data (dict): Raw tactician data from Data Dragon
        version (str): Data Dragon version
        
    Returns:
        list: Processed tactician entries
    """
    if not tacticians_data or 'data' not in tacticians_data:
        return []
    
    processed_tacticians = []
    
    for tact_id, tact_data in tacticians_data['data'].items():
        tactician = {
            'tactician_id': tact_id,
            'name': tact_data.get('name', ''),
            'species': tact_data.get('species', ''),
            'level': tact_data.get('level', 1),
            'image_url': f"https://ddragon.leagueoflegends.com/cdn/{version}/img/tft-tactician/{tact_data.get('image', {}).get('full', '')}",
            'version': version,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        processed_tacticians.append(tactician)
    
    return processed_tacticians

def process_items_data(items_data, version):
    """
    Process item data into format for database storage.
    
    Args:
        items_data (dict): Raw item data from Data Dragon
        version (str): Data Dragon version
        
    Returns:
        list: Processed item entries
    """
    if not items_data or 'data' not in items_data:
        return []
    
    processed_items = []
    
    for item_id, item_data in items_data['data'].items():
        item = {
            'item_id': item_id,
            'name': item_data.get('name', ''),
            'description': item_data.get('description', ''),
            'image_url': f"https://ddragon.leagueoflegends.com/cdn/{version}/img/tft-item/{item_data.get('image', {}).get('full', '')}",
            'version': version,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        processed_items.append(item)
    
    return processed_items

def process_traits_data(traits_data, version):
    """
    Process trait data into format for database storage.
    
    Args:
        traits_data (dict): Raw trait data from Data Dragon
        version (str): Data Dragon version
        
    Returns:
        list: Processed trait entries
    """
    if not traits_data or 'data' not in traits_data:
        return []
    
    processed_traits = []
    
    for trait_id, trait_data in traits_data['data'].items():
        trait = {
            'trait_id': trait_id,
            'name': trait_data.get('name', ''),
            'description': trait_data.get('description', ''),
            'image_url': f"https://ddragon.leagueoflegends.com/cdn/{version}/img/tft-trait/{trait_data.get('image', {}).get('full', '')}",
            'version': version,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        processed_traits.append(trait)
    
    return processed_traits

def process_augments_data(augments_data, version):
    """
    Process augment data into format for database storage.
    
    Args:
        augments_data (dict): Raw augment data from Data Dragon
        version (str): Data Dragon version
        
    Returns:
        list: Processed augment entries
    """
    if not augments_data or 'data' not in augments_data:
        return []
    
    processed_augments = []
    
    for augment_id, augment_data in augments_data['data'].items():
        augment = {
            'augment_id': augment_id,
            'name': augment_data.get('name', ''),
            'description': augment_data.get('description', ''),
            'image_url': f"https://ddragon.leagueoflegends.com/cdn/{version}/img/tft-augment/{augment_data.get('image', {}).get('full', '')}",
            'tier': augment_data.get('tier', 0),
            'version': version,
            'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        processed_augments.append(augment)
    
    return processed_augments

def load_champions_to_sql(champions):
    """
    Load processed champion data into the database.
    
    Args:
        champions (list): List of processed champion entries
    """
    if not champions:
        print("No champion data to load")
        return
    
    # Connect to database
    conn = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT")),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )
    
    cursor = conn.cursor()
    
    try:
        # Create champion table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tft_champion (
            champion_id VARCHAR(100) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            tier INT NOT NULL,
            cost INT NOT NULL,
            image_url VARCHAR(255),
            traits TEXT,
            version VARCHAR(20),
            last_updated DATETIME
        )
        """)
        
        # Insert champions
        for champion in champions:
            cursor.execute("""
            INSERT INTO tft_champion 
            (champion_id, name, tier, cost, image_url, traits, version, last_updated)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            tier = VALUES(tier),
            cost = VALUES(cost),
            image_url = VALUES(image_url),
            traits = VALUES(traits),
            version = VALUES(version),
            last_updated = VALUES(last_updated)
            """, (
                champion['champion_id'],
                champion['name'],
                champion['tier'],
                champion['cost'],
                champion['image_url'],
                champion['traits'],
                champion['version'],
                champion['last_updated']
            ))
        
        conn.commit()
        print(f"Successfully loaded {len(champions)} champion entries")
        
    except Exception as e:
        print(f"Error loading champion data: {e}")
        conn.rollback()
    
    finally:
        cursor.close()
        conn.close()

def load_tacticians_to_sql(tacticians):
    """
    Load processed tactician data into the database.
    
    Args:
        tacticians (list): List of processed tactician entries
    """
    if not tacticians:
        print("No tactician data to load")
        return
    
    # Connect to database
    conn = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT")),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )
    
    cursor = conn.cursor()
    
    try:
        # Create tactician table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tft_tactician (
            tactician_id VARCHAR(100) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            species VARCHAR(50),
            level INT,
            image_url VARCHAR(255),
            version VARCHAR(20),
            last_updated DATETIME
        )
        """)
        
        # Insert tacticians
        for tactician in tacticians:
            cursor.execute("""
            INSERT INTO tft_tactician 
            (tactician_id, name, species, level, image_url, version, last_updated)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            species = VALUES(species),
            level = VALUES(level),
            image_url = VALUES(image_url),
            version = VALUES(version),
            last_updated = VALUES(last_updated)
            """, (
                tactician['tactician_id'],
                tactician['name'],
                tactician['species'],
                tactician['level'],
                tactician['image_url'],
                tactician['version'],
                tactician['last_updated']
            ))
        
        conn.commit()
        print(f"Successfully loaded {len(tacticians)} tactician entries")
        
    except Exception as e:
        print(f"Error loading tactician data: {e}")
        conn.rollback()
    
    finally:
        cursor.close()
        conn.close()

def load_items_to_sql(items):
    """
    Load processed item data into the database.
    
    Args:
        items (list): List of processed item entries
    """
    if not items:
        print("No item data to load")
        return
    
    # Connect to database
    conn = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT")),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )
    
    cursor = conn.cursor()
    
    try:
        # Create item table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tft_item (
            item_id VARCHAR(100) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            image_url VARCHAR(255),
            version VARCHAR(20),
            last_updated DATETIME
        )
        """)
        
        # Insert items
        for item in items:
            cursor.execute("""
            INSERT INTO tft_item 
            (item_id, name, description, image_url, version, last_updated)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            description = VALUES(description),
            image_url = VALUES(image_url),
            version = VALUES(version),
            last_updated = VALUES(last_updated)
            """, (
                item['item_id'],
                item['name'],
                item['description'],
                item['image_url'],
                item['version'],
                item['last_updated']
            ))
        
        conn.commit()
        print(f"Successfully loaded {len(items)} item entries")
        
    except Exception as e:
        print(f"Error loading item data: {e}")
        conn.rollback()
    
    finally:
        cursor.close()
        conn.close()

def load_traits_to_sql(traits):
    """
    Load processed trait data into the database.
    
    Args:
        traits (list): List of processed trait entries
    """
    if not traits:
        print("No trait data to load")
        return
    
    # Connect to database
    conn = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT")),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )
    
    cursor = conn.cursor()
    
    try:
        # Create trait table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tft_trait (
            trait_id VARCHAR(100) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            image_url VARCHAR(255),
            version VARCHAR(20),
            last_updated DATETIME
        )
        """)
        
        # Insert traits
        for trait in traits:
            cursor.execute("""
            INSERT INTO tft_trait 
            (trait_id, name, description, image_url, version, last_updated)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            description = VALUES(description),
            image_url = VALUES(image_url),
            version = VALUES(version),
            last_updated = VALUES(last_updated)
            """, (
                trait['trait_id'],
                trait['name'],
                trait['description'],
                trait['image_url'],
                trait['version'],
                trait['last_updated']
            ))
        
        conn.commit()
        print(f"Successfully loaded {len(traits)} trait entries")
        
    except Exception as e:
        print(f"Error loading trait data: {e}")
        conn.rollback()
    
    finally:
        cursor.close()
        conn.close()

def load_augments_to_sql(augments):
    """
    Load processed augment data into the database.
    
    Args:
        augments (list): List of processed augment entries
    """
    if not augments:
        print("No augment data to load")
        return
    
    # Connect to database
    conn = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT")),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )
    
    cursor = conn.cursor()
    
    try:
        # Create augment table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tft_augment (
            augment_id VARCHAR(100) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            image_url VARCHAR(255),
            tier INT,
            version VARCHAR(20),
            last_updated DATETIME
        )
        """)
        
        # Insert augments
        for augment in augments:
            cursor.execute("""
            INSERT INTO tft_augment 
            (augment_id, name, description, image_url, tier, version, last_updated)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            name = VALUES(name),
            description = VALUES(description),
            image_url = VALUES(image_url),
            tier = VALUES(tier),
            version = VALUES(version),
            last_updated = VALUES(last_updated)
            """, (
                augment['augment_id'],
                augment['name'],
                augment['description'],
                augment['image_url'],
                augment['tier'],
                augment['version'],
                augment['last_updated']
            ))
        
        conn.commit()
        print(f"Successfully loaded {len(augments)} augment entries")
        
    except Exception as e:
        print(f"Error loading augment data: {e}")
        conn.rollback()
    
    finally:
        cursor.close()
        conn.close()

def extract_match_companions(match_id, region="vn2"):
    """
    Extract companion (Little Legend/Pet) information from a specific match.
    
    Args:
        match_id (str): Match ID to retrieve
        region (str): Region/platform ID (e.g., "vn2", "kr", "jp1")
        
    Returns:
        list: List of player-companion mappings
    """
    try:
        api_key = os.environ.get("RIOT_API_KEY")
        if not api_key:
            print("Missing RIOT_API_KEY in environment variables")
            return []
            
        url = f"https://{region}.api.riotgames.com/tft/match/v1/matches/{match_id}?api_key={api_key}"
        response = requests.get(url)
        response.raise_for_status()
        
        match_data = response.json()
        companions = []
        
        # Extract companion data for each participant
        for participant in match_data.get('info', {}).get('participants', []):
            companion_data = participant.get('companion', {})
            if companion_data:
                companions.append({
                    'match_id': match_id,
                    'puuid': participant.get('puuid'),
                    'content_id': companion_data.get('content_ID'),
                    'skin_id': companion_data.get('skin_ID'),
                    'placement': participant.get('placement')
                })
        
        return companions
        
    except Exception as e:
        print(f"Error extracting match companion data: {e}")
        return []

def load_match_companions_to_sql(companions):
    """
    Load match companion data into the database.
    
    Args:
        companions (list): List of match companion entries
    """
    if not companions:
        print("No match companion data to load")
        return
    
    # Connect to database
    conn = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT")),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )
    
    cursor = conn.cursor()
    
    try:
        # Create match_companion table if it doesn't exist
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tft_match_companion (
            match_id VARCHAR(20),
            puuid VARCHAR(100),
            content_id VARCHAR(20),
            skin_id INT,
            placement INT,
            PRIMARY KEY (match_id, puuid)
        )
        """)
        
        # Insert match companions
        for companion in companions:
            cursor.execute("""
            INSERT INTO tft_match_companion 
            (match_id, puuid, content_id, skin_id, placement)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
            content_id = VALUES(content_id),
            skin_id = VALUES(skin_id),
            placement = VALUES(placement)
            """, (
                companion['match_id'],
                companion['puuid'],
                companion['content_id'],
                companion['skin_id'],
                companion['placement']
            ))
        
        conn.commit()
        print(f"Successfully loaded {len(companions)} match companion entries")
        
    except Exception as e:
        print(f"Error loading match companion data: {e}")
        conn.rollback()
    
    finally:
        cursor.close()
        conn.close()

def run_static_data_etl():
    """
    Run the complete static data ETL pipeline.
    """
    # Get latest version
    version = get_latest_version()
    if not version:
        print("Failed to get latest version, aborting pipeline")
        return
    
    print(f"Using Data Dragon version: {version}")
    
    # Champions ETL
    print("\n--- Processing Champions ---")
    champions_data = fetch_champions_data(version)
    if champions_data:
        processed_champions = process_champions_data(champions_data, version)
        load_champions_to_sql(processed_champions)
    
    # Tacticians (Little Legends/Pets) ETL
    print("\n--- Processing Tacticians (Little Legends) ---")
    tacticians_data = fetch_tacticians_data(version)
    if tacticians_data:
        processed_tacticians = process_tacticians_data(tacticians_data, version)
        load_tacticians_to_sql(processed_tacticians)
    
    # Items ETL
    print("\n--- Processing Items ---")
    items_data = fetch_items_data(version)
    if items_data:
        processed_items = process_items_data(items_data, version)
        load_items_to_sql(processed_items)
    
    # Traits ETL
    print("\n--- Processing Traits ---")
    traits_data = fetch_traits_data(version)
    if traits_data:
        processed_traits = process_traits_data(traits_data, version)
        load_traits_to_sql(processed_traits)
    
    # Augments ETL
    print("\n--- Processing Augments ---")
    augments_data = fetch_augments_data(version)
    if augments_data:
        processed_augments = process_augments_data(augments_data, version)
        load_augments_to_sql(processed_augments)
    
    print("\nStatic data ETL completed successfully!")

if __name__ == "__main__":
    run_static_data_etl()
