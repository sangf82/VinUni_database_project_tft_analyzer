import mysql.connector

def load_to_sql(data):

    # Connect to the database
    conn  = mysql.connector.connect(
        host="34.64.57.7",       # or your DB host
        user="root",   # replace with your MySQL username
        password="M@tkhau1",  # replace with your MySQL password
        database="tftdb"
    )

    # cursor = conn.cursor()

    # # Insert a new player
    # sql = """
    #     INSERT INTO Player (PlayerID, Dob, Gender)
    #     VALUES (%s, %s, %s)
    # """
    # player_data = ("P001TEST", "2000-01-15", "M")  # Example player

    # try:
    #     cursor.execute(sql, player_data)
    #     conn.commit()
    #     print("Player inserted successfully.")
    # except mysql.connector.Error as err:
    #     print("Error:", err)
    #     conn.rollback()

    # # Close the connection
    # cursor.close()
    # conn.close()

    # conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Get the data
    Player, Match, MatchPlayerInfo, MatchPlayerChampionInfo, Champion = data['Player'], data['Match'], data['MatchPlayerInfo'],  data['MatchPlayerChampionInfo'], data['Champion']

    # Insert player
    cursor.execute("""
        INSERT INTO Player (puuid, gameName, tagLine, lastLP, gamePLayed)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE gameName=VALUES(gameName), tagLine=VALUES(tagLine), lastLP=VALUES(lastLP), gamePLayed=VALUES(gamePLayed)
    """, (Player['puuid'], Player['gameName'], Player['tagLine'], Player['lastLP'], Player['gamePlayed']))

    # Insert champions
    for champ_id in Champion:
        cursor.execute("""
            INSERT IGNORE INTO Champion (ChampionID)
            VALUES (%s)
        """, (champ_id,))

    # Insert matches
    for m in Match:
        cursor.execute("""
            INSERT IGNORE INTO `Match` (MatchID, gameLength, endDatetime)
            VALUES (%s, %s, %s)
        """, (m['MatchID'], m['gameLength'], m['endDatetime']))

    # Insert match-player info
    for mpi in MatchPlayerInfo:
        cursor.execute("""
            INSERT IGNORE INTO MatchPlayerInfo (puuid, MatchID, placement, currentLP)
            VALUES (%s, %s, %s, %s)
        """, (mpi['puuid'], mpi['MatchID'], mpi['placement'], mpi['currentLP']))

    # Insert match-player-champion info
    for mpci in MatchPlayerChampionInfo:
        cursor.execute("""
            INSERT IGNORE INTO MatchPlayerChampionInfo (puuid, MatchID, ChampionID, quantity)
            VALUES (%s, %s, %s, %s)
        """, (mpci['puuid'], mpci['MatchID'], mpci['ChampionID'], mpci['quantity']))

    print("Sample data loaded successfully.")
    # Commit all changes
    conn.commit()

    # Close connection
    cursor.close()
    conn.close()
    
if __name__ == "__main__":
    sample_data = {
        'Player': {
            'puuid': 'player-1234',
            'gameName': 'TestPlayer',
            'tagLine': 'NA1',
            'lastLP': 100,
            'gamePlayed': 50
        },

        'Champion' : {'champ-1', 'champ-2'},

        'Match' : [
            {
                'MatchID': 'match-abc',
                'gameLength': 32.5,
                'endDatetime': '2024-05-10 13:45:00'
            }
        ],

        'MatchPlayerInfo' : [
            {
                'puuid': 'player-1234',
                'MatchID': 'match-abc',
                'placement': 1,
                'currentLP': 120
            }
        ],

        'MatchPlayerChampionInfo' : [
            {
                'puuid': 'player-1234',
                'MatchID': 'match-abc',
                'ChampionID': 'champ-1',
                'quantity': 2
            },
            {
                'puuid': 'player-1234',
                'MatchID': 'match-abc',
                'ChampionID': 'champ-2',
                'quantity': 1
            }
        ]
    }
    
    load_to_sql(sample_data)
    