from flask import render_template, request, redirect, url_for, flash, session, jsonify
from fe_app import app, db
from fe_models import User, PlayerStats, MatchHistory, Champion, ChampionPick, LPHistory, LeaderboardEntry
from fe_utils import login_required, get_placement_color, calculate_average_placement
from fe_data_manager import get_user_stats, get_recent_matches, get_top_champions, get_lp_history
import logging

@app.route('/')
def index():
    """Homepage with leaderboard and welcome section"""
    # Get top 50 players from leaderboard
    top_players = LeaderboardEntry.query.order_by(LeaderboardEntry.rank_position).limit(50).all()
    
    return render_template('index.html', top_players=top_players)

@app.route('/leaderboard')
def leaderboard():
    """Full leaderboard page"""
    top_players = LeaderboardEntry.query.order_by(LeaderboardEntry.rank_position).limit(100).all()
    return render_template('leaderboard.html', top_players=top_players)

@app.route('/player/<player_name>/<tagline>')
def player_detail(player_name, tagline):
    """View detailed stats for a specific player"""
    # Check if this is a registered user (search by both exact match and player name)
    user = User.query.filter_by(riot_name=player_name, riot_tag=tagline).first()
    if not user:
        # Try searching with spaces removed from player name (handle URL encoding)
        user = User.query.filter(
            User.riot_name.like(f'%{player_name.replace("%20", " ")}%'),
            User.riot_tag == tagline
        ).first()
    
    if user and user.player_stats:
        # Registered user - show full stats
        stats = get_user_stats(user.id)
        recent_matches = get_recent_matches(user.id, limit=20)
        top_champions = get_top_champions(user.id)
        lp_history = get_lp_history(user.id)
        
        # Calculate placement distribution for last 20 matches
        placement_dist = [0] * 8
        recent_placements = []
        
        for match in recent_matches:
            if match.placement <= 8:
                placement_dist[match.placement - 1] += 1
                recent_placements.append(match.placement)
        
        return render_template('player_detail.html', 
                             user=user, 
                             stats=stats, 
                             recent_matches=recent_matches,
                             top_champions=top_champions,
                             lp_history=lp_history,
                             placement_distribution=placement_dist,
                             recent_placements=recent_placements[:20])
    else:
        # Check leaderboard entry
        leaderboard_entry = LeaderboardEntry.query.filter_by(
            player_name=player_name, 
            tagline=tagline
        ).first()
        
        if leaderboard_entry:
            return render_template('player_detail.html', 
                                 leaderboard_entry=leaderboard_entry,
                                 limited_view=True)
        else:
            flash('Player not found.', 'error')
            return redirect(url_for('leaderboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Welcome back!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        username = request.form['username']
        riot_id = request.form['riot_id']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
        if not User.validate_riot_id(riot_id):
            flash('Invalid Riot ID format. Use format: username#tag', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('register.html')
        
        # Check if username already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return render_template('register.html')
        
        # Parse Riot ID
        riot_name, riot_tag = riot_id.split('#', 1)
        
        # Check if Riot ID already exists
        if User.query.filter_by(riot_name=riot_name, riot_tag=riot_tag).first():
            flash('This Riot ID is already registered.', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(username=username, riot_name=riot_name, riot_tag=riot_tag)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            
            # Create initial player stats
            stats = PlayerStats(user_id=user.id)
            db.session.add(stats)
            db.session.commit()
            
            # Auto-login after registration
            session['user_id'] = user.id
            session['username'] = user.username
            
            flash('Registration successful! Welcome to TFT Analyzer!', 'success')
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Registration error: {e}")
            flash('Registration failed. Please try again.', 'error')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """User logout"""
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard with comprehensive stats"""
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('login'))
    
    # Get user statistics
    stats = get_user_stats(user_id)
    recent_matches = get_recent_matches(user_id, limit=10)
    top_champions = get_top_champions(user_id)
    lp_history = get_lp_history(user_id)
    
    # Calculate placement distribution for charts
    all_matches = get_recent_matches(user_id, limit=50)
    placement_distribution = [0] * 8
    recent_placements = []
    
    # Get last 20 matches for placement grid
    last_20_matches = get_recent_matches(user_id, limit=20)
    for match in last_20_matches:
        if match.placement <= 8:
            recent_placements.append(match.placement)
    
    # Calculate placement distribution from last 50 matches
    for match in all_matches:
        if match.placement <= 8:
            placement_distribution[match.placement - 1] += 1
    
    return render_template('dashboard.html',
                         user=user,
                         stats=stats,
                         recent_matches=recent_matches,
                         top_champions=top_champions,
                         lp_history=lp_history,
                         placement_distribution=placement_distribution,
                         recent_placements=recent_placements)

@app.route('/refresh_data')
@login_required
def refresh_data():
    """Refresh user data (placeholder for future Riot API integration)"""
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    if user and user.player_stats:
        # Recalculate stats from existing matches
        user.player_stats.calculate_stats_from_matches()
        db.session.commit()
        flash('Stats updated successfully!', 'success')
    else:
        flash('Unable to refresh data at this time.', 'warning')
    
    return redirect(url_for('dashboard'))

@app.route('/api/lp_history/<int:user_id>')
@login_required
def api_lp_history(user_id):
    """API endpoint for LP history chart data"""
    if session['user_id'] != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    lp_history = get_lp_history(user_id)
    
    data = {
        'labels': [entry.recorded_at.strftime('%m/%d %H:%M') for entry in lp_history],
        'values': [entry.lp_value for entry in lp_history]
    }
    
    return jsonify(data)

@app.route('/api/placement_distribution/<int:user_id>')
@login_required
def api_placement_distribution(user_id):
    """API endpoint for placement distribution chart data"""
    if session['user_id'] != user_id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    matches = get_recent_matches(user_id, limit=50)
    distribution = [0] * 8
    
    for match in matches:
        if match.placement <= 8:
            distribution[match.placement - 1] += 1
    
    return jsonify({
        'labels': ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th'],
        'values': distribution
    })

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# Template filters
@app.template_filter('placement_color')
def placement_color_filter(placement):
    return get_placement_color(placement)

@app.template_filter('format_lp')
def format_lp_filter(lp_change):
    if lp_change > 0:
        return f"+{lp_change}"
    return str(lp_change)
