from typing import Generator, Any

import requests
from bs4 import BeautifulSoup
import re
from pprint import pprint


class Translator:

    def __init__(self, home_lang: str, translate_to: str, word: str):
        self.languages = ['All', 'Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew',
                          'Japanese', 'Dutch', 'Ukrainian', 'Portuguese', 'Italian', 'Russian', 'Turkish']
        self.home_lang = home_lang
        self.translate_to = translate_to
        self.word = word
        self.url = "https://context.reverso.net/translation/"
        self.headers = {'User-Agent': 'Mozilla/5.0'}

    def validate_langs(self) -> bool:
        if self.home_lang.capitalize() not in self.languages:
            print(f"Sorry, the program doesn't support {self.home_lang}")
            return False
        elif self.translate_to.capitalize() not in self.languages:
            print(f"Sorry, the program doesn't support {self.translate_to}")
            return False
        return True

    def handle_all_query(self) -> bool:
        if self.translate_to in ['all', 'All']:
            translate_to = self.languages.copy()
            translate_to.remove('All')
            translate_to.remove(self.home_lang.capitalize())
            self.translate_to = translate_to
        else:  # if len(self.translate_to == 1)
            self.translate_to = [self.translate_to]
        return True

    def send_request(self, translate_to: str, word: str) -> BeautifulSoup:
        url = self.url + f"{self.home_lang}-{translate_to.lower()}/{word}"
        request_result = requests.get(url, headers=self.headers)
        if request_result.status_code == 200:
            return BeautifulSoup(request_result.content, 'html.parser')
        elif request_result.status_code == 404:
            print(f"Sorry, unable to find {word}")
        else:
            print("Something wrong with your internet connection")

    def fetch_words(self, soup: BeautifulSoup) -> list:
        translations_in_a = soup.findAll('a', re.compile("translation (ltr|rtl) dict.*"))
        translations_in_div = soup.findAll('div', re.compile("translation (ltr|rtl) dict.*"))
        translations = translations_in_a + translations_in_div
        word_list = [word.text.strip() if word else '' for word in translations]
        return word_list

    def fetch_sentences(self, soup: BeautifulSoup) -> list[tuple[str, str]]:
        untranslated_sents = soup.findAll('div', {'class': 'src ltr'})
        translated_sents = soup.findAll('div', {'class': re.compile("trg.*(ltr|rtl).*")})
        sentences = [(untranslated.text.strip(), translated.text.strip())
                     if untranslated and translated else ('', '')
                     for untranslated, translated in zip(untranslated_sents, translated_sents)]
        return sentences

    def write_words_sents(self, language: str, words: list, sentences: list) -> bool:
        with open(f"{self.word}.txt", 'a', encoding='UTF-8') as file:
            print(f"{language} Translations:", file=file)
            print(f"{language} Translations:")
            print(f"{words[0]}\n", file=file)
            print(f"{words[0]}\n")
            print(f"{language} Examples:", file=file)
            print(f"{language} Examples:")
            print(f"{sentences[0][0]}", file=file)
            print(f"{sentences[0][0]}")
            print(f"{sentences[0][1]}\n", file=file)
            print(f"{sentences[0][1]}\n")
        return True


if __name__ == '__main__':
    pass
