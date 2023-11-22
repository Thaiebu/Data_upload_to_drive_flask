
import requests
from flask import Flask,render_template,request
from pdf_uploader import upload_pdf

PARENT_FOLDER_ID = "1CiQLVoG-fUML0d6KNHNuDxccuLuYBRBo"

app = Flask(__name__)
@app.route("/file_uploader", methods=['GET', 'POST'])
def facebook_downloader():
  link = request.form.get('link',False)
  name = request.form.get('name',False)
  # return render_template('fb_downloader.html')
  if link and name:
    print(link)
    print(name)
    message = upload_pdf(link,name,PARENT_FOLDER_ID)
    if message :
      return render_template('drive_uploader.html',message = message)
    else: 
      message = "Please Check the link"
      return render_template('drive_uploader.html',message = message)
  else:
    error = 'Enter both link and name'
    return render_template('drive_uploader.html',message = error)

if __name__ == "__main__":
  app.run(debug=True)