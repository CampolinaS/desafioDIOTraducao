import os
import requests
from docs import Document

subscription_key = os.getenv('SUB_KEY')
endpoint = "https://api.cognitive.microsofttranslator.com"
location = "eastus2"
target_language = "pt-br"

def translator_text(text, target_language):
    path = "/translate"
    constructed_url = endpoint + path
    headers = {
        'Ocp-Apim-Subscription-Key' : subscription_key,
        'Ocp-Apim-Subscription-Region' : location,
        'Content-type' : 'application/json',
        'X-ClienteTraceId' : str(os.urandom(16))
    }
    
    body = [{
        'text' : text
    }]
    params = {
        'api-version': '3.0',
        'from' : 'en',
        'to' : target_language,
    }
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response= request.json()
    return response[0]['translations'][0]["text"]

translator_text("I know you're somewhere out thjere, somewhere far away", target_language)

def translate_document(path):
    document = Document(path)
    full_text = []
    for paragraph in document.paragraph:
        translated_text = translator_text(paragraph.text ,target_language)
        full_text.append(translated_text)
    
    translated_doc = Document()
    for line in full_text:
        translated_doc.add_paragraph(line)
    path_translated = path.replace(".docx", f"_language{target_language}.docx")
    translated_doc.save(path_translated)
    return path_translated
    
        
input_file = '/content/MUSICA.docx'
translate_document(input_file)
