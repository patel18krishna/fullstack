from transformers import BartForConditionalGeneration, BartTokenizer

# Initialize the BART tokenizer and model
tokenizer = BartTokenizer.from_pretrained('facebook/bart-base')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-base')

# Your text to be summarized
text = """
The trees, therefore, must be such old and primitive techniques that they thought nothing of them, deeming them so inconsequential that even savages like us would know of them and not be suspicious. At that, they probably didn't have too much time after they detected us orbiting and intending to land. And if that were true, there could be only one place where their civilization was hidden.
"""

# Tokenize the text and generate summary
inputs = tokenizer([text], max_length=1024, return_tensors='pt', truncation=True)
summary_ids = model.generate(inputs['input_ids'], num_beams=4, min_length=30, max_length=100)

# Decode the summary
summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

print(summary)
