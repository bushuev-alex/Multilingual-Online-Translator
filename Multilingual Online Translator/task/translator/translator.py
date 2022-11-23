import requests
from bs4 import BeautifulSoup
import re
import argparse


class Translator:

    def __init__(self, home_lang, translate_to, word):
        self.languages = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew',
                          'Japanese', 'Dutch', 'Polish', 'Portuguese', 'Romanian', 'Russian', 'Turkish']
        self.home_lang = home_lang
        self.translate_to = translate_to
        self.word = word
        self.url = "https://context.reverso.net/translation/"
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.r = None
        self.soup = None

    def validate_langs(self) -> bool:
        if self.home_lang.capitalize() not in self.languages:
            print(f"Sorry, the program doesn't support {self.home_lang}")
            return False
        if self.translate_to == 'all':
            self.translate_to = self.languages.copy()
            self.translate_to.remove(self.home_lang.capitalize())
            return True
        elif self.translate_to not in self.languages:
            print(f"Sorry, the program doesn't support {self.translate_to}")
            return False

    def send_request(self, lang_translate_to) -> bool:
        url = self.url + f"{self.home_lang}-{lang_translate_to}/{self.word}"
        self.r = requests.get(url, headers=self.headers)
        if self.r.status_code == 200:
            self.soup = BeautifulSoup(self.r.content, 'html.parser')
            return True
        elif self.r.status_code == 404:
            print(f"Sorry, unable to find {self.word}")
            return False
        else:
            print("Something wrong with your internet connection")
            return False

    def get_words(self) -> list:
        translations = [self.soup.find(teg, re.compile("translation.*(ltr|rtl).*dict.*")) for teg in ['a', 'div']]
        word_list = [t.text.strip() for t in translations][:1]
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
            if self.send_request(language.lower()):
                words = self.get_words()
                sentences = self.get_sentences()
                self.write_words_sents(language, words, sentences)
            else:
                break

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
    parser.add_argument("home_lang")
    parser.add_argument("translate_to")
    parser.add_argument("word")
    args = parser.parse_args()
    home_lang, translate_to, word = args.home_lang, args.translate_to, args.word
    my_translator = Translator(home_lang, translate_to, word)
    if my_translator.validate_langs():
        my_translator.translate_sentences()
        my_translator.print_result()


if __name__ == '__main__':
    main()
