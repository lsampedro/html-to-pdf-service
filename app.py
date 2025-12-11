from flask import Flask, request, send_file
import subprocess
import tempfile
import os

app = Flask(__name__)

@app.post("/html-to-pdf")
def html_to_pdf():
    payload = request.get_json(silent=True) or {}
    html = payload.get("html", "")

    if not html:
        return {"error": "No HTML provided"}, 400

    # Archivo temporal HTML
    with tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False) as html_file:
        html_file.write(html)
        html_path = html_file.name

    # Archivo temporal PDF
    pdf_path = tempfile.mktemp(suffix=".pdf")

    try:
        # Llamar a wkhtmltopdf CON MÁRGENES
        subprocess.run(
            [
                "wkhtmltopdf",
                "--enable-local-file-access",
                "--margin-top", "25mm",      # <- margen superior en TODAS las páginas
                "--margin-right", "20mm",
                "--margin-bottom", "20mm",
                "--margin-left", "20mm",
                "--footer-center", "[page]",  # <- numeración de páginas (opcional)
                html_path,
                pdf_path
            ],
            check=True
        )

        return send_file(pdf_path, mimetype="application/pdf")
    finally:
        if os.path.exists(html_path):
            os.remove(html_path)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)