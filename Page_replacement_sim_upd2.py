import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt

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

# ------------------ Visualization ------------------
def plot_history(history, page_refs, hits, misses, algorithm):
    fig, ax = plt.subplots(figsize=(8, 6))

    # Ensure all lists in history are of the same length (pad with -1 if needed)
    max_len = max(len(x) for x in history)
    history = [x + [-1] * (max_len - len(x)) for x in history]

    ax.imshow(np.array(history).T, cmap="Blues", aspect="auto")

    ax.set_xticks(range(len(page_refs)))
    ax.set_xticklabels(page_refs)
    ax.set_yticks(range(len(history[0])))
    ax.set_yticklabels([f"Frame {i+1}" for i in range(len(history[0]))])

    ax.set_xlabel("Page References")
    ax.set_ylabel("Frames")
    ax.set_title(f"{algorithm} Page Replacement Visualization")

    # Display hit & miss ratio
    hit_ratio = hits / (hits + misses)
    miss_ratio = misses / (hits + misses)

    plt.figtext(0.15, 0.01, f"Hits: {hits}, Misses: {misses}, Hit Ratio: {hit_ratio:.2f}, Miss Ratio: {miss_ratio:.2f}", fontsize=10, bbox={"facecolor":"white", "alpha":0.5, "pad":5})

    plt.show()

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

        # Plot visualization
        plot_history(history, page_refs, hits, misses, selected_algo)

    except ValueError:
        messagebox.showerror("Error", "Invalid input! Please enter space-separated integers for reference string.")

# ------------------ Main GUI Window ------------------
root = tk.Tk()
root.title("Page Replacement Algorithm Simulator")
root.geometry("500x400")
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

# Start GUI Loop
root.mainloop()
