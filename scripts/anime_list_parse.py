import json
import os
import time

import requests
import pickle

input_file_name = "../data/anime_list.txt"
output_file_name = "../data/anime_dic.txt"
alt_output_file_name = "../data/anime_dic_with_id.txt"
rating_file_name = "../data/ratings.txt"
not_found_file_name = "../data/anime_not_found.txt"
pickle_file_name = "../data/pickle_file.txt"
unrated_title = ["Dragon Ball", "Another"]
curr_file = os.path.abspath(__file__)
curr_dir = os.path.dirname(curr_file)
input_path = os.path.join(curr_dir, input_file_name)
output_path = os.path.join(curr_dir, output_file_name)
alt_output_path = os.path.join(curr_dir, alt_output_file_name)
ratings_path = os.path.join(curr_dir, rating_file_name)
not_found_path = os.path.join(curr_dir, not_found_file_name)
pickle_file_path = os.path.join(curr_dir, pickle_file_name)

client_id = os.environ.get("CLIENT_ID")
assert client_id is not None
Header = {"X-MAL-CLIENT-ID": client_id}


def parse_anime_list():
    """Parses anime list from anime_list.txt into an array of anime dictionaries. For the raw code the Proxer.me UCP's
    anime list was copied from the site and reformatted by removing empty lines, option lines and ensuring the following
    format:
    [Abgeschlossen] 	Dragon Ball Z 	Animeserie
    TV		291 /
    The lines for Watching, Plan to watch and Dropped were kept in to determine the watch status."""
    try:
        with open(output_path, 'w') as file:
            # Secure that output is empty
            pass
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f'An error occured: {e}')
    anime_dic_array = []
    with open(input_path, "r") as input_file:
        with open(ratings_path, "r") as rating_file:
            line = input_file.readline()
            rating = rating_file.readline()
            watch_state = "Completed"
            while len(line) > 0:
                if line == "Wird noch geschaut\n":
                    watch_state = "Plan to Watch"
                    line = input_file.readline()
                elif line == "Am Schauen\n":
                    watch_state = "Watching"
                    line = input_file.readline()
                elif line == "Abgebrochen\n":
                    watch_state = "Dropped"
                    line = input_file.readline()
                anime_dic = {}
                line_array = line.split("\t")
                anime_dic.update({"watch_state": watch_state})
                anime_dic.update({"name": line_array[1].rstrip()})
                anime_dic.update({"type": line_array[2].replace("\n", "")})
                line = input_file.readline()
                line_array = line.split("\t")
                episodes = line_array[2].split(" ")
                anime_dic.update({"ep_watched": episodes[0], "ep_total": episodes[2].replace("\n", "")})
                if anime_dic["watch_state"] != "Plan to Watch" and anime_dic["watch_state"] != "Watching" and not anime_dic["name"] in unrated_title:
                    anime_dic.update({"rating": rating.replace("\n", "")})
                    rating = rating_file.readline()
                with open(output_path, 'a') as output_file:
                    output_file.write(str(anime_dic) + "\n")
                line = input_file.readline()
                anime_dic_array.append(anime_dic)
    with open(pickle_file_path, "wb") as pickle_file:
        pickle.dump(anime_dic_array, pickle_file)


def add_anime_ids():
    """This function makes request to the MAL API to get the related id's for the animes. The requests are artificially
    slowed, because otherwise the MAL API will block them because of TooManyRequests. This needs an environment
    variable named CLIENT_ID that holds your X-MAL-CLIENT-ID. Look into the Readme.md for more information."""
    with open(pickle_file_path, 'rb') as pickle_file:
        anime_dic_array = pickle.load(pickle_file)
    try:
        with open(pickle_file_path, 'w') as file:
            # Secure that output is empty
            pass
        with open(alt_output_path, 'w') as file:
            # Secure that output is empty
            pass
        with open(not_found_path, "w") as not_found:
            # Secure that output is empty
            pass
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f'An error occured: {e}')
    result_array = []
    with open(alt_output_path, 'a') as output_file:
        with open(not_found_path, "a") as not_found:
            for anime_dic in anime_dic_array:
                rs = requests.get("https://api.myanimelist.net/v2/anime", params={"q": anime_dic["name"], "fields": "id"}, headers=Header)
                print(anime_dic["name"])
                print("Status Code: " + str(rs.status_code))
                print("Response: " + rs.text)
                print("-" * 500)
                if rs.status_code == 200:
                    rs_dict = json.loads(rs.text)
                    if anime_dic["name"] == rs_dict["data"][0]["node"]["title"]:
                        anime_dic.update({"id": rs_dict["data"][0]["node"]["id"]})
                        output_file.write(str(anime_dic) + "\n")
                        result_array.append(anime_dic)
                    else:
                        anime_dic.update({"error_message": "needs to be checked"})
                        anime_dic.update({"id": rs_dict["data"][0]["node"]["id"]})
                        output_file.write(str(anime_dic) + "\n")
                        not_found.write(str(anime_dic) + "\n")
                        result_array.append(anime_dic)
                else:
                    rs_dict = json.loads(rs.text)
                    anime_dic.update({"error_message": rs_dict["message"]})
                    output_file.write(str(anime_dic) + "\n")
                    not_found.write(str(anime_dic) + "\n")
                    result_array.append(anime_dic)
                time.sleep(5)
    with open(pickle_file_path, "wb") as pickle_file:
        print("write Pickle")
        pickle.dump(result_array, pickle_file)


if __name__ == "__main__":
    #anime_dic_array = parse_anime_list()
    #add_anime_ids(anime_dic_array)
    rs = requests.get("https://api.myanimelist.net/v2/anime", params={"q": "Komi-san wa, Comyushou desu.", "fields": "id"}, headers=Header)
    print(rs.status_code)
    print(rs.text)
