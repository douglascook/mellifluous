import json
import pathlib
import sqlite3
import sys
from datetime import datetime

import spotify

DATA_DIR = pathlib.Path("./data")
DB_PATH = "./db/mellifluous.sqlite3"


def download_playlist_metadata(user: str, playlist: str) -> None:
    now = datetime.now().isoformat(timespec="seconds")
    client = spotify.SpotifyClient()
    print(f"Downloading {playlist} owned by {user}")
    tracks = client.get_playlist_tracks_metadata(user, playlist)

    with sqlite3.connect(DB_PATH, autocommit=False) as db:
        cursor = db.cursor()
        cursor.execute(
            """
            INSERT INTO playlist (name, user, timestamp)
            VALUES (?, ?, ?)
            RETURNING id
        """,
            (playlist, user, now),
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


if __name__ == "__main__":
    _, user, playlist = sys.argv
    download_playlist_metadata(user, playlist)
