import fitz  # PyMuPDF
import io
from PIL import Image

def extract_text_pymupdf(pdf_path):
    """Extracts text from a PDF file using PyMuPDF."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def extract_images(pdf_path):
    """Extracts images from a PDF file."""
    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            images.append(image)
    return images

def ocr_page(image):
    """Performs OCR on an image using Pytesseract."""
    try:
        import pytesseract
        text = pytesseract.image_to_string(image)
        return text
    except ImportError:
        print("Pytesseract not installed. Skipping OCR.")
        return ""
    except Exception as e:
        print(f"OCR Error: {e}")
        return ""
