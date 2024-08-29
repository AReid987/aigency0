# from flask import Flask, request, jsonify
# import subprocess
# import mlx.core as mx
# import mlx.nn as nn
# from transformers import AutoTokenizer, PreTrainedTokenizer

# app = Flask(__name__)

# # Initialize your model here (different for each container)
# def initialize_model():
#     if 'llama.cpp' in subprocess.check_output(['ls']).decode():
#         # llama.cpp
#         global llama_model
#         llama_model = subprocess.Popen(['./llama.cpp/main', '-m', '/models/model.gguf', '--host', '0.0.0.0', '--port', '8080'])
#     elif 'llamafile' in subprocess.check_output(['ls']).decode():
#         # Llamafile
#         global llamafile_model
#         llamafile_model = subprocess.Popen(['./llamafile', '-m', '/models/model.gguf', '--host', '0.0.0.0', '--port', '8080'])
#     else:
#         # MLX
#         global mlx_model, tokenizer
#         mlx_model = nn.TransformerDecoder.from_pretrained("/models/model")
#         tokenizer = AutoTokenizer.from_pretrained("/models/tokenizer")

# initialize_model()

# @app.route('/generate', methods=['POST'])
# def generate():
#     data = request.json
#     prompt = data['prompt']
#     
#     if 'llama.cpp' in subprocess.check_output(['ls']).decode() or 'llamafile' in subprocess.check_output(['ls']).decode():
#         # For llama.cpp and Llamafile, we'll use the HTTP API they provide
#         import requests
#         response = requests.post('http://localhost:8080/completion', json={'prompt': prompt, 'n_predict': 100})
#         return jsonify(response.json())
#     else:
#         # For MLX
#         inputs = tokenizer(prompt, return_tensors="np")
#         outputs = mlx_model.generate(inputs.input_ids, max_length=100)
#         response = tokenizer.decode(outputs[0].tolist())
#         return jsonify({'response': response})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)






from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/run', methods=['POST'])
def run_llama():
    prompt = request.json.get('prompt', '')
    model_path = "/models/7B/ggml-model-q4_0.gguf"

    result = subprocess.run(
        ["/app/llama.cpp/main", "-m", model_path, "-p", prompt],
        capture_output=True,
        text=True
    )

    return jsonify({
        'output': result.stdout,
        'error': result.stderr
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
