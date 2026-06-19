import pdfplumber


class ResumeParser:

    def __init__(self, pdf_path):
        self.pdf_path = pdf_path


    def extract_text(self):

        text = ""

        try:

            with pdfplumber.open(self.pdf_path) as pdf:

                for page in pdf.pages:

                    page_text = page.extract_text()

                    if page_text:

                        text += page_text + "\n"

        except Exception as e:

            print("PDF Error:", e)

        return text