from pdf2image import convert_from_path
import pytesseract
import util
import shutil
import os

from prescription_parser import PrescriptionParser
from patient_details_parser import PatientDetailsParser

_tesseract_path = shutil.which("tesseract")
if _tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = _tesseract_path

_pdftoppm_path = shutil.which("pdftoppm")
if _pdftoppm_path:
    POPPLER_PATH = os.path.dirname(_pdftoppm_path)
else:
    # leave a reasonable default; `extract` will check availability before use
    POPPLER_PATH = r"/usr/bin"


def extract(file_path, file_format):
    # step 1: extracting text from pdf file

    # runtime checks for required system binaries
    if shutil.which("pdftoppm") is None:
        raise RuntimeError(
            "Poppler 'pdftoppm' not found. Install it (Debian/Ubuntu):\n"
            "  sudo apt install -y poppler-utils\n"
            "Or make sure 'pdftoppm' is on your PATH."
        )

    if shutil.which("tesseract") is None and not getattr(pytesseract.pytesseract, "tesseract_cmd", None):
        raise RuntimeError(
            "Tesseract not found. Install it (Debian/Ubuntu):\n"
            "  sudo apt update && sudo apt install -y tesseract-ocr\n"
            "Or make sure 'tesseract' is on your PATH."
        )

    # convert pdf file to image
    pages = convert_from_path(file_path, poppler_path=POPPLER_PATH)
    document_text = ''
    for page in pages:
        processed_img = util.preprocess_image(page)
        text = pytesseract.image_to_string(processed_img, lang='eng')
        document_text += '\n' + text

    # step 2: extract fields from text

    if file_format == 'prescription':
        # extract data from prescription
        extracted_data = PrescriptionParser(document_text).parse()
    elif file_format == 'patient_details':
        # extract data from patienet_details
        extracted_data = PatientDetailsParser(document_text).parse()
    else:
        raise Exception(f"Invalid Document Format: {file_format}")

    return extracted_data


if __name__ == '__main__':
    data = extract('/home/mehfooj/Desktop/Medical-ocr/medical-data-extraction/src/resources/pre_1 (1).pdf', 'prescription')
    print(data)
