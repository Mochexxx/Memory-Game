import os
import random
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

class MusicManager:
    def __init__(self):
        self.current_music = None
        self.music_files = []
        self.volume = 1.0
        self.enabled = True
        # Update path to use correct case and structure
        self.music_folder = os.path.join("C:", os.sep, "Users", "pedro", "Documents", "GitHub", "IPC_24-25", "Items_Jogo", "Musicas_No_Copyright")
        print(f"Music folder path: {self.music_folder}")
        self.load_music_files()
        self.schedule = None
    
    def load_music_files(self):
        """Load all music files from the music folder"""
        print(f"Attempting to load music from: {self.music_folder}")
        
        if os.path.exists(self.music_folder):
            print(f"Music folder exists. Checking contents...")
            
            # List all files in the directory
            all_files = os.listdir(self.music_folder)
            print(f"All files in directory: {all_files}")
            
            # Filter music files
            self.music_files = [
                os.path.join(self.music_folder, f) 
                for f in all_files 
                if f.lower().endswith(('.mp3', '.wav', '.ogg'))
            ]
            
            if self.music_files:
                print(f"Found {len(self.music_files)} music files: {[os.path.basename(f) for f in self.music_files]}")
            else:
                print(f"No music files (mp3, wav, ogg) found in {self.music_folder}")
        else:
            print(f"ERROR: Music folder not found: {self.music_folder}")
            # Try to check if parent directories exist
            parent_dir = os.path.dirname(self.music_folder)
            print(f"Checking if parent directory exists: {parent_dir}")
            if os.path.exists(parent_dir):
                print(f"Parent directory exists. Contents: {os.listdir(parent_dir)}")
            else:
                print(f"Parent directory does not exist.")
    
    def play_random(self):
        """Start playing a random music track"""
        if not self.enabled:
            print("Music is disabled. Not playing.")
            return False
        
        if not self.music_files:
            print("No music files available to play.")
            return False
        
        self.stop()  # Stop any currently playing music
        
        try:
            random_music_file = random.choice(self.music_files)
            print(f"Selected random music file: {os.path.basename(random_music_file)}")
            return self.play(random_music_file)
        except Exception as e:
            print(f"Error in play_random: {e}")
            return False
    
    def play(self, music_file):
        """Play a specific music file"""
        if not self.enabled:
            print("Music is disabled. Not playing.")
            return False
        
        try:
            print(f"Attempting to load and play: {os.path.basename(music_file)}")
            self.current_music = SoundLoader.load(music_file)
            
            if self.current_music:
                self.current_music.volume = self.volume
                print(f"Playing music with volume {self.volume}")
                self.current_music.play()
                self.current_music.bind(on_stop=self.on_music_end)
                print(f"Success! Now playing: {os.path.basename(music_file)}")
                return True
            else:
                print(f"Failed to load music: {music_file}")
                return False
        except Exception as e:
            print(f"Error playing music: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def on_music_end(self, instance):
        """Called when a track finishes playing"""
        if self.enabled:
            # Schedule starting the next song with a small delay
            self.schedule = Clock.schedule_once(lambda dt: self.play_random(), 1)
    
    def stop(self):
        """Stop the current music"""
        if self.current_music:
            if self.current_music.state == 'play':
                self.current_music.stop()
            self.current_music = None
        
        if self.schedule:
            self.schedule.cancel()
            self.schedule = None
    
    def set_enabled(self, enabled):
        """Enable or disable music"""
        # Only make changes if the enabled state is changing
        if self.enabled != enabled:
            print(f"Music enabled state changing: {self.enabled} -> {enabled}")
            self.enabled = enabled
            
            if enabled:
                # Start playing since we're turning music on
                print("Starting music playback")
                self.play_random()
            else:
                # Stop playing since we're turning music off
                print("Stopping music playback")
                self.stop()
        else:
            print(f"Music enabled state unchanged: {enabled}")
    
    def set_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        self.volume = max(0, min(1, volume))
        if self.current_music:
            print(f"Updating music volume to {self.volume}")
            self.current_music.volume = self.volume
