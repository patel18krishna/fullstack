from flask import Flask, render_template, request, jsonify
from language_tool_python import LanguageTool

app = Flask(__name__)

def correct_grammar(text):
    tool = LanguageTool('en-US')
    matches = tool.check(text)
    corrected_text = tool.correct(text)
    return corrected_text

@app.route('/')
def index():
    return render_template('grammer.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    data = request.json
    input_text = data['inputData']
    corrected_text = correct_grammar(input_text)
    save_output_to_file(corrected_text)
    return jsonify({'outputData': corrected_text})

def save_output_to_file(output_data):
    with open('output.txt', 'w') as f:
        f.write(output_data)

if __name__ == '__main__':
    app.run(debug=True)
