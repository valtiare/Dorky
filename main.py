# main.py
import os
import webbrowser
from stem import Signal
from stem.control import Controller
from dork_utils import generate_dorks, get_target_domain
from categories import categories
from config import LOG_FILE_PATH, TOR_BROWSER_URL

RESULTS_FOLDER = "results"
DATA_FOLDER = "data"  

def log_search_history(dorks, results_folder):
    result_file_path = os.path.join(results_folder, "search_results.txt")
    with open(result_file_path, "a") as result_file:
        result_file.write("\n".join(dorks))
        result_file.write("\n\n")

def start_tor():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)

def open_browser(urls, proxies=None):
    for url in urls:
        webbrowser.open_new_tab(url)

def get_input_from_file(prompt):
    file_option = input(f"Do you want to provide {prompt} through a file? (yes/no): ").lower()
    if file_option == 'yes':
        file_path = input(f"Enter the path to the {prompt} file: ")
        if not os.path.exists(file_path):
            print(f"Error: File '{file_path}' not found.")
            return None
        with open(file_path, 'r') as file:
            return file.read().splitlines()
    else:
        user_input = input(f"Enter {prompt} (separated by commas if multiple): ")
        return user_input.split(',')

def read_proxies():
    proxies_file_path = os.path.join(DATA_FOLDER, "proxy.txt")
    if not os.path.exists(proxies_file_path):
        print("Proxy file 'proxy.txt' not found.")
        return None
    with open(proxies_file_path, 'r') as proxies_file:
        return proxies_file.read().splitlines()

def main():
    print("Welcome to Dorky - Your Advanced Google Dork Tool!")

    target_option = input("Choose a target option (single/batch/custom/none): ").lower()

    if target_option == 'single':
        target_domain = get_target_domain()
    elif target_option == 'batch':
        batch_targets = get_input_from_file("batch targets")
        if batch_targets is None:
            return
    elif target_option == 'custom':
        custom_dorks = get_input_from_file("custom dorks")
        if custom_dorks is None:
            return
    elif target_option == 'none':
        target_domain = None
    else:
        print("Invalid target option. Exiting.")
        return

    choose_site = input("Do you want to choose a specific site? (yes/no): ").lower()
    if choose_site == 'yes':
        target_domain = input("Enter the site you want to target (e.g., example.com): ")

    print("Choose a category:")
    for key, value in categories.items():
        print(f"{key}. {value}")

    selected_category = int(input("Enter the number of the category: "))

    use_tor = input("Do you want to use Tor for Google Dorking? (yes/no): ").lower() == 'yes'

    use_proxies = input("Do you want to use proxies? (yes/no): ").lower() == 'yes'
    proxies = read_proxies() if use_proxies else None

    if use_tor:
        try:
            with Controller.from_port(port=9051) as controller:
                controller.authenticate()
                print("Tor is already running.")
        except:
            print("Tor is not running. Opening Tor Browser download page...")
            webbrowser.open(TOR_BROWSER_URL)
            return

    if use_tor:
        start_tor()

    if not os.path.exists(RESULTS_FOLDER):
        os.makedirs(RESULTS_FOLDER)
        
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)

    if target_option == 'single' or target_option == 'none':
        dorks = generate_dorks(selected_category, target_domain)
    elif target_option == 'batch':
        dorks = []
        for target_domain in batch_targets:
            dorks.extend(generate_dorks(selected_category, target_domain))
    elif target_option == 'custom':
        dorks = custom_dorks
    else:
        return

    urls = [f"https://www.google.com/search?q={dork}" for dork in dorks]

    open_browser(urls, proxies=proxies)

    log_search_history(dorks, RESULTS_FOLDER)

if __name__ == "__main__":
    main()
