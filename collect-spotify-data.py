import requests
import base64
import json

import pandas as pd


def get_spotify_track_id(track_name, artist_name, access_token):
    """
    :param track_name: Name of the track
    :param artist_name: name of the artist
    :param access_token: Spotify access token
    :return: Spotify track id
    """

    base_url = "https://api.spotify.com/v1/search"
    query_string = f"artist:{artist_name} track:{track_name}"

    params = {
        'q': query_string,
        'type': 'track',
        'access_token': access_token
    }

    return requests.get(base_url, params=params)


def read_access_token_from_file(access_token_file):
    """
    :param access_token_file: Text file with access token
    :return: Access token
    """
    # Get access token
    with open(access_token_file, "r") as f:
        access_token = f.read()

    return access_token


def generate_access_token_from_spotify(client_id_file, client_secret_file, access_token_file):
    """
    :param client_id_file: Text file that contains the client id
    :param client_secret_file: Text file that contains the secret id
    :param access_token_file: Access token written to this file
    """
    # Read the files to get client id and secret
    with open(client_id_file, "r") as f:
        client_id = f.readline().replace("\n", "")

    with open(client_secret_file, "r") as f:
        client_secret = f.readline().replace("\n", "")

    auth_string = base64.b64encode(bytes(f"{client_id}:{client_secret}", "utf-8"))
    auth_string_64 = auth_string.decode("utf-8")

    # Create data dictionary
    headers = {
        "Authorization": f"Basic {auth_string_64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    body = {
        'grant_type': 'client_credentials',
    }

    # Get access token and write to a file
    auth_url = 'https://accounts.spotify.com/api/token'
    auth_response = requests.post(auth_url, headers=headers, data=body)
    access_token = auth_response.json().get('access_token')

    # Write the access token to this file
    with open(access_token_file, "w") as f:
        f.write(access_token)


def get_spotify_track_audio_features(access_token, spotify_track_id):
    """
    :param access_token: Spotify access token
    :param spotify_track_id: ID of spotify track to read
    :return:
    """
    audio_feature_endpoint = f"https://api.spotify.com/v1/audio-features/{spotify_track_id}"

    return requests.get(audio_feature_endpoint, headers={"Authentication": f"Bearer {access_token}"})


if __name__ == "__main__":
    pass
    # while True:
    #     token = read_access_token_from_file("access_token.txt")
    #     api_response = get_spotify_track_id("Never Gonna Give You Up", "Rick Astley", token)
    #     generate_access_token_from_spotify("client-id.txt", "client-secret.txt", "access_token.txt")

