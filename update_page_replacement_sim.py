import tkinter as tk
from tkinter import ttk, messagebox
import time

# ------------------ Page Replacement Algorithms ------------------

def fifo_page_replacement(pages, frames):
    frame_list = []
    history = []
    hits, misses = 0, 0

    for page in pages:
        if page in frame_list:
            hits += 1
        else:
            misses += 1
            if len(frame_list) < frames:
                frame_list.append(page)
            else:
                frame_list.pop(0)
                frame_list.append(page)
        history.append(frame_list.copy())

    return history, hits, misses

def lru_page_replacement(pages, frames):
    frame_list = []
    history = []
    hits, misses = 0, 0
    page_order = []

    for page in pages:
        if page in frame_list:
            hits += 1
            page_order.remove(page)
        else:
            misses += 1
            if len(frame_list) < frames:
                frame_list.append(page)
            else:
                lru_page = page_order.pop(0)
                frame_list[frame_list.index(lru_page)] = page

        page_order.append(page)
        history.append(frame_list.copy())

    return history, hits, misses

def optimal_page_replacement(pages, frames):
    frame_list = []
    history = []
    hits, misses = 0, 0

    for i in range(len(pages)):
        page = pages[i]

        if page in frame_list:
            hits += 1
        else:
            misses += 1
            if len(frame_list) < frames:
                frame_list.append(page)
            else:
                future_use = {frame: pages[i+1:].index(frame) if frame in pages[i+1:] else float('inf') for frame in frame_list}
                page_to_replace = max(future_use, key=future_use.get)
                frame_list[frame_list.index(page_to_replace)] = page

        history.append(frame_list.copy())

    return history, hits, misses

# ------------------ Text-Based Visualization ------------------

def display_table(history, pages, frames):
    table_output = ""
    column_width = 4

    # Top Header
    table_output += "Pages:  " + "  ".join(f"{page:>{column_width}}" for page in pages) + "\n"
    table_output += "+" + ("-" * (column_width + 1)) * len(pages) + "+\n"

    # Frame Rows
    for i in range(frames):
        row = [f"Frame {i+1} |"]
        for step in history:
            if i < len(step):
                row.append(f"{step[i]:>{column_width}}")
            else:
                row.append(" " * column_width)
        table_output += " | ".join(row) + " |\n"
        table_output += "+" + ("-" * (column_width + 1)) * len(pages) + "+\n"

    return table_output

# ------------------ GUI Implementation ------------------

def run_simulation():
    try:
        page_refs = list(map(int, entry_pages.get().split()))
        num_frames = int(entry_frames.get())
        selected_algo = algo_var.get()

        if num_frames <= 0:
            messagebox.showerror("Error", "Number of frames must be greater than 0!")
            return
        
        if not page_refs:
            messagebox.showerror("Error", "Reference string cannot be empty!")
            return

        if selected_algo == "FIFO":
            history, hits, misses = fifo_page_replacement(page_refs, num_frames)
        elif selected_algo == "LRU":
            history, hits, misses = lru_page_replacement(page_refs, num_frames)
        elif selected_algo == "Optimal":
            history, hits, misses = optimal_page_replacement(page_refs, num_frames)
        else:
            messagebox.showerror("Error", "Invalid algorithm selected!")
            return

        # Computation Outline
        result_text.set(
            f"Algorithm: {selected_algo}\n"
            f"Frames: {num_frames}\n"
            f"Reference Length: {len(page_refs)}\n"
            f"Reference String: {page_refs}\n\n"
            f"Page Faults: {misses}\n"
            f"Hit Ratio: {hits / (hits + misses):.2f}\n"
            f"Miss Ratio: {misses / (hits + misses):.2f}"
        )

        # Display Table-Based Visualization
        text_area.config(state="normal")
        text_area.delete("1.0", tk.END)
        text_area.insert(tk.END, display_table(history, page_refs, num_frames))
        text_area.config(state="disabled")

    except ValueError:
        messagebox.showerror("Error", "Invalid input! Please enter space-separated integers for reference string.")

# ------------------ Main GUI Window ------------------

root = tk.Tk()
root.title("Page Replacement Algorithm Simulator")
root.geometry("700x500")
root.configure(bg="lightgray")

# Title Label
tk.Label(root, text="Page Replacement Algorithm Simulator", font=("Arial", 14, "bold"), bg="lightgray").pack(pady=10)

# Algorithm Selection
tk.Label(root, text="Select Algorithm:", bg="lightgray").pack()
algo_var = tk.StringVar(value="FIFO")
algo_menu = ttk.Combobox(root, textvariable=algo_var, values=["FIFO", "LRU", "Optimal"], state="readonly")
algo_menu.pack(pady=5)

# Number of Frames
tk.Label(root, text="Enter Number of Frames:", bg="lightgray").pack()
entry_frames = tk.Entry(root)
entry_frames.pack(pady=5)

# Reference String Input
tk.Label(root, text="Enter Reference String (space-separated):", bg="lightgray").pack()
entry_pages = tk.Entry(root)
entry_pages.pack(pady=5)

# Run Button
tk.Button(root, text="Run Simulation", command=run_simulation, bg="blue", fg="white").pack(pady=10)

# Results Display
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, justify="left", bg="white", font=("Courier", 10), relief="solid", padx=10, pady=5)
result_label.pack(pady=10, fill="both")

# Text Area for Table-Based Visualization
text_area = tk.Text(root, height=15, font=("Courier", 10), state="disabled", wrap="none")
text_area.pack(pady=10, padx=10, fill="both")

# Start GUI Loop
root.mainloop()
