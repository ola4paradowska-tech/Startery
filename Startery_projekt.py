import os
import re
import tkinter as tk
from tkinter import messagebox

INPUT_DIR = r"C:\Users\ola4p\Desktop\FASTA"
CUT_DIR = r"C:\Users\ola4p\Desktop\FASTA\Cut"
REPORT_DIR = r"C:\Users\ola4p\Desktop\FASTA\Raport"

os.makedirs(CUT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

report_data = []

#CZSZCZENIE
for filename in os.listdir(INPUT_DIR):
    if not filename.lower().endswith((".fasta", ".fa", ".fna")):
        continue

    filepath = os.path.join(INPUT_DIR, filename)

    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    header = lines[0]
    sequence = "".join(lines[1:])

    gene_match = re.search(r"\s([A-Za-z0-9_-]+)\s+\[organism=", header)
    gene = gene_match.group(1) if gene_match else "UNKNOWN_GENE"

    organism_match = re.search(r"\[organism=(.*?)\]", header)
    organism = organism_match.group(1) if organism_match else "UNKNOWN"

    original_length = len(sequence)

    n_count = sequence.upper().count("N")

    cleaned_sequence = re.sub(r"[Nn]", "", sequence)

    final_length = len(cleaned_sequence)

    cut_file = os.path.join(CUT_DIR, f"{gene}.fasta")

    with open(cut_file, "w", encoding="utf-8") as out:
        out.write(cleaned_sequence)

    report_data.append([
        filename,
        gene,
        organism,
        original_length,
        n_count,
        final_length
    ])

report_file = os.path.join(REPORT_DIR, "raport.txt")

with open(report_file, "w", encoding="utf-8") as report:

    report.write("=== RAPORT PRZETWARZANIA FASTA ===\n\n")

    for row in report_data:

        filename = row[0]
        gene = row[1]
        organism = row[2]
        original_length = row[3]
        n_count = row[4]
        final_length = row[5]

        report.write(f"Plik: {filename}\n")
        report.write(f"Gen: {gene}\n")
        report.write(f"Organizm: {organism}\n")
        report.write(f"Długość przed czyszczeniem: {original_length}\n")
        report.write(f"Usunięte N: {n_count}\n")
        report.write(f"Długość po czyszczeniu: {final_length}\n")
        report.write("-" * 50 + "\n")

#PROGRAM
app_data = {
    "gene": "",
    "sequence": "",
    "selected_range": None,
    "primer_name": "",
    "primer_sequence": ""
}
def open_gene_window(gene_name, sequence):

    app_data["gene"] = gene_name
    app_data["sequence"] = sequence

    for widget in root.winfo_children():
        widget.destroy()

    root.title(gene_name)
    root.geometry("1200x800")

    # LEWY PANEL
    left_frame = tk.Frame(root, width=200)
    left_frame.pack(side="left", fill="y")

    # PRAWY PANEL
    right_frame = tk.Frame(root)
    right_frame.pack(side="right", fill="both", expand=True)

    # PRZYCISKI
    sequence_button = tk.Button(
        left_frame,
        text="Sekwencja",
        command=lambda: show_sequence(right_frame)
    )

    sequence_button.pack(fill="x", padx=10, pady=10)

    range_button = tk.Button(
        left_frame,
        text="Wybór zakresu",
        command=lambda: show_range(right_frame)
    )

    range_button.pack(fill="x", padx=10, pady=10)

    primer_button = tk.Button(
        left_frame,
        text="Starter"
    )

    primer_button.pack(fill="x", padx=10, pady=10)

    show_sequence(right_frame)

def show_sequence(right_frame):

    for widget in right_frame.winfo_children():
        widget.destroy()

    title_label = tk.Label(
        right_frame,
        text=app_data["gene"],
        font=("Arial", 16)
    )

    title_label.pack(pady=10)

    text = tk.Text(
        right_frame,
        wrap="word",
        font=("Courier New", 11)
    )

    text.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    text.insert("1.0", app_data["sequence"])

    text.config(state="disabled")

def show_range(right_frame):

    for widget in right_frame.winfo_children():
            widget.destroy()

    title_label = tk.Label(
            right_frame,
            text=app_data["gene"],
            font=("Arial", 16)
        )
    title_label.pack(pady=10)

    controls_frame = tk.Frame(right_frame)
    controls_frame.pack(fill="x", padx=10, pady=10)

    tk.Label(
        controls_frame,
        text="Start:"
    ).grid(row=0, column=0, padx=5)

    start_entry = tk.Entry(
        controls_frame,
        width=10
    )
    start_entry.grid(row=0, column=1, padx=5)

    tk.Label(
        controls_frame,
        text="Koniec:"
    ).grid(row=0, column=2, padx=5)

    end_entry = tk.Entry(
        controls_frame,
        width=10
    )
    end_entry.grid(row=0, column=3, padx=5)

    highlight_button = tk.Button(
        controls_frame,
        text="Podświetl"
    )
    highlight_button.grid(row=0, column=4, padx=10)

    text = tk.Text(
        right_frame,
        wrap="word",
        font=("Courier New", 11)
    )

    text.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    text.insert("1.0", app_data["sequence"])


def select_gene():

    selected = listbox.curselection()

    if not selected:
        messagebox.showwarning(
            "Uwaga",
            "Wybierz gen z listy."
        )
        return

    gene_file = listbox.get(selected[0])

    filepath = os.path.join(CUT_DIR, gene_file)

    with open(filepath, "r", encoding="utf-8") as f:
        sequence = f.read()

    open_gene_window(gene_file, sequence)

root = tk.Tk()
root.title("Wczytaj gen")
root.geometry("400x500")

title_label = tk.Label(
    root,
    text="Wybierz gen",
    font=("Arial", 16)
)
title_label.pack(pady=10)

listbox = tk.Listbox(
    root,
    width=40,
    height=15
)
listbox.pack(padx=10, pady=10)

for file in os.listdir(CUT_DIR):

    if file.endswith(".fasta"):
        listbox.insert(tk.END, file)

select_button = tk.Button(
    root,
    text="Wczytaj gen",
    command=select_gene
)
select_button.pack(pady=10)

root.mainloop()

