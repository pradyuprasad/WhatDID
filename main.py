import pygetwindow as gw  # type: ignore[import]
from typing import List, Tuple, Optional, Any
import subprocess
import time
import sqlite3
from datetime import datetime
from .models import Browser

# Function to get active tab details from Brave Browser using AppleScript
def get_browser_tab_details(browser: Browser) -> Tuple[Optional[str], Optional[str]]:
    script_template = """
    tell application "{browser}"
        set the_url to {url_command}
        set the_title to {title_command}
        return the_title & "\n" & the_url
    end tell
    """

    url_command = {
        Browser.SAFARI: "URL of front document",
        Browser.CHROME: "URL of active tab of front window",
        Browser.FIREFOX: "URL of active tab of front window",
        Browser.BRAVE: "URL of active tab of front window",
        Browser.EDGE: "URL of active tab of front window"
    }

    title_command = {
        Browser.SAFARI: "name of front document",
        Browser.CHROME: "title of active tab of front window",
        Browser.FIREFOX: "title of active tab of front window",
        Browser.BRAVE: "title of active tab of front window",
        Browser.EDGE: "title of active tab of front window"
    }

    script = script_template.format(
        browser=browser.value,
        url_command=url_command[browser],
        title_command=title_command[browser]
    )

    try:
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        if result.stdout:
            output = result.stdout.strip().split('\n')
            if len(output) == 2:
                return output[0], output[1]
    except Exception as e:
        print(f"Error retrieving browser tab info for {browser.value}: {e}")
    return None, None


# Function to store window information in the SQLite database
def store_window_info(db_conn:Any, window_name:str, url:Optional[str], title:Optional[str]) -> None:
    cursor = db_conn.cursor()
    timestamp = int(time.time())
    print("inserting with timestamp", timestamp, "window_name", window_name, "url", url, "title", title)
    cursor.execute("INSERT INTO window_info (timestamp, window_name, url, title) VALUES (?, ?, ?, ?)",
                   (timestamp, window_name, url, title))
    db_conn.commit()

def return_browser_type(title: str) -> Optional[Browser]:
    for browser in Browser:
        if browser.value in title:
            return browser

    return None

# Main function to set up the database and start monitoring
def main() -> None:
    # Set up the SQLite database
    db_conn = sqlite3.connect('window_info.db')
    cursor = db_conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS window_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER NOT NULL,
            window_name TEXT NOT NULL,
            url TEXT,
            title TEXT
        )
    ''')
    db_conn.commit()

    try:
        while True:
            current_window = gw.getActiveWindow()
            if current_window is not None:
                window_title = current_window.title()
                browser_type = return_browser_type(window_title)
                if browser_type:
                    url, text = get_browser_tab_details(browser_type)
                    store_window_info(db_conn, window_title, url, text)
                else:
                    store_window_info(db_conn, window_title, None, None)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopped monitoring.")
    finally:
        db_conn.close()

if __name__ == '__main__':
    main()

