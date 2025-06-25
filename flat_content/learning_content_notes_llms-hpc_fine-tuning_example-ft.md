## Supervised Full Fine-Tuning

The data for supervised learning includes labels, e.g., a text review and sentiment label (positive or negative).

An LLM is generally pre-trained for the task of masked language modeling.
Through fine-tuning, we can change the task to text classification.
  
This means that the LLM head (the last layers) will change to text classification layers.
There is a transformers function that will do this for us.

