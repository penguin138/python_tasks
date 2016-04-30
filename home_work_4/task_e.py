#! /usr/bin/env python3
import bs4
from urllib.request import urlopen


def get_post_urls(url):
    with urlopen(url) as url_conn:
        data = url_conn.read()
        main_page = data.decode('utf-8')
    soup = bs4.BeautifulSoup(main_page, 'html.parser')
    posts = soup.find("div", attrs={'class': 'posts'})
    posts_shortcuts = posts.find_all("div", class_='post shortcuts_item')
    urls = []
    for post_shortcut in posts_shortcuts:
        title = post_shortcut.find('h1', class_="title")
        link = title.find('a')['href']
        urls.append(link)
    return urls


def get_text_from_url(url):
    with urlopen(url) as url_conn:
        data = url_conn.read()
        post = data.decode('utf-8')
    soup = bs4.BeautifulSoup(post, 'html.parser')
    text = soup.find('div', class_="content")
    return text.get_text()


def main():
    filename = input("Enter filename: ")
    main_url = "https://geektimes.ru/users/alizar/topics/"
    all_urls = []
    for page in range(1, 85):
        urls = get_post_urls(main_url + 'page{}/'.format(page))
        # print(page)
        all_urls.extend(urls)
    with open(filename, 'w') as posts:
        for url in all_urls:
            # print(url)
            posts.write(get_text_from_url(url))

# main()
