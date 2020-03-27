try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

def convert(filename):
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

    text = pytesseract.image_to_string(Image.open(filename))
    return text
