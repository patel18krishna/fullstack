from transformers import BartTokenizer, BartForConditionalGeneration
import sys

def bart_abstractive_summarization(text):
    # Load pre-trained BART model and tokenizer
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

    # Tokenize input text
    inputs = tokenizer(text, max_length=1024, return_tensors='pt', truncation=True)

    # Generate summary
    summary_ids = model.generate(inputs['input_ids'], num_beams=4, max_length=150, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def main():
    filename = sys.argv[1]  # Get input filename from command-line argument
    with open(filename, "r") as file:
        input_text = file.read()

    # Perform abstractive summarization using BART
    output_text = bart_abstractive_summarization(input_text)

    # Print output text so it can be captured by Flask
    print(output_text)

if __name__ == "__main__":
    main()
