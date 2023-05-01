import json
import os

from ssc_scraper import link_to_id


def unify_consolidated_summary(link):
    id_ = link_to_id(link)

    if not os.path.exists(f'data/summaries/{id_}/summary_consolidated.txt'):
        print(f"No consolidated summary. Skipping.")
        return

    # Open the input file for reading
    with open(f'data/summaries/{id_}/summary_consolidated.txt', 'r') as f:
        lines = f.readlines()

    # Initialize variables for each section
    key_ideas = []
    key_learnings = []
    key_questions = []

    # Loop over each line in the input file and add it to the appropriate section
    current_section = None
    for line in lines:
        if line.lower().startswith('key ideas'):
            current_section = key_ideas
        elif line.lower().startswith('key learnings'):
            current_section = key_learnings
        elif line.lower().startswith('key questions'):
            current_section = key_questions
        elif line.startswith('-'):
            current_section.append(line.strip())

    # Open the output file for writing
    with open(f'data/summaries/{id_}/summary_consolidated_unified.txt', 'w') as f:
        # Write the key ideas section
        f.write('Key ideas:\n')
        for idea in key_ideas:
            f.write(idea + '\n')

        # Write the key learnings section
        f.write('\nKey learnings:\n')
        for learning in key_learnings:
            f.write(learning + '\n')

        # Write the key questions section
        f.write('\nKey questions:\n')
        for question in key_questions:
            f.write(question + '\n')


def unify_all_summaries():
    # load links from json
    with open('data/ssc_links.json', 'r') as f:
        links = json.load(f)

    for link in links:
        print(link)
        unify_consolidated_summary(link)