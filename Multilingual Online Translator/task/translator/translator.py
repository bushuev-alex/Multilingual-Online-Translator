import requests
from bs4 import BeautifulSoup
import re
import argparse


class Translator:

    def __init__(self, home_lang: str, translate_to: str, word: str):
        self.languages = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew',
                          'Japanese', 'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish']
        self.home_lang = home_lang
        self.translate_to = translate_to
        self.word = word
        self.url = "https://context.reverso.net/translation/"
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.request_result = None
        self.soup = None

    def validate_langs(self) -> bool:
        if self.home_lang.capitalize() not in self.languages:
            print(f"Sorry, the program doesn't support {self.home_lang}")
            return False
        if self.translate_to == 'all':
            self.translate_to = self.languages.copy()
            self.translate_to.remove(self.home_lang.capitalize())
            print(2)
            return True
        if self.translate_to not in self.languages:
            print(f"Sorry, the program doesn't support {self.translate_to}")
            print(3)
            return False
        else:
            return True

    def send_request(self, lang_translate_to: str) -> bool:
        url = self.url + f"{self.home_lang}-{lang_translate_to}/{self.word}"
        self.request_result = requests.get(url, headers=self.headers)
        if self.request_result.status_code == 200:
            self.soup = BeautifulSoup(self.request_result.content, 'html.parser')
            return True
        elif self.request_result.status_code == 404:
            print(f"Sorry, unable to find {self.word}")
            return False
        else:
            print("Something wrong with your internet connection")
            return False

    def translate_words(self) -> list:
        translations = [self.soup.find(teg, re.compile("translation.*(ltr|rtl).*dict.*")) for teg in ['a', 'div']]
        word_list = [t.text.strip() for t in translations if t is not None][:1]
        if len(word_list) == 0:
            return [""]
        else:
            return word_list

    def get_sentences(self) -> list:
        untranslated_sentences = self.soup.findAll('div', {'class': 'src ltr'})
        translated_sentences = self.soup.findAll('div', {'class': re.compile("trg.*(ltr|rtl).*")})
        sentences = []
        try:
            sentences.append(untranslated_sentences[0].text.strip())
            sentences.append(translated_sentences[0].text.strip())
        except IndexError:
            sentences.append('')
            sentences.append('')
        return sentences

    def translate_sentences(self):
        for language in self.translate_to:
            request_result = self.send_request(language.lower())
            if request_result:
                words = self.translate_words()
                sentences = self.get_sentences()
                self.write_words_sents(language, words, sentences)
            else:
                continue

    def write_words_sents(self, language: str, words: list, sentences: list):
        with open(f"{self.word}.txt", 'a', encoding='UTF-8') as file:
            file.write(f"{language} Translations:\n")
            file.write(f"{words[0]}\n\n")
            file.write(f"{language} Examples:\n")
            file.write(f"{sentences[0]}\n")
            file.write(f"{sentences[1]}\n\n")

    def print_result(self):
        try:
            with open(f"{self.word}.txt", 'r', encoding='UTF-8') as file:
                for line in file:
                    print(line.strip())
        except FileNotFoundError:
            pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("home_lang", default="russian")
    parser.add_argument("translate_to", default="all")
    parser.add_argument("word", default="Слово")
    args = parser.parse_args()
    home_lang, translate_to, word = args.home_lang, args.translate_to, args.word
    my_translator = Translator(home_lang, translate_to, word)
    if my_translator.validate_langs():
        my_translator.translate_sentences()
        my_translator.print_result()


if __name__ == '__main__':
    main()
