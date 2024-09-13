import os
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
        'limit': 50
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


def get_spotify_tracks_audio_features(access_token, spotify_track_ids):
    """
    :param access_token: Spotify access token
    :param spotify_track_id: ID of spotify track to read
    :return:
    """

    parameters = {
        "ids": spotify_track_ids
    }

    audio_feature_endpoint = f"https://api.spotify.com/v1/audio-features"
    print("Audio Feature batch requested.")
    return requests.get(audio_feature_endpoint, params=parameters, headers={"Authorization": f"Bearer {access_token}"})


if __name__ == "__main__":
    '''
    Spotify table columns:
    spotify_id, last_fm_id, acousticness, danceability, energy, instrumentalness, loudness, speechiness, valence, 
    tempo, mode, manual_check
    '''

    def id_list_to_string(list_of_ids):
        total_string = ""

        for id_ in list_of_ids:
            total_string += id_
            if id_ != list_of_ids[-1]:
                total_string += ","

        return total_string

    def initialize_new_data():
        return {
            "spotify_id": -1.0, "lastfm_id": -1.0, "acousticness": -1.0, "danceability": -1.0, "energy": -1.0,
            "instrumentalness": -1.0, "loudness": -1, "speechiness": -1.0, "valence": -1.0, "tempo": -1.0,
            "mode": -1.0, "manual_check": False
        }


    spotify_sleep = 0.07  # DO NOT LOWER

    lastfm_df = pd.read_csv("./data/lastfm.csv")

    # df_dict = {"start": pd.read_csv("./data/spotify.csv").drop(columns=["Unnamed: 0"])}
    df_dict = {}
    df = pd.DataFrame(columns=["spotify_id", "lastfm_id", "acousticness", "danceability", "energy", "instrumentalness",
                               "loudness", "speechiness", "valence", "tempo", "mode", "manual_check"])

    total = len(lastfm_df)
    start_at = 0

    client_iteration = 0
    # generate_access_token_from_spotify(id_list[client_iteration], secret_list[client_iteration],
    #                                    "./client-info/access_token.txt")

    client_path = "./client-info"
    file_list = os.listdir("client-info")
    id_list = []
    secret_list = []
    for file in file_list:
        if "id" in file:
            id_list.append(os.path.join(client_path, file))
        elif "secret" in file:
            secret_list.append(os.path.join(client_path, file))

    id_list.sort()
    secret_list.sort()

    progress_report_interval = 1000
    progress_save_interval = 10000

    progress_report = progress_report_interval
    progress_save = progress_save_interval

    spotify_ids_for_call = []
    lastfm_ids_for_linking = []
    manual_check_list = []
    for index, row in lastfm_df.iterrows():
        if index <= start_at:
            continue
        if index % 10 == 0:
            print(f"File {index + 1}")

        new_data = initialize_new_data()

        artist = lastfm_df.loc[index]["artist"]
        track = lastfm_df.loc[index]["title"]
        lastfm_id = lastfm_df.loc[index]["lastfm_id"]

        token = read_access_token_from_file("./client-info/access_token.txt")
        time.sleep(spotify_sleep)
        api_response = get_spotify_track_id(track, artist, token)

        if api_response.status_code == 401:
            time.sleep(spotify_sleep)
            generate_access_token_from_spotify(id_list[client_iteration], secret_list[client_iteration],
                                               "./client-info/access_token.txt")
            token = read_access_token_from_file("./client-info/access_token.txt")
            time.sleep(spotify_sleep)
            api_response = get_spotify_track_id(track, artist, token)

        if api_response.status_code == 400:
            print(api_response.json())
            print(api_response.url)
            continue

        elif api_response.status_code == 429:
            print(api_response.json())
            print(api_response.headers)
            time.sleep(spotify_sleep)
            client_iteration += 1
            if client_iteration > 2:
                break

            generate_access_token_from_spotify(id_list[client_iteration], secret_list[client_iteration],
                                               "./client-info/access_token.txt")
            token = read_access_token_from_file("./client-info/access_token.txt")
            time.sleep(spotify_sleep)
            api_response = get_spotify_track_id(track, artist, token)
            if api_response.status_code == 429:
                print(api_response.json())
                print(api_response.headers)
                break

        if api_response.status_code != 200:
            print(api_response.json())
            print(api_response.url)
            break

        try:
            response_items = api_response.json()["tracks"]["items"]

            spot_artist = response_items[0]["artists"][0]["name"]
            spot_track = response_items[0]["name"]
            new_data["spotify_id"] = response_items[0]["id"]

            response_item_selection = response_items[0]

            for item in response_items:
                if item["artists"][0]["name"].lower() != artist.lower() or item["name"].lower() != track.lower():
                    continue
                else:
                    response_item_selection = item
                    spot_artist = item["artists"][0]["name"]
                    spot_track = item["name"]
                    break

            spotify_ids_for_call.append(response_item_selection["id"])
            lastfm_ids_for_linking.append(lastfm_id)

            if spot_artist.lower() != artist.lower() or spot_track.lower() != track.lower():
                manual_check_list.append(True)
            else:
                manual_check_list.append(False)

        except IndexError:
            continue

        assert len(spotify_ids_for_call) == len(lastfm_ids_for_linking), "Somehow these two lists are different sizes."
        assert len(spotify_ids_for_call) == len(manual_check_list), "Somehow these two lists are different sizes."

        if len(spotify_ids_for_call) != 100:
            continue

        spotify_id_string = id_list_to_string(spotify_ids_for_call)

        time.sleep(spotify_sleep)
        api_response = get_spotify_tracks_audio_features(token, spotify_id_string)

        # first check
        if api_response.status_code == 401:
            time.sleep(spotify_sleep)
            generate_access_token_from_spotify(id_list[client_iteration], secret_list[client_iteration],
                                               "./client-info/access_token.txt")
            token = read_access_token_from_file("./client-info/access_token.txt")
            time.sleep(spotify_sleep)
            api_response = get_spotify_tracks_audio_features(token, spotify_id_string)

        elif api_response.status_code == 429:
            print(api_response.json())
            print(api_response.headers)
            time.sleep(spotify_sleep)
            client_iteration += 1
            if client_iteration > 2:
                break

            generate_access_token_from_spotify(id_list[client_iteration], secret_list[client_iteration],
                                               "./client-info/access_token.txt")
            token = read_access_token_from_file("./client-info/access_token.txt")
            time.sleep(spotify_sleep)
            api_response = get_spotify_tracks_audio_features(token, spotify_id_string)
            if api_response.status_code == 429:
                print(api_response.json())
                print(api_response.headers)
                break

        # Second check
        if api_response.status_code != 200:
            print(f"Spotify ID: {new_data["spotify_id"]} // {spot_track} by {spot_artist}: {api_response.json()}")
            print(api_response.url)
            df.loc[len(df)] = new_data.values()
            continue

        features = api_response.json()

        lastfm_id_idx = 0
        for feature_dict in features["audio_features"]:
            new_data["lastfm_id"] = lastfm_ids_for_linking[lastfm_id_idx]
            new_data["spotify_id"] = spotify_ids_for_call[lastfm_id_idx]
            new_data["manual_check"] = manual_check_list[lastfm_id_idx]
            lastfm_id_idx += 1
            if feature_dict is None:
                new_data = initialize_new_data()
                continue
            for key in feature_dict.keys():
                if key in new_data.keys():
                    new_data[key] = feature_dict[key]

            df.loc[len(df)] = new_data.values()
            new_data = initialize_new_data()

        spotify_ids_for_call = []
        lastfm_ids_for_linking = []

        if index > progress_report:
            progress_report += progress_report_interval
            print(f"Progress: {round(100 * index / total, 2)}%")
            df_dict[index] = df
            df = df.drop(labels=df.index, axis=0)

        if index > progress_save:
            progress_save += progress_save_interval
            print(f"Progress saved: {round(100 * index / total, 2)}%")
            df_dict[index] = df
            write_df = pd.concat(df_dict.values())
            write_df.to_csv("./data/spotify.csv")


    with open("data/last-index-written.txt", "w") as f:
        f.write(str(index))

    index += 1
    df_dict[index] = df
    write_df = pd.concat(df_dict.values())
    write_df.to_csv("./data/spotify.csv")
