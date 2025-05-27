from app import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import re
import random

class User(db.Model):
    """User model for storing user authentication and Riot ID information"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    riot_name = db.Column(db.String(80), nullable=False)
    riot_tag = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    player_stats = db.relationship('PlayerStats', backref='user', lazy=True, cascade='all, delete-orphan', uselist=False)
    match_history = db.relationship('MatchHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set the user's password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the stored hash"""
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def validate_riot_id(riot_id):
        """Validate Riot ID format (username#tag)"""
        RIOTID_PATTERN = re.compile(r"^.+#[A-Za-z0-9]{1,10}$")
        return RIOTID_PATTERN.match(riot_id) is not None
    
    @property
    def riot_id(self):
        """Get full Riot ID in username#tag format"""
        return f"{self.riot_name}#{self.riot_tag}"
    
    def __repr__(self):
        return f'<User {self.username} - {self.riot_id}>'

class PlayerStats(db.Model):
    """Model for storing current player statistics and rank information"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Current rank information
    tier = db.Column(db.String(20), default='UNRANKED')
    rank = db.Column(db.String(5), default='IV')
    league_points = db.Column(db.Integer, default=0)
    
    # Win/Loss statistics
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    
    # Additional stats
    games_played = db.Column(db.Integer, default=0)
    average_placement = db.Column(db.Float, default=0.0)
    top_four_rate = db.Column(db.Float, default=0.0)
    
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def win_rate(self):
        """Calculate win rate percentage"""
        total_games = self.wins + self.losses
        if total_games == 0:
            return 0.0
        return round((self.wins / total_games) * 100, 1)
    
    @property
    def rank_display(self):
        """Get formatted rank display"""
        if self.tier == 'UNRANKED':
            return 'Unranked'
        elif self.tier in ['MASTER', 'GRANDMASTER', 'CHALLENGER']:
            return f"{self.tier.title()} {self.league_points} LP"
        else:
            return f"{self.tier.title()} {self.rank} ({self.league_points} LP)"
    
    def calculate_stats_from_matches(self):
        """Calculate stats from user's match history"""
        matches = MatchHistory.query.filter_by(user_id=self.user_id).order_by(MatchHistory.played_at.desc()).limit(20).all()
        
        if matches:
            # Calculate average placement
            total_placement = sum(match.placement for match in matches)
            self.average_placement = round(total_placement / len(matches), 1)
            
            # Calculate top 4 rate
            top_four_matches = sum(1 for match in matches if match.placement <= 4)
            self.top_four_rate = round((top_four_matches / len(matches)) * 100, 1)
            
            # Update games played
            all_matches = MatchHistory.query.filter_by(user_id=self.user_id).count()
            self.games_played = all_matches
            
            # Calculate wins/losses (top 4 is win)
            self.wins = sum(1 for match in MatchHistory.query.filter_by(user_id=self.user_id).all() if match.placement <= 4)
            self.losses = all_matches - self.wins
    
    def __repr__(self):
        return f'<PlayerStats {self.user.username} - {self.rank_display}>'

class MatchHistory(db.Model):
    """Model for storing individual match results"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    match_id = db.Column(db.String(50), nullable=False)
    placement = db.Column(db.Integer, nullable=False)
    lp_change = db.Column(db.Integer, default=0)
    lp_after = db.Column(db.Integer, nullable=False)
    
    # Match details
    game_length = db.Column(db.Integer, default=0)
    game_version = db.Column(db.String(20), default='14.1')
    
    played_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    champion_picks = db.relationship('ChampionPick', backref='match', lazy=True, cascade='all, delete-orphan')
    
    @property
    def is_win(self):
        """Consider top 4 placements as wins"""
        return self.placement <= 4
    
    @property
    def game_length_formatted(self):
        """Format game length in MM:SS"""
        minutes = self.game_length // 60
        seconds = self.game_length % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def __repr__(self):
        return f'<Match {self.match_id} - Placement: {self.placement}>'

class Champion(db.Model):
    """Model for TFT champion information"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    
    # Champion stats
    health = db.Column(db.Integer, default=0)
    attack_damage = db.Column(db.Integer, default=0)
    armor = db.Column(db.Integer, default=0)
    magic_resist = db.Column(db.Integer, default=0)
    
    # Visual
    image_url = db.Column(db.String(200))
    
    # Relationships
    picks = db.relationship('ChampionPick', backref='champion', lazy=True)
    
    def __repr__(self):
        return f'<Champion {self.name} ({self.cost} cost)>'

class ChampionPick(db.Model):
    """Model for tracking champion picks in matches"""
    id = db.Column(db.Integer, primary_key=True)
    match_id = db.Column(db.Integer, db.ForeignKey('match_history.id'), nullable=False)
    champion_id = db.Column(db.Integer, db.ForeignKey('champion.id'), nullable=False)
    
    star_level = db.Column(db.Integer, default=1)
    items = db.Column(db.Text)  # JSON string of items
    
    def __repr__(self):
        return f'<ChampionPick {self.champion.name} - {self.star_level}*>'

class LPHistory(db.Model):
    """Model for tracking LP changes over time"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    lp_value = db.Column(db.Integer, nullable=False)
    tier = db.Column(db.String(20), nullable=False)
    rank = db.Column(db.String(5))
    
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign key relationship
    user_lp = db.relationship('User', backref='lp_history', lazy=True)
    
    def __repr__(self):
        return f'<LPHistory {self.user.username} - {self.lp_value} LP at {self.recorded_at}>'

class LeaderboardEntry(db.Model):
    """Model for storing leaderboard data for top players"""
    id = db.Column(db.Integer, primary_key=True)
    player_name = db.Column(db.String(80), nullable=False)
    tagline = db.Column(db.String(10), nullable=False)
    tier = db.Column(db.String(20), nullable=False)
    rank = db.Column(db.String(5))
    league_points = db.Column(db.Integer, nullable=False)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    games_played = db.Column(db.Integer, default=0)
    average_placement = db.Column(db.Float, default=0.0)
    win_rate = db.Column(db.Float, default=0.0)
    rank_position = db.Column(db.Integer, nullable=False)
    
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    @property
    def riot_id(self):
        return f"{self.player_name}#{self.tagline}"
    
    @property
    def rank_display(self):
        if self.tier in ['MASTER', 'GRANDMASTER', 'CHALLENGER']:
            return f"{self.tier.title()} {self.league_points} LP"
        else:
            return f"{self.tier.title()} {self.rank} ({self.league_points} LP)"
    
    def __repr__(self):
        return f'<LeaderboardEntry #{self.rank_position} {self.player_name}#{self.tagline}>'
