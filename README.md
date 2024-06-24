# WhatDID
Lightweight activity tracker for MacOS

## What this does
- Logs what the active window on your device is, and stores it onto a DB
- This DB is then accessed to understand what you did

# Features for MVP

## Active Window Tracking:
- Track the currently active window/application
- Record time spent on each window/application

## Basic Time-based Summary:
- Generate a summary for today's activities
- Show total time spent on each application

## Simple User Interface:
- A basic web interface accessible via localhost
- Display today's summary
- Start/Stop button for tracking

## Start/Stop Tracking:
- Ability to start and stop tracking via the web interface

## Data Storage:
- Use SQLite database to store activity data locally
- Store timestamp, application name, window title, and duration for each record

## Basic Privacy:
- All data stored locally on the user's machine
- No data sent to external servers

## Lightweight Design:
- Minimal resource usage
- Runs in the background with low system impact

## MacOS Compatibility:
- Designed to work specifically with MacOS
- Utilizes MacOS-specific APIs for window tracking
