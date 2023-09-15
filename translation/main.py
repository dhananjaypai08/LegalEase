from PyPDF2 import PdfReader
from googletrans import Translator

# Open the PDF file
file = open("marathinew.pdf", 'rb')
reader = PdfReader(file)

# Initialize the Translator
translator = Translator()

# Loop through each page of the PDF
for page_num in range(len(reader.pages)):
    page = reader.pages[page_num]
    text = page.extract_text()

    # Split the text into paragraphs (you can adjust the splitting logic as needed)
    paragraphs = text.split('\n')  # Assuming paragraphs are separated by newlines
    # Translate and print each paragraph
    translated_texts = []
    for paragraph in paragraphs:
        if paragraph.strip():  # Skip empty paragraphs
            translated_text = translator.translate(paragraph, dest='en').text
            translated_texts.append(translated_text)

# Close the PDF file
file.close()

