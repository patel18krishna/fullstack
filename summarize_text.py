from flask import Flask, render_template, request, jsonify
from transformers import BartForConditionalGeneration, BartTokenizer

app = Flask(__name__)

# Initialize the BART tokenizer and model
tokenizer = BartTokenizer.from_pretrained('facebook/bart-base')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-base')

@app.route('/')
def index():
    return render_template('summarise.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    data = request.json
    input_text = data['inputData']
    
    # Summarize input text
    summary = summarize_text(input_text)
    
    # Save output to file
    save_output_to_file(summary)
    
    return jsonify({'outputData': summary})

# TEST
@app.route('/account')
def account():
    return render_template('account.html')

def summarize_text(text):
    # Tokenize the text and generate summary
    inputs = tokenizer([text], max_length=1024, return_tensors='pt', truncation=True)
    summary_ids = model.generate(inputs['input_ids'], num_beams=4, min_length=30, max_length=100)

    # Decode the summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def save_output_to_file(output_data):
    with open('output.txt', 'w') as f:
        f.write(output_data)

if __name__ == '__main__':
    app.run(debug=True)
