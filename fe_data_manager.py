from fe_models import User, PlayerStats, MatchHistory, Champion, ChampionPick, LPHistory
from fe_app import db
from sqlalchemy import func
import logging

def get_user_stats(user_id):
    """Get comprehensive user statistics"""
    user = User.query.get(user_id)
    if not user:
        return None
    
    # Get or create player stats
    stats = PlayerStats.query.filter_by(user_id=user_id).first()
    if not stats:
        stats = PlayerStats(user_id=user_id)
        db.session.add(stats)
        db.session.commit()
    
    # Update stats from match history
    stats.calculate_stats_from_matches()
    db.session.commit()
    
    return stats

def get_recent_matches(user_id, limit=20):
    """Get recent matches for a user"""
    return MatchHistory.query.filter_by(user_id=user_id)\
                           .order_by(MatchHistory.played_at.desc())\
                           .limit(limit).all()

def get_top_champions(user_id, limit=5):
    """Get most played champions for a user"""
    # Query champion picks with champion data
    top_champions = db.session.query(
        Champion.name,
        Champion.cost,
        Champion.image_url,
        func.count(ChampionPick.id).label('pick_count')
    ).join(
        ChampionPick, Champion.id == ChampionPick.champion_id
    ).join(
        MatchHistory, ChampionPick.match_id == MatchHistory.id
    ).filter(
        MatchHistory.user_id == user_id
    ).group_by(
        Champion.id
    ).order_by(
        func.count(ChampionPick.id).desc()
    ).limit(limit).all()
    
    # Convert to list of dictionaries for easier template access
    result = []
    for champ in top_champions:
        result.append({
            'name': champ.name,
            'cost': champ.cost,
            'image_url': champ.image_url or f'https://ddragon.leagueoflegends.com/cdn/14.1.1/img/champion/{champ.name}.png',
            'pick_count': champ.pick_count
        })
    
    return result

def get_lp_history(user_id, limit=100):
    """Get LP history for charts"""
    lp_records = LPHistory.query.filter_by(user_id=user_id)\
                               .order_by(LPHistory.recorded_at.asc())\
                               .limit(limit).all()
    
    # Convert to dictionary format for JSON serialization
    return [
        {
            'lp_value': record.lp_value,
            'tier': record.tier,
            'rank': record.rank,
            'recorded_at': record.recorded_at.isoformat()
        }
        for record in lp_records
    ]

def calculate_placement_distribution(user_id, limit=50):
    """Calculate placement distribution for charts"""
    matches = get_recent_matches(user_id, limit)
    distribution = [0] * 8
    
    for match in matches:
        if 1 <= match.placement <= 8:
            distribution[match.placement - 1] += 1
    
    return distribution

def get_match_details(match_id):
    """Get detailed match information including champion picks"""
    match = MatchHistory.query.get(match_id)
    if not match:
        return None
    
    # Get champion picks for this match
    champion_picks = db.session.query(
        ChampionPick, Champion
    ).join(
        Champion, ChampionPick.champion_id == Champion.id
    ).filter(
        ChampionPick.match_id == match_id
    ).all()
    
    return {
        'match': match,
        'champions': [{'pick': pick, 'champion': champion} for pick, champion in champion_picks]
    }

def update_user_lp_history(user_id, lp_value, tier, rank=None):
    """Add entry to LP history"""
    lp_entry = LPHistory(
        user_id=user_id,
        lp_value=lp_value,
        tier=tier,
        rank=rank
    )
    db.session.add(lp_entry)
    db.session.commit()
    
    return lp_entry

def get_leaderboard_stats():
    """Get statistics for leaderboard display"""
    # This would typically fetch from Riot API
    # For now, return sample data structure
    return {
        'total_players': 1000000,
        'last_updated': 'Just now',
        'season': 'Set 12'
    }
