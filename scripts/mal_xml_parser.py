import json
import os
import pickle
import time
import xml.etree.ElementTree as ET
from datetime import datetime
from xml.dom import minidom

template_file_name = "../data/template.xml"
output_file_name = "../data/mal_import.xml"
pickle_file_name = "../data/pickle_file.txt"
curr_file = os.path.abspath(__file__)
curr_dir = os.path.dirname(curr_file)
template_path = os.path.join(curr_dir, template_file_name)
output_path = os.path.join(curr_dir, output_file_name)
pickle_file_path = os.path.join(curr_dir, pickle_file_name)


def parse_anime_to_xml(anime):
    """Parse one anime dictionary into a xml element."""
    elements = []
    new_element = ET.Element("anime")
    if "error_message" in anime.keys():
        error = ET.Element("Error")
        error.text = anime["name"] + ": " + anime["error_message"]
        elements.append(error)
    id = ET.Element("series_animedb_id")
    id.text = str(anime["id"]) if "id" in anime.keys() else "NEEDS TO BE UPDATED. SEE ERROR MESSAGE"
    series_type = ET.Element("series_type")
    series_type.text = "TV" if anime["type"] == "Animeserie" else anime["type"]
    series_episodes = ET.Element("series_episodes")
    series_episodes.text = anime["ep_total"]
    my_id = ET.Element("my_id")
    my_id.text = 0
    my_watched_episodes = ET.Element("my_watched_episodes")
    my_watched_episodes.text = anime["ep_watched"]
    my_start_date = ET.Element("my_start_date")
    my_start_date.text = datetime.now().strftime("%Y-%m-%d")
    my_finish_date = ET.Element("my_finish_date")
    my_finish_date.text = datetime.now().strftime("%Y-%m-%d")
    my_rated = ET.Element("my_rated")
    my_score = ET.Element("my_score")
    if "rating" in anime.keys():
        my_score.text = anime["rating"]
    my_dvd = ET.Element("my_dvd")
    my_storage = ET.Element("my_storage")
    my_status = ET.Element("my_status")
    my_status.text = anime["watch_state"]
    my_comments = ET.Element("my_comments")
    my_times_watched = ET.Element("my_times_watched")
    my_times_watched.text = str(1) if anime["watch_state"] == "Finished" else str(0)
    my_rewatch_value = ET.Element("my_rewatch_value")
    my_tags = ET.Element("my_tags")
    my_rewatching = ET.Element("my_rewatching")
    my_rewatching_ep = ET.Element("my_rewatching_ep")
    update_on_import = ET.Element("update_on_import")
    update_on_import.text = str(1)
    elements.append(id)
    elements.append(series_type)
    elements.append(series_episodes)
    elements.append(my_id)
    elements.append(my_watched_episodes)
    elements.append(my_start_date)
    elements.append(my_finish_date)
    elements.append(my_rated)
    elements.append(my_score)
    elements.append(my_dvd)
    elements.append(my_storage)
    elements.append(my_status)
    elements.append(my_comments)
    elements.append(my_rewatch_value)
    elements.append(my_tags)
    elements.append(my_rewatching)
    elements.append(my_rewatching_ep)
    elements.append(update_on_import)
    for elem in elements:
        new_element.append(elem)
    return new_element


def parse_mal_xml():
    """Parse anime dictionary to XML elements and write it together with the template into mal_import.xml"""
    with open(pickle_file_path, 'rb') as pickle_file:
        anime_dic_array = pickle.load(pickle_file)
    try:
        with open(output_path, 'w') as file:
            # Secure that output is empty
            pass
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f'An error occured: {e}')
    with open(output_path, 'w') as output_file:
        tree = ET.parse(template_path)
        root = tree.getroot()
        for anime in anime_dic_array:
            print(anime)
            new_element = parse_anime_to_xml(anime)
            root.append(new_element)
        xml_str = minidom.parseString(ET.tostring(root, encoding="utf-8")).toprettyxml(indent="  ")
        output_file.write(xml_str)


if __name__ == "__main__":
    parse_mal_xml()
