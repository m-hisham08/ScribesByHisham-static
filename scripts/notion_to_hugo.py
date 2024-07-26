# scripts/notion_to_hugo.py
import os
from notion_client import Client
from notion2md.exporter.block import MarkdownExporter

# Use GitHub Actions secrets for sensitive information
api_key = os.environ['NOTION_API_KEY']
database_id = os.environ['NOTION_DATABASE_ID']

# Set the API key as an environment variable
os.environ['NOTION_TOKEN'] = api_key

# Initialize the Notion client
notion = Client(auth=api_key)

# Query the database to get all pages
results = notion.databases.query(database_id=database_id)

# Create a directory to store the markdown files
output_path = "content/posts"  # This matches your existing structure
os.makedirs(output_path, exist_ok=True)

# Loop through each page in the database
for page in results["results"]:
    page_id = page["id"]
    
    # Get the page title
    try:
        page_title = page["properties"]["Name"]["title"][0]["plain_text"]
    except (KeyError, IndexError):
        page_title = f"Untitled_Page_{page_id}"
    
    try:
        # Use MarkdownExporter to export the page
        MarkdownExporter(block_id=page_id, output_path=output_path, download=True).export()
        print(f"Exported: {page_title}")
    except Exception as e:
        print(f"Error exporting page {page_id}: {str(e)}")

print("All pages processed.")