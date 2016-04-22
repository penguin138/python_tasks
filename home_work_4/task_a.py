#! /usr/bin/env python3
import sys


def language(word, languages):
    letters = {}
    for letter in word:
        for lang in sorted(languages.keys()):
            if letter in languages[lang]:
                letters[letter] = lang
                break
    langs_used = {}
    for letter, lang in letters.items():
        if lang in langs_used:
            langs_used[lang] += 1
        else:
            langs_used[lang] = 1
    sorted_langs = sorted(langs_used.items())
    if sorted_langs:
        return max(sorted(langs_used.items()), key=lambda x: x[1])[0]
    return ""


def main():
    languages = {}
    queries = []
    blank_line = False
    for line in sys.stdin:
        if line == "\n":
            # print("blank")
            blank_line = True
            continue
        if not blank_line:  # haven't received blank line yet
            lang_name, lang_letters = line.split()
            languages[lang_name] = lang_letters
        else:  # received blank line - now receiving queries
            queries.append(line)
    for query in queries:
        langs = []
        for word in query.split(' '):
            langs.append(language(word.lower(), languages))
        for lang in sorted(set(langs)):
            print(lang, end=" ")
        print()
main()
