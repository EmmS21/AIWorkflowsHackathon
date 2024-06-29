import PyPDF2

# Constants for PDF and output text file paths
pdf_path = 'testing.pdf'
output_txt = 'output.txt'

# Open PDF file and extract text
with open(pdf_path, 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()

# Write extracted text to output text file
with open(output_txt, 'w', encoding='utf-8') as txt_file:
    txt_file.write(text)

print("PDF converted to text successfully!")
