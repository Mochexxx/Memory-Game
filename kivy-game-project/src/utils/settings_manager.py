import os
import json
from kivy.utils import platform

def get_settings_dir():
    """Get the appropriate directory for storing settings based on platform"""
    if platform == 'android':
        from android.storage import app_storage_path
        return app_storage_path()
    elif platform == 'ios':
        from pyobjus import autoclass
        NSSearchPathForDirectoriesInDomains = autoclass('NSSearchPathForDirectoriesInDomains')
        NSDocumentDirectory = 1
        NSUserDomainMask = 1
        paths = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, True)
        return paths.objectAtIndex_(0)
    else:
        # Windows, macOS, Linux
        return os.path.join(os.path.expanduser('~'), '.memory_game')

def get_settings_file():
    """Get the full path to the settings file"""
    settings_dir = get_settings_dir()
    
    # Make sure the directory exists
    if not os.path.exists(settings_dir):
        os.makedirs(settings_dir)
    
    return os.path.join(settings_dir, 'settings.json')

def load_settings():
    """Load settings from file or return defaults if no file exists"""
    settings_file = get_settings_file()
    
    # Default settings
    default_settings = {
        'fullscreen': True,
        'text_size_factor': 1.0,
        'sound_effects': True,
        'music': True,
        'music_volume': 0.5,
        'score_display': True,
        'timer_display': True,
        'colorblind_mode': False,
        'audio_assist': False,
        'visual_feedback': True,
        'easy_mode': False,
    }
    
    try:
        if os.path.exists(settings_file):
            with open(settings_file, 'r') as f:
                saved_settings = json.load(f)
                # Merge with defaults in case new settings were added
                for key, value in default_settings.items():
                    if key not in saved_settings:
                        saved_settings[key] = value
                return saved_settings
    except Exception as e:
        print(f"Error loading settings: {e}")
    
    # Return defaults if file doesn't exist or there was an error
    return default_settings

def save_settings(settings):
    """Save settings to file"""
    settings_file = get_settings_file()
    
    try:
        with open(settings_file, 'w') as f:
            json.dump(settings, f)
        return True
    except Exception as e:
        print(f"Error saving settings: {e}")
        return False
