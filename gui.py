import tkinter as tk
from tkinter import messagebox

from config import *
from primers import *

def open_gene_window(gene_name, sequence):

    app_data["gene"] = gene_name
    app_data["sequence"] = sequence

    for widget in app_data["root"].winfo_children():
        widget.destroy()

    app_data["root"].title(gene_name)
    app_data["root"].geometry("1200x800")

    left_frame = tk.Frame(app_data["root"], width=200)
    left_frame.pack(side="left", fill="y")

    right_frame = tk.Frame(app_data["root"])
    right_frame.pack(side="right", fill="both", expand=True)

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
        text="Starter",
        command=lambda: show_primer(right_frame)
    )

    primer_button.pack(fill="x", padx=30, pady=10)

    show_sequence(right_frame)

def highlight_selected_region(text):

    text.config(state="normal")

    text.tag_remove("fragment", "1.0", tk.END)
    text.tag_remove("forward", "1.0", tk.END)
    text.tag_remove("reverse", "1.0", tk.END)

    if app_data["selected_range"] is None:
        text.config(state="disabled")
        return

    start = app_data["range_start"]
    end = app_data["range_end"]

    text.tag_add(
        "fragment",
        f"1.{start-1}",
        f"1.{end}"
    )

    text.tag_config(
        "fragment",
        background="yellow"
    )

    if (
        app_data["forward_primer"]
        and app_data["reverse_primer"]
    ):

        primer_length = len(app_data["forward_primer"])

        text.tag_add(
            "forward",
            f"1.{start-1}",
            f"1.{start-1+primer_length}"
        )

        text.tag_config(
            "forward",
            background="lightgreen"
        )

        text.tag_add(
            "reverse",
            f"1.{end-primer_length}",
            f"1.{end}"
        )

        text.tag_config(
            "reverse",
            background="salmon"
        )

    text.config(state="disabled")



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
    app_data["sequence_widget"] = text
    highlight_selected_region(text)

def highlight_range():

    try:
        start = int(app_data["start_entry"].get())
        end = int(app_data["end_entry"].get())

    except ValueError:
        messagebox.showerror(
            "Błąd",
            "Start i Koniec muszą być liczbami."
        )
        return

    sequence_length = len(app_data["sequence"])

    if start < 1:
        messagebox.showerror(
            "Błąd",
            "Start musi być większy od 0."
        )
        return

    if end > sequence_length:
        messagebox.showerror(
            "Błąd",
            f"Sekwencja ma tylko {sequence_length} nukleotydów."
        )
        return

    if start >= end:
        messagebox.showerror(
            "Błąd",
            "Koniec musi być większy od Start."
        )
        return

    app_data["range_start"] = start
    app_data["range_end"] = end
    app_data["selected_range"] = (start, end)

    fragment_length = end - start + 1

    app_data["selection_label"].config(
        text=(
            f"Wybrany zakres: {start}-{end}    "
            f"Długość fragmentu: {fragment_length} bp"
        )
    )
    text = app_data["sequence_widget"]
    highlight_selected_region(text)

