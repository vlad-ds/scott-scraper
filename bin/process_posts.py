import json
import os
from typing import List

from ssc_scraper import link_to_id


def process_posts():
    with open('data/ssc_links.json', 'r') as f:
        links = json.load(f)

    for link in links:
        post_id = link_to_id(link)

        with open(f"data/posts/{post_id}/post.json", 'r') as f:
            post_data = json.load(f)

        if not os.path.exists(f"data/summaries/{post_id}"):
            print(f"No summaries found for {post_id}")
            continue

        summary_files: List = os.listdir(f"data/summaries/{post_id}")

        if not len(summary_files):
            print(f"No summaries found for {post_id}")
            continue

        if len(summary_files) == 1:
            with open(f"data/summaries/{post_id}/summary0.txt", 'r') as f:
                summary = f.read()
        else:
            with open(f"data/summaries/{post_id}/summary_consolidated_unified.txt", 'r') as f:
                summary = f.read()

        post_data_final = {
            "title": post_data['title'],
            "date": post_data['date'],
            "links": post_data['links'],
            "url": post_data['url'],
            "summary": summary
        }

        # save in post_processed
        with open(f"data/posts_processed/{post_id}.json", 'w') as f:
            json.dump(post_data_final, f, indent=4)



