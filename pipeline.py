import csv
import json
import pathlib
import sys
from datetime import datetime

import spotify

DATA_DIR = pathlib.Path("./data")


def process_playlist(user: str, playlist: str) -> None:
    now = datetime.now().isoformat(timespec="seconds")
    client = spotify.SpotifyClient()

    print(f"Downloading {playlist} owned by {user}")
    raw_output = DATA_DIR / "raw" / f"{playlist}_{now}.jsonl"
    with raw_output.open("w") as raw_out:
        for track in client.get_playlist_tracks_metadata(user, playlist):
            raw_out.write(json.dumps(track) + "\n")

    print("Cleaning data")
    clean_output = DATA_DIR / "clean" / f"{playlist}_{now}.csv"
    with clean_output.open("w") as clean_out:
        parsed = (spotify.parse_track_metadata(l) for l in raw_output.open("r"))
        first = next(parsed)
        writer = csv.DictWriter(clean_out, fieldnames=first.keys())
        writer.writeheader()
        writer.writerow(first)
        writer.writerows(parsed)


if __name__ == "__main__":
    _, user, playlist = sys.argv
    process_playlist(user, playlist)
