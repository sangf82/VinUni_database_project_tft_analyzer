## Database Project: TFT Analyzer

### A. Description:

The Riot Games Analytics Pipeline addresses the challenge faced by players who want to make data-driven decisions but lack access to processed, actionable insights from vast amounts of game data. By ingesting match histories, player statistics, champion/unit performance, and meta trends, our pipeline transforms raw game data into strategic recommendations and performance analytics.

### B. Requirements:
#### B.1. Function Requirements:
- Extract and ingest game data from Riot Games API (match histories, player stats, champion/unit data)
- Process and transform raw data into structured formats suitable for analysis
- Identify patterns, correlations, and insights from game data
- Generate personalized recommendations based on player history and preferences
- Visualize key metrics and insights through dashboards
- Provide timely updates that reflect current game meta and patches
- Allow querying of historical data for trend analysis

#### B.2. Non-function Requirements:
- Scalability to handle large volumes of game data (thousands of matches per hour)
- Low latency for near real-time data processing and insights
- High availability and reliability (>99.5% uptime)
- Data security and compliance with Riot Games API terms of service
- Efficient resource utilization for cost-effectiveness
- Maintainability with clear documentation and modular design
- Configurability to support different game titles (LoL, TFT) and analysis parameters

### C. Planned Core Entities:
- Players: ID, username, rank, region, performance metrics
- Matches: Match ID, timestamp, duration, game version, participating players
- Champions/Units: ID, name, class, attributes, performance metrics
- Items: ID, name, attributes, usage statistics
- Team Compositions: Configuration, win rates, placement statistics
- Meta Trends: Patch information, popularity trends, success rates
- Recommendations: Player-specific suggestions, general strategy recommendations
- Analysis Results: Processed insights, statistical findings

### D. Tech Stack:
- Data Lake: MinIO(open-source S3-compatible object storage) or MongoDB for raw data storage
- Data Storage: MySQL (relational database for structured game data)
- Data Processing: Python with pandas/numpy for data analysis
- Data Orchestration: Apache Airflow for scheduling data updates and processing
- API Integration: Python requests/riotwatcher libraries for Riot Games API
- Backend: Flask for simple API to serve results
- Frontend: Basic HTML/CSS/JavaScript for visualization in web application
- Version Control: Git/GitHub
- Development: Jupyter Notebooks for exploratory analysis and prototyping

Detail Pipeline and Workflow of the System:
![alt text](images/pipeline.png)

### E. Team Members and Roles:
- Luong Tran Sang: Front-end Developer 
- Thai Minh Dung: Data Engineer
- Nguyen Hoang Long: Quality Assessment

### F. Project Timeline
The Gantt Chart show the detail workload of our team through the period time of project:

![alt text](images/timeline.png)



# TFT Analyzer - Teamfight Tactics Player Statistics App

A comprehensive TFT (Teamfight Tactics) web application providing in-depth player analytics, match history tracking, and competitive insights for players and strategists.

## Features

- **Player Dashboard**: Comprehensive statistics including rank, LP, win rate, and average placement
- **Match History**: MetaTFT-style expandable match rows with detailed team compositions
- **Leaderboard**: Top 30 VN players with rankings and statistics
- **Interactive Charts**: LP progression and placement distribution visualization
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **Dark Theme**: Professional TFT-inspired design

## Tech Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **Frontend**: Bootstrap 5, Chart.js, Font Awesome
- **Authentication**: Flask sessions with password hashing
- **Data Visualization**: Chart.js for interactive graphs

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- pip (Python package installer)

### 1. Clone or Download the Project

Download all project files to your local directory.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

#### Option A: Using PostgreSQL locally
1. Install PostgreSQL on your system
2. Create a new database:
```sql
CREATE DATABASE tft_analyzer;
```
3. Set environment variable:
```bash
export DATABASE_URL="postgresql://username:password@localhost:5432/tft_analyzer"
```

#### Option B: Using Replit (Recommended)
The app is configured to work seamlessly on Replit with their PostgreSQL service.

### 4. Environment Variables

Set the following environment variables:

```bash
export DATABASE_URL="your_postgresql_connection_string"
export SESSION_SECRET="your_secret_key_for_sessions"
```

### 5. Initialize the Database

The app will automatically create tables and populate sample data on first run.

### 6. Run the Application

```bash
# Development mode
python main.py

# Production mode with Gunicorn
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

The application will be available at `http://localhost:5000`

## Sample Users

The app comes with 30 pre-registered users representing top VN TFT players:

| Username | Password | Riot ID |
|----------|----------|---------|
| tln_yby1 | password123 | TLN YBY1#2024 |
| saigon_buffalo_shenlong | password123 | Saigon Buffalo Shenlong#VN01 |
| team_flash_noway | password123 | Team Flash NoWay#FL01 |
| ... | ... | ... |

All users use the password: `password123`

## Usage

1. **Homepage**: View the leaderboard and top players
2. **Login**: Use any of the sample usernames with password `password123`
3. **Dashboard**: View your personal statistics and match history
4. **Player Profiles**: Click on any player to view their detailed stats
5. **Match Details**: Click on match rows to expand team compositions

## Project Structure

```
tft-analyzer/
├── app.py              # Flask app configuration
├── main.py             # Application entry point
├── models.py           # Database models
├── routes.py           # Route handlers
├── data_manager.py     # Data processing utilities
├── sample_data.py      # Sample data initialization
├── utils.py            # Helper functions
├── static/             # CSS, JS, and assets
│   ├── css/
│   ├── js/
│   └── img/
├── templates/          # HTML templates
└── requirements.txt    # Python dependencies
```

## Key Features Explained

### Recent Games Component
- **MetaTFT-style interface** with expandable match rows
- **Champion previews** with cost-colored borders and star indicators
- **LP tracking** with visual up/down indicators
- **Team compositions** showing full champion builds

### Player Statistics
- **Rank progression** with tier and LP tracking
- **Performance metrics** including win rate and average placement
- **Interactive charts** for LP history and placement distribution
- **Match analytics** with detailed breakdowns

### Leaderboard System
- **Real-time rankings** of top players
- **Comprehensive stats** including games played and win rates
- **Player profiles** accessible with detailed match histories

## Customization

The app uses authentic League of Legends champion data and can be easily extended to:
- Connect to Riot Games API for live data
- Add more detailed item tracking
- Implement team composition analytics
- Add trait synergy calculations

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check DATABASE_URL environment variable
- Verify database credentials

### Missing Champion Images
- Champion images load from League of Legends CDN
- Fallback placeholders are provided for missing images

### Chart Display Issues
- Ensure JavaScript is enabled
- Check browser console for errors
- Verify Chart.js is loading properly

## Support

For issues or questions about the TFT Analyzer:
1. Check the troubleshooting section
2. Ensure all dependencies are installed
3. Verify database connection
4. Check browser console for JavaScript errors

---

**Built with**: Flask, PostgreSQL, Bootstrap, Chart.js
**Inspired by**: MetaTFT interface design
**Data Source**: League of Legends Data Dragon (Champion images)
