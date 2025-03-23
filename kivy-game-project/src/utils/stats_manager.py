import os
import json
from utils.settings_manager import get_settings_dir

def get_stats_file():
    """Get the full path to the stats file"""
    settings_dir = get_settings_dir()
    
    # Make sure the directory exists
    if not os.path.exists(settings_dir):
        os.makedirs(settings_dir)
    
    return os.path.join(settings_dir, 'stats.json')

def load_stats():
    """Load statistics from file or return defaults if no file exists"""
    stats_file = get_stats_file()
    
    # Default stats
    default_stats = {
        'games_played': 0,
        'best_score': 0,
        'total_time': 0,  # in seconds
        'pairs_matched': 0,
        'best_times': {}  # dictionary mapping theme_difficulty to best time
    }
    
    try:
        if os.path.exists(stats_file):
            with open(stats_file, 'r') as f:
                saved_stats = json.load(f)
                # Merge with defaults in case new stats were added
                for key, value in default_stats.items():
                    if key not in saved_stats:
                        saved_stats[key] = value
                return saved_stats
    except Exception as e:
        print(f"Error loading stats: {e}")
    
    # Return defaults if file doesn't exist or there was an error
    return default_stats

def save_stats(stats):
    """Save statistics to file"""
    stats_file = get_stats_file()
    
    try:
        with open(stats_file, 'w') as f:
            json.dump(stats, f)
        return True
    except Exception as e:
        print(f"Error saving stats: {e}")
        return False

def update_stats(game_data):
    """Update statistics based on game results"""
    stats = load_stats()
    
    # Update games played
    stats['games_played'] += 1
    
    # Update best score if applicable
    if game_data.get('score', 0) > stats['best_score']:
        stats['best_score'] = game_data['score']
    
    # Update total time
    stats['total_time'] += game_data.get('time', 0)
    
    # Update pairs matched
    stats['pairs_matched'] += game_data.get('pairs_matched', 0)
    
    # Update best time for this theme/difficulty if applicable
    theme_diff_key = f"{game_data.get('theme', 'default')}_{game_data.get('difficulty', 0)}"
    current_time = game_data.get('time', 0)
    
    if current_time > 0:  # Only consider positive times
        if theme_diff_key not in stats['best_times'] or current_time < stats['best_times'][theme_diff_key]:
            stats['best_times'][theme_diff_key] = current_time
            print(f"New best time for {theme_diff_key}: {current_time}s")
    
    # Save updated stats
    success = save_stats(stats)
    if success:
        print("Statistics saved successfully")
    else:
        print("Failed to save statistics")
    
    return stats

def format_time(seconds):
    """Format seconds into a human-readable time string"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60
    
    if hours > 0:
        return f"{hours}h {minutes}m"
    elif minutes > 0:
        return f"{minutes}m {remaining_seconds}s"
    else:
        return f"{remaining_seconds}s"
