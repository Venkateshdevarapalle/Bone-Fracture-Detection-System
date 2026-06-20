from flask import Flask, render_template, request, send_file
import os
from predict import predict_xray

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
REPORT_FOLDER = "static/reports"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)

# Store previous uploads and their reports
previous_uploads = []  # list of dicts: {'filename':..., 'report':..., 'report_file':...}

@app.route("/", methods=["GET", "POST"])
def home():
    global previous_uploads
    uploaded_image = None
    output_report = ""
    report_file = None

    if request.method == "POST":
        # Handle file upload
        if "file" in request.files:
            file = request.files["file"]
            if file and file.filename != "":
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)
                uploaded_image = file.filename

                # Prediction
                import sys
                from io import StringIO
                import contextlib

                sys.argv = ["predict.py", file_path]
                f = StringIO()
                with contextlib.redirect_stdout(f):
                    predict_xray(file_path)
                output_report = f.getvalue()

                # Save report as text file
                safe_name = os.path.splitext(file.filename)[0] + "_report.txt"
                report_path = os.path.join(REPORT_FOLDER, safe_name)
                with open(report_path, "w", encoding="utf-8") as rfile:
                    rfile.write("Bone Fracture Detection Report\n")
                    rfile.write("==============================\n\n")
                    rfile.write(f"Uploaded file: {file.filename}\n\n")
                    rfile.write(output_report)

                report_file = safe_name

                # Save in previous uploads
                previous_uploads.append({
                    'filename': uploaded_image,
                    'report': output_report,
                    'report_file': report_file
                })

    # Handle click on previous upload
    if request.args.get("file"):
        clicked_file = request.args.get("file")
        uploaded_image = clicked_file
        for item in previous_uploads:
            if item['filename'] == clicked_file:
                output_report = item['report']
                report_file = item.get('report_file')
                break

    return render_template("index.html",
                           uploaded_image=uploaded_image,
                           previous_uploads=previous_uploads,
                           output_report=output_report,
                           report_file=report_file)

@app.route("/download/<filename>")
def download_report(filename):
    return send_file(os.path.join(REPORT_FOLDER, filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
