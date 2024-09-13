from turtledemo.forest import start

import requests
import base64
import json
import time

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
        'access_token': access_token,
        'limit': 1
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

    return requests.get(audio_feature_endpoint, headers={"Authorization": f"Bearer {access_token}"})


if __name__ == "__main__":
    '''
    Spotify table columns:
    spotify_id, last_fm_id, acousticness, danceability, energy, instrumentalness, loudness, speechiness, valence, 
    tempo, mode, manual_check
    '''
    spotify_sleep = 0.1

    lastfm_df = pd.read_csv("./data/lastfm.csv")

    df_dict = {}
    df = pd.DataFrame(columns=["spotify_id", "lastfm_id", "acousticness", "danceability", "energy", "instrumentalness",
                               "loudness", "speechiness", "valence", "tempo", "mode", "manual_check"])

    total = len(lastfm_df)
    start_at = 0

    generate_access_token_from_spotify("client-id.txt", "client-secret.txt", "access_token.txt")

    for index, row in lastfm_df.iterrows():
        if index < start_at:
            continue
        if index % 10 == 0:
            print(f"File {index + 1}")

        new_data = {
            "spotify_id": -1.0, "lastfm_id": -1.0, "acousticness": -1.0, "danceability": -1.0, "energy": -1.0,
            "instrumentalness": -1.0, "loudness": -1, "speechiness": -1.0, "valence": -1.0, "tempo": -1.0,
            "mode": -1.0, "manual_check": False
        }

        artist = lastfm_df.loc[index]["artist"]
        track = lastfm_df.loc[index]["title"]

        token = read_access_token_from_file("access_token.txt")
        time.sleep(spotify_sleep)
        api_response = get_spotify_track_id(track, artist, token)

        if api_response.status_code == 401:
            time.sleep(spotify_sleep)
            generate_access_token_from_spotify("client-id.txt", "client-secret.txt", "access_token.txt")
            token = read_access_token_from_file("access_token.txt")
            time.sleep(spotify_sleep)
            api_response = get_spotify_track_id(track, artist, token)

        if api_response.status_code == 400:
            print(api_response.json())
            print(api_response.url)
            continue

        elif api_response.status_code == 429:
            print(api_response.json())
            print(api_response.headers)
            break


        elif api_response.status_code != 200:
            print(api_response.json())
            print(api_response.url)
            break

        try:
            response_items = api_response.json()["tracks"]["items"][0]
            spot_artist = response_items["artists"][0]["name"]
            spot_track = response_items["name"]

            new_data["spotify_id"] = response_items["id"]

            if spot_artist.lower() != artist.lower() and spot_track.lower() != track.lower():
                new_data["manual_check"] = True

        except IndexError:
            continue

        time.sleep(spotify_sleep)
        api_response = get_spotify_track_audio_features(token, new_data["spotify_id"])

        # first check
        if api_response.status_code == 401:
            time.sleep(spotify_sleep)
            generate_access_token_from_spotify("client-id.txt", "client-secret.txt", "access_token.txt")
            token = read_access_token_from_file("access_token.txt")
            time.sleep(spotify_sleep)
            api_response = get_spotify_track_audio_features(token, new_data["spotify_id"])

        elif api_response.status_code == 429:
            print(api_response.json())
            print(api_response.headers)
            print(api_response.url)
            break

        # Second check
        if api_response.status_code != 200:
            print(f"Spotify ID: {new_data["spotify_id"]} // {spot_track} by {spot_artist}: {api_response.json()}")
            df.loc[len(df)] = new_data.values()
            continue

        features = api_response.json()

        for key in features.keys():
            if key in new_data.keys():
                new_data[key] = features[key]
        new_data["lastfm_id"] = lastfm_df.loc[index]["lastfm_id"]

        df.loc[len(df)] = new_data.values()

        if index % 1000 == 0:
            print(f"progress saved: {round(100 * index / total, 2)}%")
            df_dict[index] = df
            df = df.drop(labels=df.index, axis=0)

        if index > 5000:
            break

    with open("data/last-index-written.txt", "w") as f:
        f.write(str(index))

    index += 1
    df_dict[index] = df
    test = df_dict.values()
    write_df = pd.concat(df_dict.values())
    write_df.to_csv("spotify.csv")
