import json
import os
import time

import requests
import pickle
from bs4 import BeautifulSoup

input_file_html_name = "../data/anime_list_html.txt"
output_file_name = "../data/anime_dic.txt"
alt_output_file_name = "../data/anime_dic_with_id.txt"
not_found_file_name = "../data/anime_not_found.txt"
pickle_file_name = "../data/pickle_file.txt"
curr_file = os.path.abspath(__file__)
curr_dir = os.path.dirname(curr_file)
input_html_path = os.path.join(curr_dir, input_file_html_name)
output_path = os.path.join(curr_dir, output_file_name)
alt_output_path = os.path.join(curr_dir, alt_output_file_name)
not_found_path = os.path.join(curr_dir, not_found_file_name)
pickle_file_path = os.path.join(curr_dir, pickle_file_name)


def add_anime_ids(clientid: str):
    """This function makes request to the MAL API to get the related id's for the animes. The requests are artificially
    slowed, because otherwise the MAL API will block them because of TooManyRequests. This needs an environment
    variable named CLIENT_ID that holds your X-MAL-CLIENT-ID or you can give it your Client_ID as a parametere on call.
    Look into the Readme.md for more information."""
    # define the header for the API calls
    header = {"X-MAL-CLIENT-ID": clientid}
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
                rs = requests.get("https://api.myanimelist.net/v2/anime", params={"q": anime_dic["name"], "fields": "id"}, headers=header)
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


def find_watch_state(line: str) -> str:
    """This function tries to find the watch state in a html line. If it does not find any watch_state it returns None"""
    # Parse the HTML content
    soup = BeautifulSoup(line, 'lxml')

    # Check if the table with id "box-table-a" exists
    watch_state_table = soup.find('table', {'id': 'box-table-a'})

    if watch_state_table:
        # Find the first row in the table
        first_row = watch_state_table.find('tr')

        if first_row:
            # Extract the content of the first header cell dynamically
            header_content = first_row.find('th').get_text(strip=True)
            return header_content
        else:
            return None
    else:
        return None


def find_name(line: str) -> str:
    """This function tries to find the name in a html line. If it does not find any watch_state it returns None"""
    # Parse the HTML content
    soup = BeautifulSoup(line, 'lxml')

    # Extract the name using BeautifulSoup
    name_element = soup.find('a', {'class': 'tip'})
    if name_element:
        name = name_element.get_text(strip=True)
        return name
    else:
        return None


def find_statistics(line: str) -> tuple[str, str, str, str]:
    """This function tries to find various statistics (rating, medium, watched and total episodes) in a html line.
    If it does not find any watch_state it returns None"""
    # Parse the HTML content
    soup = BeautifulSoup(line, 'html.parser')

    # Extract information using BeautifulSoup
    medium_full = soup.find('td', {'valign': 'top'})
    medium = medium_full.contents[-1].strip() if medium_full else ""
    rating_stars = len(soup.find_all('img', {'src': '/images/misc/stern.png'}))
    rating = str(rating_stars) if  rating_stars > 0 else None
    episodes = soup.find('span', {'class': 'state'}).get_text(strip=True)
    episodes_watched, episodes_total = episodes.split("/")

    return medium, rating, episodes_watched.replace(" ", ""), episodes_total.replace(" ", "")


def parse_anime_list_from_html():
    """This function parses an array of anime dictionaries out of the html source code of your Proxer.me watchlist.
    You have to delete some of the top lines of this html code to get the parser to work. Look into the Readme.md for
    more information."""
    try:
        with open(output_path, 'w') as file:
            # Secure that output is empty
            pass
        with open(pickle_file_path, 'w') as file:
            # Secure that output is empty
            pass
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f'An error occured: {e}')
    anime_dic_array = []
    with open(output_path, "w") as output:
        with open(input_html_path, "r") as input_file:
            line = input_file.readline()
            current_watch_state = None
            for i in range(4):
                while line:
                    anime_dic = {}
                    name = None
                    watch_state = find_watch_state(line)
                    if watch_state:
                        current_watch_state = watch_state
                        line = input_file.readline()
                    name = find_name(line)
                    while not name:
                        line = input_file.readline()
                        name = find_name(line)
                        watch_state = find_watch_state(line)
                        if watch_state:
                            current_watch_state = watch_state
                        if not line:
                            break
                    if not line:
                        break
                    anime_dic.update({"watch_state": current_watch_state, "name": name})
                    line = input_file.readline()
                    stats = find_statistics(line)
                    while not line[0]:
                        line = input_file.readline()
                        stats = find_statistics(line)
                        if not line:
                            break
                    if not line:
                        break
                    anime_dic.update({"type": stats[0], "rating": stats[1], "ep_watched": stats[2], "ep_total": stats[3]})
                    print(anime_dic)
                    output.write(str(anime_dic) + "\n")
                    anime_dic_array.append(anime_dic)
                    line = input_file.readline()
            with open(pickle_file_path, "wb") as pickle_file:
                pickle.dump(anime_dic_array, pickle_file)


if __name__ == "__main__":
    clientID = input("Input your MAL ClientID: ")
    parse_anime_list_from_html()
    add_anime_ids(clientID)
    #rs = requests.get("https://api.myanimelist.net/v2/anime", params={"q": "Komi-san wa, Comyushou desu.", "fields": "id"}, headers=Header)
    #print(rs.status_code)
    #print(rs.text)
