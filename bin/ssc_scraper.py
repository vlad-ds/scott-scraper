import json
import os
from time import sleep
from typing import List

import tiktoken
import requests
from bs4 import BeautifulSoup


user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

headers = {
    'User-Agent': user_agent
}


def count_tokens(text: str,) -> int:
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    return len(tokens)


def get_ssc_links():

    archives_url = "https://slatestarcodex.com/archives/"
    response = requests.get(archives_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    links = []
    for div in soup.find_all('div', class_='sya_postcontent'):
        postlink = div.find('a', class_='sya_postlink')
        link = postlink.get('href')
        links.append(link)

    # dump links to json
    with open('data/ssc_links.json', 'w') as f:
        json.dump(links, f, indent=4)


def get_ssc_post(link):
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def parse_ssc_post(soup):

    title = soup.find('h1', class_='pjgm-posttitle').text.strip()

    postmeta = soup.find('div', class_='pjgm-postmeta')
    date = postmeta.find('span', class_='entry-date').text.strip()

    content = ''
    postcontent = soup.find('div', class_='pjgm-postcontent')
    for p in postcontent.find_all('p'):
        content += p.text.strip()

    links = []
    for a in postcontent.find_all('a'):
        link = a.get('href')
        if link:
            links.append(link)

    post_data = {
        'title': title,
        'date': date,
        'content': content,
        'content_tokens': count_tokens(content),
        'links': links
    }

    return post_data


def parse_comments(soup):
    comments = []

    def traverse_comment_list(comment_list, depth):
        for comment_element in comment_list:
            comment_data = {}
            comment_div = comment_element.find("div", class_="commentholder")
            comment_data["author"] = comment_div.find("cite", class_="fn").get_text()
            comment_data["text"] = comment_div.find("div", class_="comment-body").get_text(strip=True)
            comment_data["depth"] = depth

            comments.append(comment_data)

            children_list = comment_element.find("ul", class_="children")
            if children_list:
                traverse_comment_list(children_list.find_all("li", recursive=False), depth + 1)

    ol = soup.find("ol", class_="commentlist")

    if ol:
        traverse_comment_list([li for li in ol.find_all("li", recursive=False)
                               if "pingback" not in li.get("class", [])], 1)

    return comments


def render_comments(comments: List[dict]) -> str:
    rendered = []

    def render_comment(comment):
        indent = '-' * (comment['depth'] - 1)
        author = f"{indent}{comment['author']}: "
        text = comment['text'].replace('\n', f'\n{indent}')
        return f"{author}{text}"

    for comment in comments:
        rendered.append(render_comment(comment))

    return "\n".join(rendered)


def link_to_id(link):
    post_date = "-".join(link.split('/')[3:6])
    post_name = link.split('/')[-2]
    return f"{post_date}_{post_name}"


def extract_all_posts():
    # load links from json
    with open('data/ssc_links.json', 'r') as f:
        links = json.load(f)

    for link in links:
        sleep(1)
        print(link)
        post_id = link_to_id(link)
        folder = f"data/posts/{post_id}"
        os.makedirs(folder, exist_ok=True)
        soup = get_ssc_post(link)
        post_data = parse_ssc_post(soup)
        post_data["url"] = link
        comments = parse_comments(soup)

        with open(f"{folder}/post.json", 'w') as f:
            json.dump(post_data, f, indent=4)

        if comments:
            with open(f"{folder}/comments.json", 'w') as f:
                json.dump(comments, f, indent=4)


def render_all_comments():
    # load links from json
    with open('data/ssc_links.json', 'r') as f:
        links = json.load(f)

    for link in links:
        post_id = link_to_id(link)
        print(post_id)
        if "open-thread" in post_id or "meetup" in post_id:
            print("Skipping open thread or meetup")
            continue

        try:
            with open(f"data/posts/{post_id}/comments.json", 'r') as f:
                comments = json.load(f)
            rendered_comments = render_comments(comments)
        except FileNotFoundError:
            print("No comments found")
            continue

        with open(f"data/posts/{post_id}/rendered_comments.txt", 'w') as f:
            f.write(rendered_comments)
