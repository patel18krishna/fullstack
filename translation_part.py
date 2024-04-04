from flask import Flask, render_template, request, jsonify
from translate import Translator

app = Flask(__name__)

def translate_english_to_hindi(text):
    translator = Translator(to_lang="hi")
    translated_text = translator.translate(text)
    return translated_text

@app.route('/')
def index():
    return render_template('translate.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    data = request.json
    english_text = data['inputData']
    
    # Translate English text to Hindi
    translated_text = translate_english_to_hindi(english_text)
    
    # Save output to file
    save_output_to_file(translated_text)
    
    return jsonify({'outputData': translated_text})

def save_output_to_file(output_data):
    with open('output.txt', 'w', encoding = 'utf-8') as f:
        f.write(output_data)

if __name__ == '__main__':
    app.run(debug=True)

