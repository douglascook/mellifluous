import base64
import json
import os
import pathlib
import sys
from datetime import datetime
from typing import Any

import requests


class SpotifyClient:
    token_endpoint = "https://accounts.spotify.com/api/token"
    user_endpoint = "https://api.spotify.com/v1/users"
    playlist_endpoint = "https://api.spotify.com/v1/playlists"

    def __init__(self) -> None:
        self.token = self.get_auth_token()
        self.data_dir = pathlib.Path("./data")

    def download_playlist_tracks_metadata(self, user: str, playlist_name: str) -> None:
        playlist_id = self.get_playlist_id(user, playlist_name)
        endpoint = f"{self.playlist_endpoint}/{playlist_id}"

        now = datetime.now().isoformat(timespec="seconds")
        output_path = self.data_dir / f"{playlist_name}_{now}.jsonl"

        data = self.get_authorised(endpoint)
        next_page = data["tracks"]["href"]
        while next_page:
            print(f"Downloading {next_page}")
            page = self.get_authorised(next_page)

            with output_path.open("a") as f_out:
                f_out.writelines((f"{json.dumps(t)}\n" for t in page["items"]))

            next_page = page["next"]

    def get_playlist_id(self, user: str, playlist_name: str) -> str:
        endpoint = f"{self.user_endpoint}/{user}/playlists"
        data = self.get_authorised(endpoint)

        for playlist in data["items"]:
            if playlist["name"] == playlist_name:
                return str(playlist["id"])

        raise ValueError(
            f"Could not find playlist named {playlist_name} for user {user}"
        )

    def get_authorised(self, endpoint: str) -> dict[str, Any]:
        """Make an authorised GET request to the given endpoint."""
        response = requests.get(
            endpoint, headers={"Authorization": f"Bearer {self.token}"}
        )
        response.raise_for_status()
        data = response.json()
        # Why isn't this typed properly in the stubs?
        assert isinstance(data, dict)
        return data

    @classmethod
    def get_auth_token(cls) -> str:
        """Return authentication token generated using client credentials flow.

        This authentication method does not give access to user data endpoints.
        """

        response = requests.post(
            cls.token_endpoint,
            headers=cls.build_auth_header(),
            data={"grant_type": "client_credentials"},
        )
        response.raise_for_status()

        token: str = response.json()["access_token"]
        return token

    @staticmethod
    def build_auth_header() -> dict[str, str]:
        """Return header containing base64 encoded Spotify credentials."""
        try:
            client_id = os.environ["SPOTIFY_CLIENT_ID"]
            client_secret = os.environ["SPOTIFY_CLIENT_SECRET"]
            creds = f"{client_id}:{client_secret}"
        except KeyError as err:
            raise RuntimeError("Missing Spotify credentials") from err

        base64_creds = base64.standard_b64encode(creds.encode()).decode()
        return {"Authorization": f"Basic {base64_creds}"}


if __name__ == "__main__":
    _, user, playlist = sys.argv
    print(f"Downloading {playlist} owned by {user}")

    client = SpotifyClient()
    client.download_playlist_tracks_metadata(user, playlist)
