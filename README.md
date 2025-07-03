# Keylogger Program

A simple Python keylogger that tracks keystrokes and provides statistical analysis with visualizations. From this project, I was able to learn to handle csvs and create graphs using python libraries.

## Features

- **Real-time keystroke tracking**: Monitors and logs all keyboard input
- **CSV data storage**: Saves keystroke data in structured CSV format
- **Session tracking**: Separates overall statistics from current session data
- **Visual statistics**: Four pie charts showing most/least used keys
- **Scrollable table**: Complete view of all keystroke data
- **Simple GUI**: Easy-to-use interface for program control

 # Statistics Features

- **Overall statistics**: Long-term keystroke patterns
- **Session statistics**: Current session analysis
- **Top 10 most/least used keys**: Visual pie charts
- **Complete data table**: All keys with counts and percentages

## Files

- `main.py` - Main keylogger program 
- `main_window.py` - Module for GUI window for program control
- `read_write.py` -  Module for CSV file handling functions
- `statistics.py` - Module for Data analysis and visualization
- `requirements.txt` - Contains Python package dependencies

## Requirements

- Python 3.6+
- pynput (for keyboard monitoring)
- matplotlib (for charts)
- tkinter (for GUI, usually included with Python) 
