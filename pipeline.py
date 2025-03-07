import json
import pathlib
import sqlite3
import sys
from datetime import datetime

import spotify

DATA_DIR = pathlib.Path("./data")
DB_PATH = "./db/mellifluous.sqlite3"


def download_playlist_metadata(user: str, playlist_name: str) -> None:
    client = spotify.SpotifyClient()

    playlist = client.get_playlist(user, playlist_name)
    playlist["timestamp"] = datetime.now().isoformat(timespec="seconds")
    playlist["user"] = user

    print(f"Downloading {playlist_name} owned by {user}")
    tracks = client.get_tracks_metadata(user, playlist["id"])

    with sqlite3.connect(DB_PATH, autocommit=False) as db:
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO playlist (name, user, timestamp, spotify_id, snapshot_id)
            VALUES (:name, :user, :timestamp, :id, :snapshot_id)
            RETURNING id
        """,
            playlist,
        )
        playlist_id = cursor.fetchone()[0]

        for track in tracks:
            cursor.execute(
                """
                INSERT INTO raw_track (playlist_id, metadata)
                VALUES (?, ?)
            """,
                (playlist_id, json.dumps(track).encode()),
            )

            cleaned = spotify.parse_track_metadata(track)
            cleaned["playlist_id"] = playlist_id
            cursor.execute(
                """
                INSERT INTO track (
                    playlist_id, name, link, isrc, artist, other_artists,
                    album, release_date, duration_ms, popularity, added_at)
                VALUES (
                    :playlist_id, :name, :link, :isrc, :artist, :other_artists,
                    :album, :release_date, :duration_ms, :popularity, :added_at
                )
            """,
                cleaned,
            )


if __name__ == "__main__":
    _, user, playlist = sys.argv
    download_playlist_metadata(user, playlist)
