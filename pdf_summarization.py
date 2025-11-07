import pdfplumber
import pytesseract
from parse_config import get_tesseract_path, get_use_tesseract

use_tesseract = get_use_tesseract()
if use_tesseract:
    pytesseract.pytesseract.tesseract_cmd = get_tesseract_path()

def read_pdf_plumber(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def pdf_to_images(pdf_path):
    images = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            images.append(page.to_image(width=2480).original)
    return images

# OCR from images appears to give better results than just extracting the text from the PDF due to layout issues
def read_pdf_tesseract(pdf_path):
    images = pdf_to_images(pdf_path)
    text = ""
    for image in images:
        text += pytesseract.image_to_string(image)
    return text

def get_pdf_text(pdf_path):
    if use_tesseract:
        return read_pdf_tesseract(pdf_path)
    else:
        return read_pdf_plumber(pdf_path)