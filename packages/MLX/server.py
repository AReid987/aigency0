from flask import Flask, request, jsonify
from packages.ml_wrapper import ModelWrapper
from transformers import AutoTokenizer, PreTrainedTokenizer

app = Flask(__name__)
model = ModelWrapper()

# Initialize your model here
"""
Loads a pre-trained Transformer decoder model from the specified path.

The Transformer decoder model is a key component of the MLX system, responsible for generating text outputs based on input prompts. This method allows you to load a pre-trained model from the specified path, which can then be used for text generation tasks.

Args:
    "/models/deepseek-coder-6.7b-instruct": The path to the pre-trained Transformer decoder model.

Returns:
    A Transformer decoder model instance that can be used for text generation.
"""
# model = nn.TransformerDecoder.from_pretrained(
#     "/models/deepseek-coder-6.7b-instruct")

tokenizer = AutoTokenizer.from_pretrained("/models/tokenizer")


@app.route('/generate', methods=['POST'])
def generate():
    """
    Generates a text response based on the provided prompt.

    This function takes a prompt as input, passes it through a pre-trained Transformer decoder model, and returns the generated text response.

    Args:
        prompt (str): The input prompt to be used for text generation.

    Returns:
        dict: A dictionary containing the generated text response.
    """
    data = request.json
    prompt = data['prompt']

    inputs = tokenizer(prompt, return_tensors="np")
    outputs = model.generate(inputs.input_ids, max_length=100)
    response = tokenizer.decode(outputs[0].tolist())

    return jsonify({'response': response})


@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    data = request.json
    messages = data['messages']
    prompt = " ".join([m['content'] for m in messages])

    inputs = tokenizer(prompt, return_tensors="np")
    outputs = model.generate(
        inputs.input_ids, max_length=data.get('max_tokens', 100))
    response = tokenizer.decode(outputs[0].tolist())

    return jsonify({
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": response
                }
            }
        ]
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
