"""Main file to run one comlpete parsing from raw files to an mal_import.xml."""
from scripts.anime_list_parse import parse_anime_list, add_anime_ids
from scripts.mal_xml_parser import parse_mal_xml
from scripts.rating_parser import parse_raw_ratings


if __name__ == "__main__":
    parse_raw_ratings()
    parse_anime_list()
    add_anime_ids()
    parse_mal_xml()
    print("You should check all animes mentioned in /data/anime_not_found.txt. They are also tagged with an error element in the mal_import.xml.")

