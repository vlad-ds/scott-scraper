import os
import json

folder_path = "data/posts"
total_content_tokens = 0
total_words = 0

for folder_name in os.listdir(folder_path):
    if "open-thread" not in folder_name and os.path.isdir(os.path.join(folder_path, folder_name)):
        post_file_path = os.path.join(folder_path, folder_name, "post.json")
        with open(post_file_path) as post_file:
            post_data = json.load(post_file)
            total_content_tokens += post_data["content_tokens"]
            total_words += len(post_data["content"].split())

print("The total content tokens is:", total_content_tokens)
print("The total words is:", total_words)
