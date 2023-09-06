# General Information
This is CLI translator based on https://context.reverso.net/   
There is a list of available languages to translate:
* Arabic
* German
* English
* Spanish
* French
* Hebrew
* Japanese
* Dutch
* Ukrainian
* Portuguese
* Italian
* Russian
* Turkish

File with result will contain two sections for each language:
* Languale_name Translations - with one most popular translation
* Languale_name Examples - contains two sentences. (1st - non_translated, 2nd - translated). 



# Howto
Launch translator with input in CLI:
* python translator.py --home_lang=russian --translate_to=german --word=машина

--home_lang - optional argument, default value: russian
--translate_to - optional argument, default value: all
--word - optional argument, default value: Папа

You can use all languages to translate to if insert 'All' or 'all' as value to argument --translate_to=
Actually, 'all' is a default value for --translate_to=...

Translation results will be saved in **Word_to_translate**.txt file.\
And printed in CLI.
