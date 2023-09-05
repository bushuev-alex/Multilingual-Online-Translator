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

        if self.translate_to in ['all', 'All']:
            self.translate_to = self.languages.copy()
            self.translate_to.remove('All')
            self.translate_to.remove(self.home_lang.capitalize())
            return True
        return True

    def send_request(self, translate_to: str, word: str) -> BeautifulSoup:
        url = self.url + f"{self.home_lang}-{translate_to.lower()}/{word}"
        print(translate_to)
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
        sentences = [(untranslated.text.strip(),
                     translated.text.strip()) if untranslated and translated else ('', '')
                     for untranslated, translated in zip(untranslated_sents, translated_sents)]
        # sentences = ((untranslated.text.strip(),
        #              translated.text.strip())
        #              for untranslated, translated in zip(untranslated_sents, translated_sents)
        #              if untranslated and translated)
        return sentences

    def write_words_sents(self, language: str, words: list, sentences: list):
        with open(f"{self.word}.txt", 'a', encoding='UTF-8') as file:
            file.write(f"{language} Translations:\n")
            file.write(f"{words[0]}\n\n")
            file.write(f"{language} Examples:\n")
            file.write(f"{sentences[0][0]}\n")
            file.write(f"{sentences[0][1]}\n\n")

    def print_result(self):
        try:
            with open(f"{self.word}.txt", 'r', encoding='UTF-8') as file:
                for line in file:
                    print(line.strip())
        except FileNotFoundError:
            print("File doesn't exist")
        finally:
            print("OK")


if __name__ == '__main__':
    pass
