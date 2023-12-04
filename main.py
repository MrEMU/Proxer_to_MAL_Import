"""Main file to run one comlpete parsing from raw files to a mal_import.xml."""
from scripts.anime_list_parse import add_anime_ids, parse_anime_list_from_html
from scripts.mal_xml_parser import parse_mal_xml


if __name__ == "__main__":
    clientID = input("Input your MAL ClientID: ")
    parse_anime_list_from_html()
    if clientID:
        add_anime_ids(clientID)
    else:
        add_anime_ids()
    parse_mal_xml()
    print("You should check all animes mentioned in /data/anime_not_found.txt. They are also tagged with an error element in the mal_import.xml.")

