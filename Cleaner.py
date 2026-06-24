import os
import re
from collections import Counter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Bio import Entrez

Entrez.email = "ola4paradowska@gmail.com"

INPUT_DIR = r"C:\Users\ola4p\Desktop\FASTA"
CUT_DIR = r"C:\Users\ola4p\Desktop\FASTA\Cut"
REPORT_DIR = r"C:\Users\ola4p\Desktop\FASTA\Raport"

os.makedirs(CUT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

report_data = []

root = tk.Tk()
root.title("Gene Data Hub")
root.geometry("850x650")

search_results = []

###POBIERANIE###
def search_gene(gene_name, organism):

    query = f"{gene_name}[Gene] AND {organism}[Organism]"

    handle = Entrez.esearch(
        db="gene",
        term=query,
        retmax=20
    )

    result = Entrez.read(handle)

    ids = result["IdList"]

    if not ids:
        return []

    handle = Entrez.esummary(
        db="gene",
        id=",".join(ids)
    )

    summaries = Entrez.read(handle)

    records = []

    for gene_data in summaries["DocumentSummarySet"]["DocumentSummary"]:
        records.append({
            "id": str(gene_data.attributes["uid"]),
            "name": gene_data["Name"],
            "description": gene_data["Description"],
            "organism": gene_data["Organism"]["ScientificName"]
        })

    return records

def on_search():
    gene = gene_entry.get().strip()
    organism = organism_entry.get().strip()

    global search_results

    search_results = search_gene(gene, organism)

    results_listbox.delete(0, tk.END)

    if not organism:
        messagebox.showwarning(
            "Brak danych",
            "Podaj nazwę organizmu."
        )
        return

    if not gene:
        messagebox.showwarning(
            "Brak danych",
            "Podaj nazwę genu."
        )
        return

    if not search_results:
        messagebox.showerror(
            "Brak wyników",
            "Nie znaleziono genu.\n\nSprawdź poprawność wpisanych danych."
        )
        return

    for record in search_results:
        results_listbox.insert(
            tk.END,
            f"{record['name']} | {record['organism']}"
        )

def on_select(event):
    selected = results_listbox.curselection()

    if not selected:
        return

    index = selected[0]

    record = search_results[index]

    gene_label.config(
        text=f"Gen: {record['name']}"
    )

    organism_label.config(
        text=f"Organizm: {record['organism']}"
    )

    description_label.config(
        text=f"Opis: {record['description']}"
    )

    gene_id_label.config(
        text=f"ID genu: {record['id']}"
    )


###GUI###
search_frame = ttk.LabelFrame(root, text="Wyszukiwanie genu")
search_frame.pack(fill="x", padx=10, pady=10)

ttk.Label(search_frame, text="Nazwa genu:").grid(row=0, column=0, padx=5, pady=5, sticky="w")

gene_entry = ttk.Entry(search_frame, width=40)
gene_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(search_frame, text="Organizm:").grid(row=1, column=0, padx=5, pady=5, sticky="w")

organism_entry = ttk.Entry(search_frame, width=40)
organism_entry.grid(row=1, column=1, padx=5, pady=5)

search_button = ttk.Button(search_frame, text="Wyszukaj", command=on_search)
search_button.grid(row=2, column=0, columnspan=2, pady=10)

results_frame = ttk.LabelFrame(root, text="Wyniki wyszukiwania")
results_frame.pack(fill="both", expand=True, padx=10, pady=10)

results_listbox = tk.Listbox(results_frame, height=10)
results_listbox.pack(fill="both", expand=True, padx=5, pady=5)
results_listbox.bind("<<ListboxSelect>>", on_select)

summary_frame = ttk.LabelFrame(root, text="Informacje o sekwencji")
summary_frame.pack(fill="x", padx=10, pady=10)

gene_label = ttk.Label(summary_frame, text="Gen: -")
gene_label.pack(anchor="w", padx=5, pady=2)

organism_label = ttk.Label(summary_frame, text="Organizm: -")
organism_label.pack(anchor="w", padx=5, pady=2)

description_label = ttk.Label(summary_frame, text="Opis: -")
description_label.pack(anchor="w", padx=5, pady=2)

gene_id_label = ttk.Label(summary_frame, text="ID genu: -")
gene_id_label.pack(anchor="w", padx=5, pady=2)

buttons_frame = ttk.Frame(root)
buttons_frame.pack(fill="x", padx=10, pady=10)

prepare_button = ttk.Button(
buttons_frame,
text="Przygotuj dane"
)
prepare_button.pack(side="left", padx=5)

primer_button = ttk.Button(
buttons_frame,
text="Przejdź do projektowania starterów"
)
primer_button.pack(side="right", padx=5)

root.mainloop()
