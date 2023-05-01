import json
import os
from ebooklib import epub
from datetime import datetime


def get_posts():
    # Get a list of all the post files
    post_files = [f for f in os.listdir("data/posts_processed") if f.endswith(".json")]

    # Read in each post and parse the date
    posts = []
    for file in post_files:
        with open(os.path.join("data/posts_processed", file), "r", encoding="utf-8") as f:
            post = json.load(f)
            post_date = datetime.strptime(post["date"], "%B %d, %Y")
            post["date"] = post_date
            posts.append(post)

    # Sort the posts by date
    posts.sort(key=lambda x: x["date"])

    return posts


def create_chapter(post):
    # Create a new chapter
    chapter = epub.EpubHtml(title=post["title"], file_name=f"{post['date'].strftime('%Y%m%d')}.xhtml", lang="en")
    summary = post['summary'].replace('\n', '<br>')
    chapter.content = f"<h1>{post['title']}</h1><p>Date: {post['date'].strftime('%B %d, %Y')}</p><p>URL: {post['url']}</p><p>{summary}</p><ul>"

    # Add the links to the chapter
    for link in post["links"]:
        chapter.content += f"<li><a href='{link}'>{link}</a></li>"
    chapter.content += "</ul>"

    return chapter


def main():
    # Get the list of posts
    posts = get_posts()

    # Create a new epub
    book = epub.EpubBook()
    book.set_title("My Blog")
    book.set_language("en")

    # Add each post as a chapter
    for post in posts:
        chapter = create_chapter(post)
        book.add_item(chapter)
        book.toc.append(chapter)
        book.spine.append(chapter)

    # Save the epub
    epub.write_epub("my_blog.epub", book, {})


if __name__ == "__main__":
    main()
