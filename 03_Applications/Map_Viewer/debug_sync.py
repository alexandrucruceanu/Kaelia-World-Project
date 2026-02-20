
import sys
import os

print("DEBUG: Starting wrapper...")
try:
    # Add scripts to path
    sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))
    import sync_wiki
    print("DEBUG: Imported sync_wiki")
    
    sync_wiki.sync_wiki()
    print("DEBUG: Finished sync_wiki")
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f"DEBUG: Error: {e}")
