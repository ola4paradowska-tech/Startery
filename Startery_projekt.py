from gui import *
from config import *

root = tk.Tk()
root.title("Wczytaj gen")
root.geometry("400x500")

app_data["root"] = root

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

app_data["listbox"] = listbox

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