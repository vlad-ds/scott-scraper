import os
import json
from datetime import datetime

# Step 1: Read all the blog posts from the folder data/posts_processed.
posts = []
for filename in os.listdir("data/posts_processed"):
    with open(os.path.join("data/posts_processed", filename), "r") as f:
        post = json.load(f)
        posts.append(post)

# Step 2: Order the posts by date.
posts.sort(key=lambda x: datetime.strptime(x["date"], "%B %d, %Y"))

# Step 3: Create a Markdown file.
md_filename = "blog_posts.md"
with open(md_filename, "w") as f:
    # Step 4 and 5: For each blog post, create a chapter in the Markdown file.
    for post in posts:
        # Add the title, date, and URL of the post.
        f.write(f"# {post['title']}\n")
        f.write(f"*{post['date']}*\n")
        f.write(f"{post['url']}\n")

        # Add the summary of the post.
        f.write("\n## Summary\n")
        f.write(f"{post['summary']}\n")

        # Add the links in the post, if any.
        if post["links"]:
            f.write("\n## Links\n")
            for link in post["links"]:
                f.write(f"- {link}\n")

        # Add a horizontal line to separate the chapters.
        f.write("\n---\n")
