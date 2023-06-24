import fitz
import pandas as pd
from PyPDF2 import PdfReader

def extract_highlights_and_annotations(pdf_path):
    pdf = PdfReader(pdf_path)
    total_pages = len(pdf.pages)
    doc = fitz.open(pdf_path)

    highlights = []
    annotations = []

    for page_number in range(total_pages):
        page = doc.load_page(page_number)
        annotations_page = page.annots()

        for annotation in annotations_page:
            if annotation.type[0] == 8:  # Check if it is a highlight annotation
                rect = annotation.rect
                highlight = fitz.Rect(rect)
                words = page.get_text("words", clip=highlight)

                if words:
                    highlight_text = ' '.join(word[4] for word in words)
                    annotation_text = annotation.info.get('content', '')

                    if highlight_text:
                        highlights.append(highlight_text)
                        annotations.append(annotation_text)

        print(f"Processed page {page_number + 1}/{total_pages}")

    return highlights, annotations

def save_to_csv(highlights, annotations, output_path):
    data = {'Highlight': highlights, 'Annotation': annotations}
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')

pdf_path = 'C:\\Users\\Runze\\Desktop\\The economist\\TheEconomist.2023.01.07.pdf'
output_path = 'C:\\Users\\Runze\\Desktop\\The economist\\output1.csv'

highlights, annotations = extract_highlights_and_annotations(pdf_path)
save_to_csv(highlights, annotations, output_path)
