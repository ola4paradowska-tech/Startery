from config import app_data
from tkinter import messagebox

def reverse_complement(sequence):

    table = str.maketrans(
        "ATGC",
        "TACG"
    )

    return sequence.translate(table)[::-1]

def gc_content(sequence):

    gc = sequence.count("G") + sequence.count("C")

    return gc / len(sequence) * 100

def calculate_tm(sequence):

    a = sequence.count("A")
    t = sequence.count("T")
    g = sequence.count("G")
    c = sequence.count("C")

    return 2 * (a + t) + 4 * (g + c)

def check_primer(gc, tm):

    warnings = []

    if gc < 40:
        warnings.append("GC < 40%")

    if gc > 60:
        warnings.append("GC > 60%")

    if tm < 55:
        warnings.append("Tm za niskie")

    if tm > 65:
        warnings.append("Tm za wysokie")

    return warnings

def score_primer(sequence):

    gc = gc_content(sequence)
    tm = calculate_tm(sequence)

    warnings = check_primer(gc, tm)

    score = 100

    score -= abs(gc - 50) * 0.5

    score -= abs(tm - 60)

    if gc < 40:
        score -= 20

    if gc > 60:
        score -= 20

    if tm < 55:
        score -= 20

    if tm > 65:
        score -= 20

    return {
        "sequence": sequence,
        "gc": gc,
        "tm": tm,
        "warnings": warnings,
        "score": score
    }

def generate_primers():

    try:
        primer_length = int(
            app_data["primer_length_entry"].get()
        )
    except ValueError:
        messagebox.showerror(
            "Błąd",
            "Podaj prawidłową długość startera."
        )
        return
    app_data["primer_length"] = primer_length
    start = app_data["range_start"]
    end = app_data["range_end"]

    if start is None or end is None:

        messagebox.showwarning(
            "Uwaga",
            "Najpierw wybierz zakres."
        )

        return

    primer_length = int(app_data["primer_length_entry"].get())

    fragment = app_data["sequence"][start-1:end]
    if len(fragment) < primer_length * 2:
        messagebox.showerror(
            "Błąd",
            "Wybrany fragment jest zbyt krótki dla tej długości starterów."
        )
        return

    # Startery z zakresu użytkownika
    forward = fragment[:primer_length]

    reverse_part = fragment[-primer_length:]
    reverse = reverse_complement(reverse_part)

    app_data["forward_primer"] = forward
    app_data["reverse_primer"] = reverse

    forward_gc = gc_content(forward)
    reverse_gc = gc_content(reverse)

    forward_tm = calculate_tm(forward)
    reverse_tm = calculate_tm(reverse)

    forward_warning = check_primer(forward_gc, forward_tm)
    reverse_warning = check_primer(reverse_gc, reverse_tm)

    tm_difference = abs(forward_tm - reverse_tm)

    if tm_difference > 2:
        forward_warning.append("Różnica Tm > 2°C")
        reverse_warning.append("Różnica Tm > 2°C")

    app_data["forward_gc"] = forward_gc
    app_data["reverse_gc"] = reverse_gc

    app_data["forward_tm"] = forward_tm
    app_data["reverse_tm"] = reverse_tm

    app_data["forward_warning"] = forward_warning
    app_data["reverse_warning"] = reverse_warning

    app_data["primer_generated"] = True


    best = find_best_primers(
        app_data["sequence"],
        start,
        end,
        primer_length
    )

    if best is None:
        messagebox.showerror(
            "Błąd",
            "Nie znaleziono odpowiedniej pary starterów."
        )
        return

    forward = best["forward"]["sequence"]
    reverse = best["reverse"]["sequence"]

    # zapis propozycji programu

    app_data["candidate_forward"] = best["forward"]["sequence"]
    app_data["candidate_reverse"] = best["reverse"]["sequence"]

    app_data["candidate_start"] = best["forward_start"]
    app_data["candidate_end"] = best["reverse_end"]

    app_data["candidate_forward_gc"] = best["forward"]["gc"]
    app_data["candidate_reverse_gc"] = best["reverse"]["gc"]

    app_data["candidate_forward_tm"] = best["forward"]["tm"]
    app_data["candidate_reverse_tm"] = best["reverse"]["tm"]

    app_data["candidate_forward_warning"] = best["forward"]["warnings"].copy()
    app_data["candidate_reverse_warning"] = best["reverse"]["warnings"].copy()

    tm_difference = abs(
        best["forward"]["tm"]
        - best["reverse"]["tm"]
    )

    if tm_difference > 2:
        app_data["candidate_forward_warning"].append(
            "Różnica Tm > 2°C"
        )

        app_data["candidate_reverse_warning"].append(
            "Różnica Tm > 2°C"
        )

def find_best_primers(sequence, start, end, primer_length):

    margin = 20

    best_pair = None
    best_score = -999999

    # zakres wyszukiwania
    forward_min = max(0, start - margin - 1)
    forward_max = start + margin - primer_length

    reverse_min = end - margin - 1
    reverse_max = min(
        len(sequence) - primer_length,
        end + margin - primer_length
    )

    for f in range(forward_min, forward_max + 1):

        forward_seq = sequence[f:f+primer_length]
        forward = score_primer(forward_seq)

        for r in range(reverse_min, reverse_max + 1):

            reverse_part = sequence[r:r+primer_length]
            reverse_seq = reverse_complement(reverse_part)

            reverse = score_primer(reverse_seq)

            pair_score = (
                forward["score"]
                + reverse["score"]
            )

            # kara za różnicę Tm
            pair_score -= abs(
                forward["tm"] - reverse["tm"]
            ) * 10

            if pair_score > best_score:

                best_score = pair_score

                best_pair = {

                    "forward": forward,

                    "reverse": reverse,

                    "forward_start": f + 1,
                    "forward_end": f + primer_length,

                    "reverse_start": r + 1,
                    "reverse_end": r + primer_length,

                    "score": pair_score
                }

    return best_pair
