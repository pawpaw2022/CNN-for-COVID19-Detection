
from fpdf import FPDF
from filestack import Client


class PdfReport():
    """
    Creates a PDF that contains data about the flatmate, such as
    their name, their due amount and the period of the bill.
    """

    def __init__(self, filename):
        self.filename = filename

    def generate(self, name, image_name, result):


        pdf = FPDF(orientation='P', unit='pt', format='A4')
        pdf.add_page()

        # Insert icon
        pdf.image(name='static/image/bot_doc.PNG', w=90, h=80)

        # Insert title
        pdf.set_font(family='Times', size=24, style='B')
        pdf.cell(w=0, h=80, txt='COVID-19 Report', align='C', ln=1)

        # Insert Period label and value
        pdf.set_font(family='Times', size=14, style='B')
        pdf.cell(w=100, h=40, txt='Name: ')
        pdf.cell(w=150, h=40, txt=name, ln=1)

        # Insert Image
        pdf.image(name=f'static/image/{image_name}', w=100, h=100)

        # Insert name and due amount of the first flatmate
        pdf.set_font(family='Times', size=12)
        pdf.cell(w=100, h=20, txt="Your Result is: ")
        pdf.cell(w=150, h=20, txt=result, ln=1)

        # Insert name and due amount of the second flatmate
        # pdf.cell(w=100, h=20, txt=flatmate2.name)
        # pdf.cell(w=150, h=20, txt=flatmate2_pay, ln=1)

        pdf.output(f"static/{self.filename}")

        # Automatically view a PDF file
        # os.chdir('files')  # change the path of searching
        # # webbrowser.open(self.filename) # if you are on Windows OS
        # path_pdf = os.path.abspath(self.filename)  # if you are on Mac OS
        # webbrowser.get('safari').open_new_tab(f'file:///{path_pdf}')


class FileSharer():
    """
    A generator that generates a URL of the file you choose to upload
    """

    def __init__(self, filepath, apikey='ArFQU9ogfQ5uoneGAZTHqz'):
        self.filepath = filepath
        self.apikey = apikey

    def share(self):
        client = Client(self.apikey)
        new_filelink = client.upload(filepath=self.filepath)
        return new_filelink.url


if __name__ == '__main__':
    # pdf = PdfReport("my_Report")
    # pdf.generate(name="Paul", image_name= "Report", result="Negative")
    url = FileSharer(f"static/my_Report")
    print(url.share())