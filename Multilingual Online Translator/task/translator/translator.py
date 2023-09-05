from html_parser import Translator
import argparse


def parse_params() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("home_lang", default="russian")
    parser.add_argument("translate_to", default="all")
    parser.add_argument("word", default="Папа")
    args = parser.parse_args()
    return args


def main():
    args = parse_params()
    my_translator = Translator(args.home_lang, args.translate_to, args.word)

    if my_translator.validate_langs():
        for lang in my_translator.translate_to:
            soup = my_translator.send_request(lang, my_translator.word)
            words = my_translator.fetch_words(soup)
            sentences = my_translator.fetch_sentences(soup)
            # my_translator.write_words_sents(lang, words, sentences)
            # my_translator.print_result()


if __name__ == '__main__':
    main()
