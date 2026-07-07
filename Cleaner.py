import os
import tkinter as tk
import subprocess
from tkinter import ttk
from tkinter import messagebox
from Bio import Entrez
from Bio.Seq import Seq

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
selected_record = None

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
    global selected_record
    selected = results_listbox.curselection()

    if not selected:
        return

    index = selected[0]
    selected_record = search_results[index]

    gene_label.config(
        text=f"Gen: {selected_record['name']}"
    )

    organism_label.config(
        text=f"Organizm: {selected_record['organism']}"
    )

    description_label.config(
        text=f"Opis: {selected_record['description']}"
    )

    gene_id_label.config(
        text=f"ID genu: {selected_record['id']}"
    )

def fetch_gene_sequence(gene_id):

    handle = Entrez.esummary(
        db="gene",
        id=gene_id
    )

    summary = Entrez.read(handle)

    gene_data = summary["DocumentSummarySet"]["DocumentSummary"][0]

    location = gene_data["GenomicInfo"][0]

    accession = location["ChrAccVer"]

    chr_start = int(location["ChrStart"])
    chr_stop = int(location["ChrStop"])

    start = min(chr_start, chr_stop)
    end = max(chr_start, chr_stop)

    is_minus = chr_start > chr_stop

    handle = Entrez.efetch(
        db="nucleotide",
        id=accession,
        rettype="fasta",
        retmode="text"
    )

    fasta = handle.read()

    sequence = "".join(
        fasta.splitlines()[1:]
    )

    gene_sequence = sequence[start:end + 1]

    if is_minus:
        gene_sequence = str(
            Seq(gene_sequence).reverse_complement()
        )

    return {
        "sequence": gene_sequence,
        "accession": accession,
        "start": start,
        "end": end,
        "is_minus": is_minus,
        "length": len(gene_sequence)
    }

def save_fasta(gene_info):

    gene_name = make_gene_name()

    filename = f"{gene_name}.fasta"

    filepath = os.path.join(
        CUT_DIR,
        filename
    )

    if os.path.exists(filepath):
        messagebox.showinfo(
            "Informacja",
            "Ten gen został już wcześniej pobrany."
        )
        return False

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(gene_info["sequence"])

    return True

from collections import Counter

def find_invalid(sequence):

    invalid = Counter()

    for base in sequence.upper():

        if base not in {"A", "T", "G", "C"}:
            invalid[base] += 1

    if invalid:

        return ", ".join(
            f"{base}: {count}"
            for base, count in sorted(invalid.items())
        )

    return "brak"

def save_report(gene_info):

    report_file = os.path.join(
        REPORT_DIR,
        "raport.txt"
    )

    invalid_text = find_invalid(
        gene_info["sequence"]
    )

    with open(
        report_file,
        "a",
        encoding="utf-8"
    ) as report:

        report.write(
            "=== RAPORT POBRANIA GENU ===\n\n"
        )

        report.write(
            f"Gen: {selected_record['name']}\n"
        )

        report.write(
            f"ID genu: {selected_record['id']}\n"
        )

        report.write(
            f"Organizm: {selected_record['organism']}\n"
        )

        report.write(
            f"Accession: {gene_info['accession']}\n"
        )

        report.write(
            f"Start: {gene_info['start']}\n"
        )

        report.write(
            f"Stop: {gene_info['end']}\n"
        )

        report.write(
            f"Orientacja minus: {gene_info['is_minus']}\n"
        )

        report.write(
            f"Długość: {gene_info['length']} bp\n"
        )

        report.write(
            f"Nieprawidłowe nukleotydy: {invalid_text}\n"
        )

        report.write(
            "-" * 60 + "\n\n"
        )

def prepare_data():

    if not selected_record:
        messagebox.showwarning(
            "Brak wyboru",
            "Najpierw wybierz gen."
        )
        return

    gene_info = fetch_gene_sequence(
        selected_record["id"]
    )

    saved = save_fasta(gene_info)

    if not saved:
        return

    save_report(gene_info)

    messagebox.showinfo(
        "Gotowe",
        "Dane zostały przygotowane."
    )

def make_gene_name():

    words = selected_record["organism"].split()

    if len(words) >= 2:
        prefix = words[0][0].upper() + words[1][0].lower()
    else:
        prefix = words[0][:2]

    return f"{prefix}{selected_record['name']}"

def open_primer_designer():

    subprocess.Popen([
        "python",
        r"C:\Users\ola4p\PycharmProjects\Startery\Startery_projekt.py"
    ])
    root.destroy()

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

prepare_button = ttk.Button(buttons_frame, text="Przygotuj dane", command=prepare_data)
prepare_button.pack(side="left", padx=5)

primer_button = ttk.Button(
    buttons_frame,
    text="Przejdź do projektowania starterów",
    command=open_primer_designer
)
primer_button.pack(side="right", padx=5)

root.mainloop()
