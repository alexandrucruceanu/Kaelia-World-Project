import os
import re
from html.parser import HTMLParser

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for name, value in attrs:
                if name == "href":
                    self.links.append(value)

def verify_links(wiki_dir):
    broken_links = []
    total_links = 0
    
    for root, dirs, files in os.walk(wiki_dir):
        for file in files:
            if file.endswith(".html"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                parser = LinkParser()
                parser.feed(content)
                
                for link in parser.links:
                    if link.startswith("http") or link.startswith("#") or link.startswith("mailto:"):
                        continue
                    
                    total_links += 1
                    # Resolve relative path
                    link_path = os.path.normpath(os.path.join(root, link))
                    # Basic check: remove anchor if present
                    link_path = link_path.split('#')[0]
                    
                    if not os.path.exists(link_path):
                        broken_links.append((file_path, link, link_path))
    
    return total_links, broken_links

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    WIKI_DIR = os.path.join(BASE_DIR, 'wiki')
    
    print(f"Verifying links in: {WIKI_DIR}")
    total, broken = verify_links(WIKI_DIR)
    
    print(f"Total internal links checked: {total}")
    if broken:
        print(f"Found {len(broken)} broken links:")
        for source, link, resolved in broken:
            print(f" - In {os.path.relpath(source, WIKI_DIR)}: '{link}' -> {os.path.relpath(resolved, WIKI_DIR) if os.path.commonpath([resolved, WIKI_DIR]) == WIKI_DIR else resolved}")
    else:
        print("All internal links are working!")
