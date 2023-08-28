import os
import time
import json
from tqdm import tqdm
from datetime import datetime


class SpellaThon:
    def __init__(self, legal_char_list, center_character,
                 dict_path="reference/words_dictionary.json"):
        self.word_dict = json.load(open(dict_path))
        self.legal_char_list = legal_char_list
        self.center_character = center_character

    def all_reference_match(self, word):
        visited = {k: False for k in self.legal_char_list}
        for char in word:
            if not char in self.legal_char_list or visited[char]:
                return False
            visited[char] = True
        return True

    def follows_rules(self, word):
        word = word.lower()
        if not self.center_character in word:
            return False
        if not (4 <= len(word) <= 7):
            return False
        if not self.all_reference_match(word):
            return False
        return True

    def get_possible_matches(self):
        matches = []
        for word in tqdm(self.word_dict):
            if self.follows_rules(word):
                matches.append(word)
        return matches


if __name__ == "__main__":

    center_character = "c"
    legal_characters = "afolbi" + center_character

    output_dir = "outputs/results.json"
    outputs_json = {}
    if os.path.exists(output_dir):
        outputs_json = json.load(open(output_dir))

    start = time.time()
    legal_char_list = [f for f in legal_characters]
    obj = SpellaThon(legal_char_list, center_character)
    matches = obj.get_possible_matches()
    date = str(datetime.now())[:10]
    outputs_json[date] = {"legal_characters": legal_char_list[:-1],
                          "center_character": center_character,
                          "possible_matches": matches}
    with open(output_dir, 'w') as f:
        json.dump(outputs_json, f, indent=4)
    print(matches)
    print(f"Time taken : {time.time()-start:.2f}s")
