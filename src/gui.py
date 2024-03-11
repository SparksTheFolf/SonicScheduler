import tkinter as tk
from tkinter import ttk
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from scheduler import Scheduler

class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.scheduler = Scheduler()
        self.create_widgets()


    def create_widgets(self):
        # Create labels
        self.label_songs = tk.Label(self.master, text="Songs:")
        self.label_talk_time = tk.Label(self.master, text="Talk Time:")
        self.label_ad_time = tk.Label(self.master, text="Ad Time:")
        self.label_schedule = tk.Label(self.master, text="Scheduled Items:")

        # Create entry fields
        self.entry_songs = tk.Entry(self.master)
        self.entry_talk_time = tk.Entry(self.master)
        self.entry_ad_time = tk.Entry(self.master)

        # Create buttons
        self.button_add_song = tk.Button(self.master, text="Add Song", command=self.add_song)
        self.button_schedule_show = tk.Button(self.master, text="Schedule Show", command=self.schedule_show)

        # Create listbox to display scheduled items
        self.listbox_schedule = tk.Listbox(self.master, width=50)

        # Grid layout
        self.label_songs.grid(row=0, column=0, sticky="w")
        self.entry_songs.grid(row=0, column=1)
        self.button_add_song.grid(row=0, column=2)
        self.label_talk_time.grid(row=1, column=0, sticky="w")
        self.entry_talk_time.grid(row=1, column=1)
        self.label_ad_time.grid(row=2, column=0, sticky="w")
        self.entry_ad_time.grid(row=2, column=1)
        self.button_schedule_show.grid(row=3, column=0, columnspan=3)
        self.label_schedule.grid(row=4, column=0, sticky="w")
        self.listbox_schedule.grid(row=5, column=0, columnspan=3)

        client_credentials_manager = SpotifyClientCredentials(client_id='YOUR_CLIENT_ID', client_secret='YOUR_CLIENT_SECRET')
        self.spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def add_song(self):
        song_info = self.entry_songs.get()
        # Call Spotify API to search for the song
        results = self.spotify.search(q=song_info, limit=1)
        if results['tracks']['items']:
            song = results['tracks']['items'][0]
            artist = song['artists'][0]['name']
            song_name = song['name']
            duration_ms = song['duration_ms']
            duration_min = duration_ms / 60000
            self.listbox_schedule.insert(tk.END, f"Song: {song_name} - Artist: {artist} - Duration: {duration_min:.2f} min")
        else:
            self.listbox_schedule.insert(tk.END, "Song not found!")

    def schedule_show(self):
        # Get talk time and ad time from entry fields
        talk_time = self.entry_talk_time.get()
        ad_time = self.entry_ad_time.get()
        # Schedule show with talk time and ad time
        self.listbox_schedule.insert(tk.END, f"Talk Time: {talk_time}")
        self.listbox_schedule.insert(tk.END, f"Ad Time: {ad_time}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    app.mainloop()
