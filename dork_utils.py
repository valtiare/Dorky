# dork_utils.py
import webbrowser
from config import GOOGLE_SEARCH_BASE_URL

def get_target_domain():
    return input("Enter the target domain (e.g., example.com): ")

def generate_dorks(category, target_domain):
    base_dork = f"site:{target_domain}"

    if category == 1:
        return [
            f"{base_dork} intitle:foothold",
            f"{base_dork} inurl:login ext:php",
            f"{base_dork} intitle:admin intext:password filetype:log",
            # Add more dorks for category 1 as needed
        ]
    elif category == 2:
        return [
            f"{base_dork} filetype:txt containing usernames",
            f"{base_dork} intext:password filetype:log",
            f"{base_dork} intitle:index.of password",
            # Add more dorks for category 2 as needed
        ]
    elif category == 3:
        return [
            f"{base_dork} intitle:index.of sensitive",
            f"{base_dork} intitle:secret filetype:txt",
            f"{base_dork} inurl:config intext:password",
            # Add more dorks for category 3 as needed
        ]
    # Add more categories and their respective dork logic as needed
    else:
        return []  # Return an empty list for unknown categories

def open_browsers(dorks):
    # Open multiple browsers with the generated dorks
    for dork in dorks:
        webbrowser.open(f"{GOOGLE_SEARCH_BASE_URL}{dork}")
