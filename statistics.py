"""
Statistics module for keylogger program.
"""

import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import ttk
import threading
from read_write import read_csv
import csv


def read_last_session():
    """Read keystroke data from the last session CSV file."""
    try:
        with open("last_session_keystrokes.csv", "r") as file:
            csv_file = csv.reader(file)
            key_counts = {}
            for row in csv_file:
                if len(row) >= 2:
                    key_counts[row[0]] = int(row[1])
            return key_counts
    except FileNotFoundError:
        return {}


def get_top_keys(key_dict, top_n=10, most_used=True):
    """Get the top N most or least used keys."""
    if not most_used:
        filtered_dict = {}
        for k, v in key_dict.items():
            if v > 0:
                filtered_dict[k] = v
    else:
        filtered_dict = key_dict
    
    sorted_keys = sorted(filtered_dict.items(), key=lambda x: x[1], reverse=most_used)
    return sorted_keys[:top_n]


def create_usage_graphs():
    """Create and display pie charts for most and least used keys."""
    key_dict = read_csv()
    last_session_dict = read_last_session()
    
    if not key_dict and not last_session_dict:
        print("No keystroke data found. Please run the keylogger first.")
        return
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    if key_dict:
        most_used = get_top_keys(key_dict, 10, most_used=True)
        if most_used:
            keys, counts = zip(*most_used)
            colors = ['#1e3a8a', '#1e40af', '#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe', '#dbeafe', '#eff6ff', '#f0f9ff', '#f8fafc'][:len(keys)]
            
            wedges, texts, autotexts = ax1.pie(counts, labels=keys, autopct='%1.1f%%', 
                                              colors=colors, startangle=90)
            ax1.set_title('Overall Top 10 Most Used Keys', fontsize=12, fontweight='bold')
            
            for autotext in autotexts:
                autotext.set_color('black')
                autotext.set_fontweight('bold')
    
    if key_dict:
        least_used = get_top_keys(key_dict, 10, most_used=False)
        if least_used:
            keys, counts = zip(*least_used)
            colors = ['#ff6b6b', '#ff8e8e', '#ffb1b1', '#ffd4d4', '#ffe6e6', '#ff9999', '#ffcccc', '#ffb3b3', '#ffa6a6', '#ff9999'][:len(keys)]
            
            wedges, texts, autotexts = ax2.pie(counts, labels=keys, autopct='%1.1f%%', 
                                              colors=colors, startangle=90)
            ax2.set_title('Overall Top 10 Least Used Keys', fontsize=12, fontweight='bold')
            
            for autotext in autotexts:
                autotext.set_color('black')
                autotext.set_fontweight('bold')
    
    if last_session_dict:
        most_used_session = get_top_keys(last_session_dict, 10, most_used=True)
        if most_used_session:
            keys, counts = zip(*most_used_session)
            colors = ['#059669', '#10b981', '#34d399', '#6ee7b7', '#a7f3d0', '#d1fae5', '#ecfdf5', '#f0fdf4', '#f7fee7', '#fefce8'][:len(keys)]
            
            wedges, texts, autotexts = ax3.pie(counts, labels=keys, autopct='%1.1f%%', 
                                              colors=colors, startangle=90)
            ax3.set_title('Last Session Top 10 Most Used Keys', fontsize=12, fontweight='bold')
            
            for autotext in autotexts:
                autotext.set_color('black')
                autotext.set_fontweight('bold')
    
    if last_session_dict:
        least_used_session = get_top_keys(last_session_dict, 10, most_used=False)
        if least_used_session:
            keys, counts = zip(*least_used_session)
            colors = ['#dc2626', '#ef4444', '#f87171', '#fca5a5', '#fecaca', '#fecaca', '#fca5a5', '#f87171', '#ef4444', '#dc2626'][:len(keys)]
            
            wedges, texts, autotexts = ax4.pie(counts, labels=keys, autopct='%1.1f%%', 
                                              colors=colors, startangle=90)
            ax4.set_title('Last Session Top 10 Least Used Keys', fontsize=12, fontweight='bold')
            
            for autotext in autotexts:
                autotext.set_color('black')
                autotext.set_fontweight('bold')
    
    plt.tight_layout()
    plt.show()


