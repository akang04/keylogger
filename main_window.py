"""
GUI module for keylogger program.
"""

import tkinter as tk


def create_window():
    """Create and configure the main GUI window."""
    root = tk.Tk()
    root.title("For Exiting the Keylogger")
    root.geometry('150x75')

    def raise_exit():
        """Raise SystemExit to terminate the program."""
        raise SystemExit

    exit_button = tk.Button(root, text="Exit", command=raise_exit) 
    exit_button.pack(padx=20)

    return root