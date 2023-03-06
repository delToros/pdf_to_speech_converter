from boto3 import Session
import convertapi
import tkinter as tk
from tkinter import filedialog as fd
import os


PDF_api_secret = os.getenv('pdf_apki_sec')
PDF_api_key = os.getenv('pdf_api_key')

POLLY_access_key = os.getenv('polly_ak')
POLLY_secret = os.getenv('polly_sa')



pdf_file = ''
file_name = ''
text = None

def convert():
    global pdf_file
    convertapi.api_secret = PDF_api_secret
    convertapi.convert('txt', {
        'File': pdf_file
    }, from_format='pdf').save_files('outputfiles/')


def select_file():
    filetypes = [('PDF files', '*.pdf')]
    global pdf_file, file_name
    pdf_file = fd.askopenfilename(title='open a file', initialdir='/', filetypes=filetypes)
    file_name = os.path.basename(pdf_file)[:1]
    convert()

def covert_to_audio():
    # This is text to speech
    global file_name, text
    with open(f'outputfiles/{file_name}.txt') as f:
        text = f.readlines()
        text = str(text[0])
        print(type(text))
    polly_client = Session(
                    aws_access_key_id=POLLY_access_key,
        aws_secret_access_key=POLLY_secret,
        region_name='us-west-2').client('polly')

    response = polly_client.synthesize_speech(VoiceId='Joanna',
                    OutputFormat='mp3',
                    Text = text,
                    Engine = 'neural')

    file = open('outputfiles/speech.mp3', 'wb')
    file.write(response['AudioStream'].read())
    file.close()


window = tk.Tk()
window.title('Pdf to Speech converter')
window.config(pady=50, padx=50)

add_pdf_button = tk.Button(text='Add pdf file', command=select_file)
add_pdf_button.grid(column=0, row=0)

convert_to_speech_button = tk.Button(text='Convert to speech', command=covert_to_audio)
convert_to_speech_button.grid(column=0, row=1)


window.mainloop()