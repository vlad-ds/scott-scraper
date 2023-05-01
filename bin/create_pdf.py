import os
import json
from datetime import datetime
from PyPDF2 import PdfMerger, PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Step 1: Read all the blog posts from the folder data/posts_processed.
posts = []
for filename in os.listdir("data/posts_processed"):
    with open(os.path.join("data/posts_processed", filename), "r") as f:
        post = json.load(f)
        posts.append(post)

# Step 2: Order the posts by date.
posts.sort(key=lambda x: datetime.strptime(x["date"], "%B %d, %Y"))

# Step 3: Create a PDF file.
pdf_filename = "blog_posts.pdf"
merger = PdfMerger()

# Step 4 and 5: For each blog post, create a chapter in the PDF.
for post in posts:
    # Create a new page in the PDF.
    canvas_obj = canvas.Canvas("temp.pdf", pagesize=letter)

    # Add the title, date, and URL of the post.
    canvas_obj.setFont("Helvetica-Bold", 16)
    canvas_obj.drawString(50, 750, post["title"])

    canvas_obj.setFont("Helvetica", 12)
    canvas_obj.drawString(50, 725, post["date"])
    canvas_obj.drawString(50, 700, post["url"])

    # Add the summary of the post.
    canvas_obj.setFont("Helvetica", 12)
    canvas_obj.drawString(50, 650, "Summary:")
    summary_text = canvas_obj.beginText(50, 625)
    summary_text.setFont("Helvetica", 12)
    summary_text.textLines(post["summary"])
    canvas_obj.drawText(summary_text)

    # Add the links in the post, if any.
    if post["links"]:
        canvas_obj.setFont("Helvetica", 12)
        canvas_obj.drawString(50, 550, "Links:")
        link_text = canvas_obj.beginText(50, 525)
        link_text.setFont("Helvetica", 12)
        for link in post["links"]:
            link_text.textLine(link)
        canvas_obj.drawText(link_text)

    # Save the page to a temporary PDF file.
    canvas_obj.save()

    # Add the temporary PDF file to the final PDF.
    merger.append(PdfReader(open("temp.pdf", "rb")))

    # Delete the temporary PDF file.
    os.remove("temp.pdf")

# Write the final PDF file.
merger.write(pdf_filename)
merger.close()
