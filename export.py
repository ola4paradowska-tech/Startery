import os
from tkinter import messagebox
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from datetime import datetime
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from config import (
    app_data,
    PDF_DIR,
    FASTA_REPORT_DIR
)


pdfmetrics.registerFont(
    TTFont(
        "CourierNew",
        "cour.ttf"
    )
)
pdfmetrics.registerFont(
    TTFont(
        "Arial",
        r"C:\Windows\Fonts\arial.ttf"
    )
)

pdfmetrics.registerFont(
    TTFont(
        "CourierNew",
        r"C:\Windows\Fonts\cour.ttf"
    )
)


def format_sequence(sequence):

    start = app_data["range_start"] - 1
    end = app_data["range_end"]

    primer_len = len(app_data["forward_primer"])

    forward_start = start
    forward_end = start + primer_len

    reverse_start = end - primer_len
    reverse_end = end

    lines = []

    for row_start in range(0, len(sequence), 50):

        row = []

        fragment = sequence[row_start:row_start + 50]

        for i, nt in enumerate(fragment):

            pos = row_start + i

            if forward_start <= pos < forward_end:

                row.append(
                    f'<font backColor="lightgreen">{nt}</font>'
                )

            elif reverse_start <= pos < reverse_end:

                row.append(
                    f'<font backColor="salmon">{nt}</font>'
                )

            elif start <= pos < end:

                row.append(
                    f'<font backColor="yellow">{nt}</font>'
                )

            else:

                row.append(nt)

            if (i + 1) % 10 == 0 and i != 49:
                row.append(" ")

        number = f"{row_start + 1:>5}".replace(" ", "&nbsp;")

        line = (
                f'<font color="gray"><b>{number}</b></font>&nbsp;&nbsp;'
                + "".join(row)
        )

        lines.append(line)

    return lines

def save_pdf():

    styles = getSampleStyleSheet()

    normal = ParagraphStyle(
        "NormalPL",
        parent=styles["Normal"],
        fontName="Arial",
        fontSize=10
    )

    heading = ParagraphStyle(
        "HeadingPL",
        parent=styles["Heading2"],
        fontName="Arial"
    )

    title = ParagraphStyle(
        "TitlePL",
        parent=styles["Title"],
        fontName="Arial"
    )

    filename = (
        f"{app_data['gene']}_"
        f"{app_data['range_start']}-{app_data['range_end']}.pdf"
    )

    filepath = os.path.join(
        PDF_DIR,
        filename
    )

    code = ParagraphStyle(
        "CodePL",
        parent=styles["Code"],
        fontName="CourierNew",
        fontSize=9,
        leading=13,
        spaceAfter=1
    )
    pdf = SimpleDocTemplate(filepath)

    story = []

    story.append(
        Paragraph(
            f"<b>Gen:</b> {app_data['gene']}",
            normal
        )
    )

    story.append(
        Paragraph(
            f"<b>Data:</b> {datetime.now().strftime('%d.%m.%Y')}",
            normal
        )
    )

    story.append(
        Paragraph(
            f"<b>Zakres:</b> {app_data['range_start']} - {app_data['range_end']}",
            normal
        )
    )

    story.append(
        Paragraph(
            f"<b>Długość amplikonu:</b> "
            f"{app_data['range_end']-app_data['range_start']+1} bp",
            normal
        )
    )
    story.append(
        Paragraph(
            f"<b>Długość starterów:</b> {len(app_data['forward_primer'])} bp",
            normal
        )
    )

    story.append(Spacer(1,20))

    story.append(
        Paragraph(
            "<b>Forward</b>",
            heading
        )
    )

    story.append(
        Paragraph(
            app_data["forward_primer"],
            code
        )
    )

    story.append(
        Paragraph(
            f"Długość: {len(app_data['forward_primer'])} bp",
            normal
        )
    )

    story.append(
        Paragraph(
            f"GC: {app_data['forward_gc']:.1f} %",
            normal
        )
    )

    story.append(
        Paragraph(
            f"Tm: {app_data['forward_tm']:.1f} °C",
            normal
        )
    )

    if app_data["forward_warning"]:
        warning = "<br/>".join(app_data["forward_warning"])
    else:
        warning = "Brak"

    story.append(
        Paragraph(
            f"<b>Ostrzeżenia:</b><br/>{warning}",
            normal
        )
    )

    story.append(Spacer(1,20))

    story.append(
        Paragraph(
            "<b>Reverse</b>",
            heading
        )
    )

    story.append(
        Paragraph(
            app_data["reverse_primer"],
            code
        )
    )

    story.append(
        Paragraph(
            f"Długość: {len(app_data['reverse_primer'])} bp",
            normal
        )
    )

    story.append(
        Paragraph(
            f"GC: {app_data['reverse_gc']:.1f} %",
            normal
        )
    )

    story.append(
        Paragraph(
            f"Tm: {app_data['reverse_tm']:.1f} °C",
            normal
        )
    )

    if app_data["reverse_warning"]:
        warning = "<br/>".join(
            app_data["reverse_warning"]
        )
    else:
        warning = "Brak"

    story.append(
        Paragraph(
            f"<b>Ostrzeżenia:</b><br/>{warning}",
            normal
        )
    )

    story.append(Spacer(1,30))

    story.append(
        Paragraph(
            "<b>Sekwencja</b>",
            heading
        )
    )

    formatted = format_sequence(
        app_data["sequence"]
    )

    story.append(Spacer(1, 10))

    for line in formatted:
        story.append(
            Paragraph(
                line,
                code
            )
        )

    pdf.build(story)

    messagebox.showinfo(
        "Zapisano",
        f"Raport PDF został zapisany.\n\n{filepath}"
    )

def save_fasta():

    gene = app_data["gene"]

    start = app_data["range_start"]
    end = app_data["range_end"]

    forward = app_data["forward_primer"]
    reverse = app_data["reverse_primer"]

    filename = (
        f"{gene}_{start}-{end}.fasta"
    )

    filepath = os.path.join(
        FASTA_REPORT_DIR,
        filename
    )

    with open(
        filepath,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            f">{gene}_forward_{start}-{end}\n"
        )

        f.write(
            forward + "\n\n"
        )

        f.write(
            f">{gene}_reverse_{start}-{end}\n"
        )

        f.write(
            reverse + "\n"
        )

    messagebox.showinfo(
        "Zapisano",
        f"Plik FASTA został zapisany.\n\n{filepath}"
    )