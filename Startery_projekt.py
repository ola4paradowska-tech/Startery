import os
import re

INPUT_DIR = r"C:\Users\ola4p\Desktop\FASTA"
OUTPUT_DIR = r"C:\Users\ola4p\Desktop\FASTA\Cut"
REPORT_DIR = r"C:\Users\ola4p\Desktop\FASTA\Raport"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

report_data = []

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

    output_file = os.path.join(OUTPUT_DIR, f"{gene}.fasta")

    with open(output_file, "w", encoding="utf-8") as out:
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