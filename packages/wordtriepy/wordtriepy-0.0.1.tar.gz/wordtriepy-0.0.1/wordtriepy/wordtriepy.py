import pickle
import pathlib
import os


class WordTrie:
    def __init__(self, language="en"):
        self._root = {}
        self._end_token = "_end"
        parent_dir = pathlib.Path(__file__).parent.resolve()
        if language == "en":
            self._load(os.path.join(parent_dir, "assets/words_en.pkl"))
        elif language == "de":
            self._load(os.path.join(parent_dir, "assets/words_de.pkl"))
        elif language == "fr":
            self._load(os.path.join(parent_dir, "assets/words_fr.pkl"))
        elif language == "es":
            self._load(os.path.join(parent_dir, "assets/words_es.pkl"))
        elif language == "pt":
            self._load(os.path.join(parent_dir, "assets/words_pt.pkl"))
        else:
            raise Exception(f"Language '{language}' not supported")

    def _save(self):
        with open("./words_pt.pkl", "wb") as file:
            pickle.dump(self._root, file)

    def _load(self, word_file_path):
        with open(word_file_path, "rb") as file:
            self._root = pickle.load(file)

    def add(self, word):
        current_element = self._root
        for char in word:
            if char not in current_element:
                current_element[char] = {}
            current_element = current_element[char]
        current_element[self._end_token] = None

    def exists(self, word):
        word = word.lower()
        current_element = self._root
        for char in word:
            if char not in current_element:
                return False
            else:
                current_element = current_element[char]
        if self._end_token in current_element:
            return True
        else:
            return False

    def __contains__(self, key):
        return self.exists(key)

    def get_next_chars(self, partial_word):
        partial_word = partial_word.lower()
        current_element = self._root
        for index, char in enumerate(partial_word):
            if char not in current_element:
                return []
            else:
                current_element = current_element[char]
                if index == len(partial_word) - 1:
                    return [key for key in current_element.keys()]

    def get_next_words(self, partial_word, topn=10):
        partial_word = partial_word.lower()
        wordlist = []
        next_chars = self.get_next_chars(partial_word)
        current_word = partial_word
        next_words = []

        def traverse(current_word, next_chars):
            if next_chars is None:
                return
            for char in next_chars:
                if char == self._end_token:
                    if len(wordlist) < topn:
                        wordlist.append(current_word)
                    else:
                        return
                else:
                    next_words.append(current_word + char)

            if len(wordlist) > topn:
                return
            if len(next_words) > 0:
                next_word = next_words[0]
                del next_words[0]
                traverse(next_word, self.get_next_chars(next_word))

        traverse(current_word, next_chars)
        return wordlist