def show_range(right_frame):

    for widget in right_frame.winfo_children():
        widget.destroy()

    title_label = tk.Label(
        right_frame,
        text=app_data["gene"],
        font=("Arial", 16)
    )
    title_label.pack(pady=10)

    length_label = tk.Label(
        right_frame,
        text=f"Długość sekwencji: {len(app_data['sequence'])} bp",
        font=("Arial", 10)
    )
    length_label.pack()

    controls_frame = tk.Frame(right_frame)
    controls_frame.pack(fill="x", padx=10, pady=10)

    if app_data["selected_range"] is None:
        selection_text = "Nie wybrano zakresu"
    else:
        start = app_data["range_start"]
        end = app_data["range_end"]

        selection_text = (
            f"Wybrany zakres: {start}-{end}    "
            f"Długość fragmentu: {end-start+1} bp"
        )

    selection_label = tk.Label(
        right_frame,
        text=selection_text
    )
    selection_label.pack(pady=5)

    app_data["selection_label"] = selection_label

    tk.Label(
        controls_frame,
        text="Start:"
    ).grid(row=0, column=0, padx=5)

    start_entry = tk.Entry(
        controls_frame,
        width=10
    )
    start_entry.grid(row=0, column=1, padx=5)

    if app_data["range_start"] is not None:
        start_entry.insert(
            0,
            str(app_data["range_start"])
        )

    tk.Label(
        controls_frame,
        text="Koniec:"
    ).grid(row=0, column=2, padx=5)

    end_entry = tk.Entry(
        controls_frame,
        width=10
    )
    end_entry.grid(row=0, column=3, padx=5)

    if app_data["range_end"] is not None:
        end_entry.insert(
            0,
            str(app_data["range_end"])
        )

    highlight_button = tk.Button(
        controls_frame,
        text="Podświetl",
        command=highlight_range
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

    highlight_selected_region(text)

    app_data["start_entry"] = start_entry
    app_data["end_entry"] = end_entry
    app_data["sequence_widget"] = text

def generate_and_refresh():

    generate_primers()

    show_primer(app_data["right_frame"])

def show_primer(right_frame):
    app_data["right_frame"] = right_frame
    global forward_label
    global reverse_label

    for widget in right_frame.winfo_children():
        widget.destroy()

    title_label = tk.Label(
        right_frame,
        text=app_data["gene"],
        font=("Arial", 16)
    )
    title_label.pack(pady=10)

    range_text = tk.Label(
        right_frame,
        text=(
            f"Wybrany zakres: "
            f"{app_data['range_start']} - "
            f"{app_data['range_end']}"
        )
    )

    range_text.pack(pady=5)

    length_frame = tk.Frame(right_frame)
    length_frame.pack(pady=5)

    tk.Label(
        length_frame,
        text="Długość startera:"
    ).pack(side="left")

    length_entry = tk.Entry(
        length_frame,
        width=5
    )

    length_entry.insert(
        0,
        str(app_data["primer_length"])
    )

    length_entry.pack(side="left", padx=5)

    app_data["primer_length_entry"] = length_entry

    generate_button = tk.Button(
        right_frame,
        text="Generuj",
        command=generate_and_refresh
    )
    generate_button.pack(pady=10)

    if app_data["primer_generated"]:

        forward_text = (
            f"Forward:\n"
            f"{app_data['forward_primer']}\n\n"
            f"Długość: {len(app_data['forward_primer'])} bp\n"
            f"GC: {app_data['forward_gc']:.1f}%\n"
            f"Tm: {app_data['forward_tm']:.1f}°C"
        )

        if app_data["forward_warning"]:
            forward_text += (
                    "\n\n⚠ "
                    + "\n⚠ ".join(app_data["forward_warning"])
            )

        reverse_text = (
            f"Reverse:\n"
            f"{app_data['reverse_primer']}\n\n"
            f"Długość: {len(app_data['reverse_primer'])} bp\n"
            f"GC: {app_data['reverse_gc']:.1f}%\n"
            f"Tm: {app_data['reverse_tm']:.1f}°C"
        )

        if app_data["reverse_warning"]:
            reverse_text += (
                    "\n\n⚠ "
                    + "\n⚠ ".join(app_data["reverse_warning"])
            )

    else:
        forward_text = "Forward:"
        reverse_text = "Reverse:"

    current_frame = tk.Frame(right_frame)
    current_frame.pack(fill="x", pady=20)

    left_current = tk.Frame(current_frame)
    left_current.pack(side="left", expand=True)

    forward_label = tk.Label(
        left_current,
        text=forward_text,
        justify="center"
    )
    forward_label.pack()

    right_current = tk.Frame(current_frame)
    right_current.pack(side="right", expand=True)

    reverse_label = tk.Label(
        right_current,
        text=reverse_text,
        justify="center"
    )
    reverse_label.pack()

    separator = tk.Frame(
        right_frame,
        height=2,
        bd=1,
        relief="sunken"
    )
    separator.pack(fill="x", pady=20)

    proposal_title = tk.Label(
        right_frame,
        text="Proponowane startery:",
        font=("Arial", 18, "bold")
    )

    proposal_title.pack(pady=10)

    proposal_frame = tk.Frame(right_frame)
    proposal_frame.pack(fill="x", pady=10)

    left_panel = tk.Frame(proposal_frame)
    left_panel.pack(side="left", expand=True)

    tk.Label(
        left_panel,
        text="Forward",
        font=("Arial", 16)
    ).pack()

    if app_data["candidate_forward"]:

        candidate_forward_text = (
            f"{app_data['candidate_forward']}\n\n"
            f"Długość: {len(app_data['candidate_forward'])} bp\n"
            f"GC: {app_data['candidate_forward_gc']:.1f}%\n"
            f"Tm: {app_data['candidate_forward_tm']:.1f}°C"
        )

        if app_data["candidate_forward_warning"]:
            candidate_forward_text += (
                    "\n\n⚠ "
                    + "\n⚠ ".join(
                app_data["candidate_forward_warning"]
            )
            )

    else:

        candidate_forward_text = "Brak propozycji"

    candidate_forward = tk.Label(
        left_panel,
        text=candidate_forward_text,
        justify="center"
    )

    candidate_forward.pack(pady=10)

    right_panel = tk.Frame(proposal_frame)
    right_panel.pack(side="right", expand=True)

    tk.Label(
        right_panel,
        text="Reverse",
        font=("Arial", 16)
    ).pack()

    if app_data["candidate_reverse"]:

        candidate_reverse_text = (
            f"{app_data['candidate_reverse']}\n\n"
            f"Długość: {len(app_data['candidate_reverse'])} bp\n"
            f"GC: {app_data['candidate_reverse_gc']:.1f}%\n"
            f"Tm: {app_data['candidate_reverse_tm']:.1f}°C"
        )

        if app_data["candidate_reverse_warning"]:
            candidate_reverse_text += (
                    "\n\n⚠ "
                    + "\n⚠ ".join(
                app_data["candidate_reverse_warning"]
            )
            )

    else:

        candidate_reverse_text = "Brak propozycji"

    candidate_reverse = tk.Label(
        right_panel,
        text=candidate_reverse_text,
        justify="center"
    )

    candidate_reverse.pack(pady=10)

    candidate_range = tk.Label(
        right_frame,
        text=(
            "Nowy zakres: ---"
            if app_data["candidate_start"] is None
            else
            f"Nowy zakres: "
            f"{app_data['candidate_start']} - "
            f"{app_data['candidate_end']}"
        )
    )

    candidate_range.pack(pady=15)

    accept_button = tk.Button(
        right_frame,
        text="Zatwierdź",
        state="disabled"
    )

    accept_button.pack(pady=10)

    reset_button = tk.Button(
        right_frame,
        text="Reset",
        command=reset_primers
    )

    reset_button.pack(pady=20)

def reset_primers():

    app_data["forward_primer"] = ""
    app_data["reverse_primer"] = ""
    app_data["primer_generated"] = False

    forward_label.config(text="Forward:")
    reverse_label.config(text="Reverse:")

    show_primer(forward_label.master)
def select_gene():

    selected = app_data["listbox"].curselection()

    if not selected:
        messagebox.showwarning(
            "Uwaga",
            "Wybierz gen z listy."
        )
        return

    gene_file = app_data["listbox"].get(selected[0])
    gene_name = os.path.splitext(gene_file)[0]
    filepath = os.path.join(CUT_DIR, gene_file)

    with open(filepath, "r", encoding="utf-8") as f:
        sequence = f.read()

    open_gene_window(gene_name, sequence)