def create_key_table():
    """Create a scrollable table showing all key presses."""
    key_dict = read_csv()
    
    if not key_dict:
        print("No keystroke data found. Please run the keylogger first.")
        return
    
    root = tk.Tk()
    root.title("Key Press Statistics Table")
    root.geometry("600x400")
    
    total_presses = sum(key_dict.values())
    
    frame = ttk.Frame(root)
    frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    tree = ttk.Treeview(frame, columns=('Key', 'Presses', 'Percentage'), show='headings', height=15)
    
    tree.heading('Key', text='Key')
    tree.heading('Presses', text='Presses')
    tree.heading('Percentage', text='Percentage')
    
    tree.column('Key', width=150, anchor='w')
    tree.column('Presses', width=100, anchor='center')
    tree.column('Percentage', width=100, anchor='center')
    
    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    
    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')
    
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(0, weight=1)
    
    sorted_keys = sorted(key_dict.items(), key=lambda x: x[1], reverse=True)
    
    for key, count in sorted_keys:
        percentage = (count / total_presses) * 100 if total_presses > 0 else 0
        tree.insert('', 'end', values=(key, count, f"{percentage:.1f}%"))
    
    summary_frame = ttk.Frame(root)
    summary_frame.pack(fill='x', padx=10, pady=(0, 10))
    
    ttk.Label(summary_frame, text=f"Total Keys: {len(key_dict)}").pack(side='left')
    ttk.Label(summary_frame, text=f"Total Presses: {total_presses}").pack(side='left', padx=(20, 0))
    ttk.Label(summary_frame, text=f"Average per Key: {total_presses/len(key_dict):.1f}").pack(side='left', padx=(20, 0))
    
    def refresh_table():
        """Refresh the table with current data."""
        for item in tree.get_children():
            tree.delete(item)
        
        key_dict = read_csv()
        total_presses = sum(key_dict.values())
        sorted_keys = sorted(key_dict.items(), key=lambda x: x[1], reverse=True)
        
        for key, count in sorted_keys:
            percentage = (count / total_presses) * 100 if total_presses > 0 else 0
            tree.insert('', 'end', values=(key, count, f"{percentage:.1f}%"))
    
    refresh_btn = ttk.Button(root, text="Refresh Data", command=refresh_table)
    refresh_btn.pack(pady=(0, 10))
    
    root.mainloop()


def print_statistics():
    """Print basic statistics about keystroke usage."""
    key_dict = read_csv()
    last_session_dict = read_last_session()
    
    if not key_dict and not last_session_dict:
        print("No keystroke data found.")
        return
    
    print("\n=== OVERALL KEYSTROKE STATISTICS ===")
    if key_dict:
        total_keys = len(key_dict)
        total_presses = sum(key_dict.values())
        most_used = get_top_keys(key_dict, 5, most_used=True)
        least_used = get_top_keys(key_dict, 5, most_used=False)
        
        print(f"Total unique keys tracked: {total_keys}")
        print(f"Total key presses: {total_presses}")
        print(f"Average presses per key: {total_presses/total_keys:.2f}")
        
        print("\nTop 5 Most Used Keys:")
        for i, (key, count) in enumerate(most_used, 1):
            percentage = (count / total_presses) * 100
            print(f"  {i}. {key}: {count} presses ({percentage:.1f}%)")
        
        print("\nTop 5 Least Used Keys (with at least 1 press):")
        for i, (key, count) in enumerate(least_used, 1):
            percentage = (count / total_presses) * 100
            print(f"  {i}. {key}: {count} presses ({percentage:.1f}%)")
    
    print("\n=== LAST SESSION STATISTICS ===")
    if last_session_dict:
        session_keys = len(last_session_dict)
        session_presses = sum(last_session_dict.values())
        most_used_session = get_top_keys(last_session_dict, 5, most_used=True)
        least_used_session = get_top_keys(last_session_dict, 5, most_used=False)
        
        print(f"Last session unique keys: {session_keys}")
        print(f"Last session total presses: {session_presses}")
        print(f"Last session average per key: {session_presses/session_keys:.2f}")
        
        print("\nLast Session Top 5 Most Used Keys:")
        for i, (key, count) in enumerate(most_used_session, 1):
            percentage = (count / session_presses) * 100
            print(f"  {i}. {key}: {count} presses ({percentage:.1f}%)")
        
        print("\nLast Session Top 5 Least Used Keys (with at least 1 press):")
        for i, (key, count) in enumerate(least_used_session, 1):
            percentage = (count / session_presses) * 100
            print(f"  {i}. {key}: {count} presses ({percentage:.1f}%)")


def show_all_statistics():
    """Show all statistics windows simultaneously."""
    print_statistics()
    
    close_event = threading.Event()
    
    def show_charts():
        create_usage_graphs()
        close_event.set()
    
    def show_table():
        create_key_table()
        close_event.set()
    
    charts_thread = threading.Thread(target=show_charts, daemon=True)
    table_thread = threading.Thread(target=show_table, daemon=True)
    
    charts_thread.start()
    table_thread.start()
    
    close_event.wait()
    
    import os
    os._exit(0)


if __name__ == "__main__":
    show_all_statistics() 