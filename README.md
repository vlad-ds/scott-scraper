# Summarizing Slate Star Codex

I am sharing the code I used for summarizing SSC as explained in [this post](https://aiprimer.substack.com/p/summarizing-slate-star-codex-a-25). The code is in the form of a Jupyter notebook. You can run it on Google Colab or locally.

This was done very quickly and most of the code was written by ChatGPT and Copilot.

The sequence is roughly the following: 

1. Scrape the posts and put them in data/posts
2. Do one ChatGPT API pass to chunk each post and generate 1+ summaries
3. Find posts which have been chunked and consolidate their summaries. I found it best to simply append the summaries together.
4. In data/posts_processed, add each post as a JSON with its summary.
5. Generate an epub with the post JSONs. 

This could certainly be improved or productized but I will probably not invest any more time in it.