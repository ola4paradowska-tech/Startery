import os

INPUT_DIR = r"C:\Users\ola4p\Desktop\FASTA"
CUT_DIR = r"C:\Users\ola4p\Desktop\FASTA\Cut"
REPORT_DIR = r"C:\Users\ola4p\Desktop\FASTA\Raport"

os.makedirs(CUT_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

report_data = []

#PROGRAM
app_data = {
    "gene": "",
    "sequence": "",

    "selected_range": None,
    "range_start": None,
    "range_end": None,

    "primer_name": "",
    "primer_sequence": "",

    "forward_primer": "",
    "reverse_primer": "",

    "sequence_widget": None,
    "start_entry": None,
    "end_entry": None,

    "primer_length": 20,
    "primer_length_entry": None,
    "primer_generated": False,

    "forward_gc": None,
    "reverse_gc": None,
    "forward_tm": None,
    "reverse_tm": None,
    "tm_difference": None,

    "forward_warning": [],
    "reverse_warning": [],

    "right_frame": None,

    "selection_label": None,

    "candidate_start": None,
    "candidate_end": None,

    "candidate_forward": "",
    "candidate_reverse": "",

    "candidate_forward_gc": None,
    "candidate_reverse_gc": None,

    "candidate_forward_tm": None,
    "candidate_reverse_tm": None,

    "candidate_forward_warning": [],
    "candidate_reverse_warning": [],

    "root": None,
    "listbox": None,
}