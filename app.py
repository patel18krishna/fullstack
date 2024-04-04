from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from language_tool_python import LanguageTool
from transformers import BartForConditionalGeneration, BartTokenizer
from translate import Translator

app = Flask(__name__)
# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['mydb']  
collection = db['users']  

# Initialize LanguageTool for grammar correction
grammar_tool = LanguageTool('en-US')

# Initialize the BART tokenizer and model for text summarization
tokenizer = BartTokenizer.from_pretrained('facebook/bart-base')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-base')

# Initialize Translator for translation
translator = Translator(to_lang="hi")

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/signup_button', methods=['POST'])
def signup_button():
    # Get form data from request
    email = request.form['email']
    password = request.form['password']
    
    # Insert data into MongoDB collection
    collection.insert_one({'email': email, 'password': password})
    
    return render_template('home.html')

@app.route('/process_grammer', methods=['POST'])
def process_grammer():
    data = request.json
    input_text = data['inputData']
    corrected_text = correct_grammar(input_text)
    save_output_to_file(corrected_text, 'grammar_output.txt')
    return jsonify({'outputData': corrected_text})

@app.route('/process_summarize', methods=['POST'])
def process_summarize():
    data = request.json
    input_text = data['inputData']
    summary = summarize_text(input_text)
    save_output_to_file(summary, 'summarize_output.txt')
    return jsonify({'outputData': summary})

@app.route('/process_translation', methods=['POST'])
def process_translation():
    data = request.json
    english_text = data['inputData']
    translated_text = translate_english_to_hindi(english_text)
    save_output_to_file(translated_text, 'translation_output.txt')
    return jsonify({'outputData': translated_text})

@app.route('/grammer')
def grammer():
    return render_template('grammer.html')

@app.route('/translate')
def translate():
    return render_template('translate.html')

@app.route('/summarise')
def summarise():
    return render_template('summarise.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

@app.route('/home')
def home():
    return render_template('home.html')

def correct_grammar(text):
    matches = grammar_tool.check(text)
    corrected_text = grammar_tool.correct(text)
    return corrected_text

def summarize_text(text):
    inputs = tokenizer([text], max_length=1024, return_tensors='pt', truncation=True)
    summary_ids = model.generate(inputs['input_ids'], num_beams=4, min_length=30, max_length=100)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def translate_english_to_hindi(text):
    translated_text = translator.translate(text)
    return translated_text

def save_output_to_file(output_data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(output_data)

if __name__ == '__main__':
    app.run(debug=True)