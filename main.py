"""
Main module for keylogger program.
"""

from pynput import keyboard
from main_window import create_window
from read_write import read_csv, write_csv, update_key_count
import csv

# Variable declarations
errors = 0
root = create_window()
key_dict = read_csv()
last_session_dict = {}


def get_key_name(key):
    """Convert key object to a string name."""
    try:
        if hasattr(key, 'char') and key.char is not None:
            return key.char
    except AttributeError:
        pass
    
    try:
        key_str = str(key)
        if key_str.startswith('Key.'):
            return key_str[4:]
        if hasattr(key, 'vk'):
            return f"vk_{key.vk}"
        return key_str
    except:
        return str(key)


def on_release(key):
    """Handle key release events and log keystrokes."""
    global errors, last_session_dict
    try:
        key_name = get_key_name(key)
        
        # Skip certain keys
        skip_keys = ['Key.unknown', 'Key.media_play_pause', 'Key.media_volume_up', 'Key.media_volume_down']
        if key_name in skip_keys:
            return
        
        # Update overall dictionary
        if key_name not in key_dict:
            key_dict[key_name] = 0
        key_dict[key_name] = key_dict[key_name] + 1
        
        # Update session dictionary
        if key_name not in last_session_dict:
            last_session_dict[key_name] = 0
        last_session_dict[key_name] = last_session_dict[key_name] + 1
        
        update_key_count(key_dict, key_name)
        
    except Exception as e:
        print(f"ERROR FOUND: {e}")
        errors = errors + 1


def write_last_session_csv():
    """Write last session data to CSV file."""
    filename = "last_session_keystrokes.csv"
    with open(filename, "w", newline="") as file:
        fieldnames = ["Key", "timesPressed"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        for key in last_session_dict:
            writer.writerow({"Key": key, "timesPressed": last_session_dict[key]})


def main():
    """Main function to initialize the keylogger and GUI."""
    try:
        with keyboard.Listener(on_release=on_release) as listener:
            root.mainloop()
            listener.join()

    except SystemExit:
        write_csv(key_dict)
        write_last_session_csv()
        print(f'Number of Errors throughout program runtime: {errors}')
        quit()


if __name__ == "__main__":
    main()

