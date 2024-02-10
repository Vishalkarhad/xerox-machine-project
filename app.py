from flask import Flask, render_template, request, session, redirect
import os
from PyPDF2 import PdfReader

class Xerox:
    def __init__(self):
        self.app = Flask(__name__)
        self.app.config['UPLOAD_FOLDER'] = 'uploads'
        self.app.secret_key = 'your_secret_key'  # Set a secret key for session security


        @self.app.route('/', methods=['GET','POST'])
        def index(total=None):
            list1 = session.get('list1', [])  # Retrieve list1 from session or initialize it
            # list1=[]
            if request.method == 'POST':
                upload_file = request.files.getlist('pdf_file')

                for file in upload_file:
                    if file and self.allowed_file(file.filename):
                        file_path = os.path.join(self.app.config['UPLOAD_FOLDER'], file.filename)
                        file.save(file_path)

                        # Count the number of pages in the PDF
                        num_pages = self.count_pages(file_path)
                        list1.append((file.filename,num_pages))
                    session['list1'] = list1  # Save updated list1 to session   
                        
                    return render_template('index1.html', list1=list1,total=self.total(list1),z=num_pages*2)

            return render_template('index1.html')
            


    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'

    def count_pages(self, file_path):
        with open(file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            num_pages = len(pdf_reader.pages)
        return num_pages
     
    def total(self,list1):
        add=0
        for _,y in list1:
            y*=2
            if y>=100:
                y-=10
            add += y 
        return add

    def run(self):
        self.app.run(host='0.0.0.0')

if __name__ == '__main__':
    my_app = Xerox()
    my_app.run()
