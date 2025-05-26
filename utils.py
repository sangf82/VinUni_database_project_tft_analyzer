from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('You must be logged in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_rank_color(tier):
    """Get color for rank display"""
    colors = {
        'IRON': '#6b4423',
        'BRONZE': '#cd7f32',
        'SILVER': '#c0c0c0',
        'GOLD': '#ffd700',
        'PLATINUM': '#40e0d0',
        'DIAMOND': '#b9f2ff',
        'MASTER': '#9d4edd',
        'GRANDMASTER': '#ff6b6b',
        'CHALLENGER': '#f72585'
    }
    return colors.get(tier, '#6c757d')

def format_lp_change(lp_change):
    """Format LP change with + or - sign"""
    if lp_change > 0:
        return f"+{lp_change}"
    return str(lp_change)

def get_placement_color(placement):
    """Get Bootstrap color class for placement"""
    if placement <= 4:
        return 'success'  # Green for top 4
    elif placement <= 6:
        return 'warning'  # Yellow for 5-6
    else:
        return 'danger'   # Red for 7-8

def get_placement_badge_color(placement):
    """Get specific color for placement badges"""
    colors = {
        1: 'gold',      # Gold
        2: 'silver',    # Silver  
        3: 'bronze',    # Bronze
        4: 'success',   # Green
        5: 'info',      # Light blue
        6: 'warning',   # Yellow
        7: 'danger',    # Red
        8: 'dark'       # Dark
    }
    return colors.get(placement, 'secondary')

def calculate_average_placement(matches):
    """Calculate average placement from match list"""
    if not matches:
        return 0.0
    
    total_placement = sum(match.placement for match in matches)
    return round(total_placement / len(matches), 2)

def get_win_streak(matches):
    """Calculate current win streak (top 4 finishes)"""
    if not matches:
        return 0
    
    streak = 0
    for match in matches:
        if match.placement <= 4:
            streak += 1
        else:
            break
    
    return streak

def format_game_time(seconds):
    """Format game time from seconds to MM:SS"""
    minutes = seconds // 60
    seconds = seconds % 60
    return f"{minutes:02d}:{seconds:02d}"

def get_tier_order():
    """Get ordered list of tiers for comparison"""
    return ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER']

def compare_ranks(tier1, rank1, lp1, tier2, rank2, lp2):
    """Compare two ranks and return -1, 0, or 1"""
    tier_order = get_tier_order()
    
    tier1_index = tier_order.index(tier1) if tier1 in tier_order else -1
    tier2_index = tier_order.index(tier2) if tier2 in tier_order else -1
    
    if tier1_index != tier2_index:
        return 1 if tier1_index > tier2_index else -1
    
    # Same tier, compare ranks (only for non-master+ tiers)
    if tier1 not in ['MASTER', 'GRANDMASTER', 'CHALLENGER']:
        rank_order = ['IV', 'III', 'II', 'I']
        rank1_index = rank_order.index(rank1) if rank1 in rank_order else -1
        rank2_index = rank_order.index(rank2) if rank2 in rank_order else -1
        
        if rank1_index != rank2_index:
            return 1 if rank1_index > rank2_index else -1
    
    # Same tier and rank, compare LP
    if lp1 > lp2:
        return 1
    elif lp1 < lp2:
        return -1
    else:
        return 0
