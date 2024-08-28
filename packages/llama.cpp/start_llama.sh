# #!/bin/bash
# if [ ! -f /models/7B/ggml-model-q4_0.gguf ]; then
#   echo 'Downloading and converting models...'
#   /usr/local/bin/llama --all-in-one /models/ 7B
# fi
# echo 'Running the model...'
# /usr/local/bin/llama --run -m /models/7B/ggml-model-q4_0.gguf -p 'Building a website can be done in 10 simple steps:' -n 512


# #!/bin/bash
# set -x  # Enable debugging
# if [ ! -f /models/7B/ggml-model-q4_0.gguf ]; then
#   echo 'Downloading and converting models...'
#   /usr/local/bin/llama --all-in-one /models/ 7B
# fi
# echo 'Running the model...'
# /usr/local/bin/llama --run -m /models/7B/ggml-model-q4_0.gguf -p 'Building a website can be done in 10 simple steps:' -n 512


#!/bin/bash
if [ ! -f /models/7B/ggml-model-q4_0.gguf ]; then
  echo 'Downloading and converting models...'
  /usr/local/bin/llama --all-in-one /models/ 7B
fi
echo 'Running the model...'
/usr/local/bin/llama --run -m /models/7B/ggml-model-q4_0.gguf -p 'Building a website can be done in 10 simple steps:' -n 512