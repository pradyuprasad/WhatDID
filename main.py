# imports
import sqlite3
from typing import List, Optional
from sqlite3 import Connection, Cursor
import subprocess
from subprocess import CompletedProcess
from AppKit import NSWorkspace, NSRunningApplication, NSApplicationActivationPolicyRegular
import time
from models import WindowData, Browser




class DB_Cursor:
    __cursor:Optional[Cursor] = None

    @staticmethod
    def get_cursor() -> Cursor:
        if DB_Cursor.__cursor:
            return DB_Cursor.__cursor
        else:
            conn:Connection = sqlite3.connect('tracker.db')
            DB_Cursor.__cursor = conn.cursor()
            return DB_Cursor.__cursor


def run_applescript(applescript_code:str) -> str:
    result:CompletedProcess = subprocess.run(['osascript', '-e', applescript_code], capture_output=True, text=True)
    if result.stderr:
        raise RuntimeError(f"Error while running AppleScript: {result.stderr}")
    return result.stdout.strip()


def create_tables() -> None:
    create_table_statements: List[str] = ['''
                                          CREATE TABLE IF NOT EXISTS tags (
                                          tag_id INTEGER PRIMARY KEY, 
                                          tag_name TEXT);
                                          ''', 
                                          '''
                                        CREATE TABLE IF NOT EXISTS sessions (
                                        session_id INTEGER PRIMARY KEY,
                                        session_name TEXT,
                                        session_start INTEGER, 
                                        session_end INTEGER
                                        );
                                        ''', 
                                        '''
                                        CREATE TABLE IF NOT EXISTS activity (
                                        acitivty_id INTEGER PRIMARY KEY,
                                        application_name TEXT NOT NULL,
                                        is_browser INTEGER NOT NULL CHECK (is_browser = 0 or is_browser = 1),
                                        url TEXT,
                                        title TEXT NOT NULL,
                                        start_time INTEGER NOT NULL,
                                        end_time INTEGER NOT NULL,
                                        tag_id INTEGER,
                                        session_id INTEGER,
                                        FOREIGN KEY (tag_id) REFERENCES tags (tag_id),
                                        FOREIGN KEY (session_id) REFERENCES sessions (session_id)
                                        );
                                        ''']
    try:
        cursor:Cursor = DB_Cursor.get_cursor()
        for statement in create_table_statements:
            cursor.execute(statement)
    except Exception as e:
        print(e)
        raise e

def get_active_window() -> WindowData:
    # Get the currently active (frontmost) application
    workspace = NSWorkspace.sharedWorkspace()
    active_app = workspace.activeApplication()
    print(active_app)
    app_name = active_app['NSApplicationName']
    
    # Get the frontmost app
    frontmost_app = NSRunningApplication.runningApplicationWithProcessIdentifier_(active_app['NSApplicationProcessIdentifier'])
    
    # Try to get the window title
    if frontmost_app.activationPolicy() == NSApplicationActivationPolicyRegular:
        # Use AppleScript to get the window title
        script = f'''
        tell application "System Events"
            tell process "{app_name}"
                return name of first window
            end tell
        end tell
        '''
        try:
            window_title = run_applescript(script)
        except subprocess.CalledProcessError:
            window_title = "Unknown"
    else:
        window_title = "No window"

    
    print(f"Application: {app_name}")
    print(f"Window Title: {window_title}")
    return WindowData(application_name=app_name, title=window_title)



def main():
    create_tables()
    while True:
        currWindownData:WindowData =  get_active_window()
        time.sleep(1)





if __name__ == "__main__":
    main()