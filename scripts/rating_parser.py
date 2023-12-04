import os
import re

regex = re.compile(r'/stern_grau')
regex_stern = re.compile(r'/stern')
ratings_raw_file_name = "../data/ratings_raw.txt"
ratings_output_file_name = "../data/ratings.txt"
curr_file = os.path.abspath(__file__)
curr_dir = os.path.dirname(curr_file)
raw_ratings_path = os.path.join(curr_dir, ratings_raw_file_name)
output_ratings_path = os.path.join(curr_dir, ratings_output_file_name)


def parse_raw_ratings():
    """Parse raw ratings from Proxer.me UCP html code. This script counts the grey stars in the html code of the site
    delivered in ratings_raw.txt to determine the rating for every rated anime."""
    try:
        with open(output_ratings_path, 'w') as file:
            # Secure that output is empty
            pass
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f'An error occured: {e}')
    with open(raw_ratings_path, "r") as input_file:
        with open(output_ratings_path, "w") as output_file:
            line = input_file.readline()
            while len(line) > 0:
                if len(regex_stern.findall(line)) > 0:
                    output_file.write(str(10 - len(regex.findall(line))) + "\n")
                line = input_file.readline()


if __name__ == "__main__":
    parse_raw_ratings()
