from PyPDF2 import PdfReader
from googletrans import Translator
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# Function to translate text to a target language
def translate_text(text, target_language):
    translator = Translator()
    return translator.translate(text, dest=target_language).text

pdf_file = "marathinew.pdf"
pdf_reader = PdfReader(open(pdf_file, "rb"))

target_language = 'en'  

output_filename = "translated_pages.pdf"

# Initialize ReportLab document
output_buffer = BytesIO()
doc = SimpleDocTemplate(output_buffer, pagesize=letter)

# Define a style for the translated text
styles = getSampleStyleSheet()
style = styles["Normal"]

translated_paragraphs = []

# Loop through each page of the PDF
for page_num in range(len(pdf_reader.pages)):
    page = pdf_reader.pages[page_num]
    text = page.extract_text()

    # Translate the entire page's text to the target language
    translated_text = translate_text(text, target_language)
    
    # Split the translated text into paragraphs
    translated_paragraphs.extend(translated_text.split('\n'))

# Create Story for ReportLab
story = []

for paragraph in translated_paragraphs:
    paragraph = Paragraph(paragraph, style)
    story.append(paragraph)

# Build the ReportLab PDF
doc.build(story)

with open(output_filename, 'wb') as output_file:
    output_file.write(output_buffer.getvalue())

print(f"Translated PDF file '{output_filename}' has been created.")
