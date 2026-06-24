import os
import re
from collections import Counter
import tkinter as tk
from tkinter import ttk
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

    results = search_gene(gene, organism)

    results_listbox.delete(0, tk.END)

    for record in results:
        results_listbox.insert(
            tk.END,
            f"{record['name']} | {record['organism']}"
        )




#def fetch_fasta(record_id):
#pass

#def analyze_sequence(sequence):
#pass

#def save_fasta(sequence, gene, organism):
#pass

#def save_report(report_data):
#pass

#def prepare_data(record_id):
#fasta = fetch_fasta(record_id)

#```
#analysis = analyze_sequence(fasta)

#save_fasta(...)

#save_report(...)

#return analysis
#```

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

summary_frame = ttk.LabelFrame(root, text="Informacje o sekwencji")
summary_frame.pack(fill="x", padx=10, pady=10)

gene_label = ttk.Label(summary_frame, text="Gen: -")
gene_label.pack(anchor="w", padx=5, pady=2)

organism_label = ttk.Label(summary_frame, text="Organizm: -")
organism_label.pack(anchor="w", padx=5, pady=2)

length_label = ttk.Label(summary_frame, text="Długość: -")
length_label.pack(anchor="w", padx=5, pady=2)

invalid_label = ttk.Label(summary_frame, text="Nietypowe nukleotydy: -")
invalid_label.pack(anchor="w", padx=5, pady=2)

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
