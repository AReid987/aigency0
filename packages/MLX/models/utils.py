import os

import yaml

flags = {
    "vi": "🇻🇳",
    "en": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "zh": "🇨🇳",
    "es": "🇪🇸",
    "tr": "🇹🇷",
    "ja": "🇯🇵",
    "kr": "🇰🇷",
    "in": "🇮🇳",
    "de": "🇩🇪",
    "fr": "🇫🇷",
    "it": "🇮🇹",
    "multi": "🌍",
}

recommended_usage = """
| Model Size/ RAM | 0.5B ~ 4B | 6B ~ 13B | 14B ~ 34B | 40B ~ 56B | 65B ~ 72B | 100B ~ 180B |
|:---------------:|:---------:|:--------:|:---------:|:---------:|:---------:|:-----------:|
|       8GB       |    ✅/✅    |    ✅/❌   |    ❌/❌    |    ❌/❌    |    ❌/❌    |     ❌/❌     |
|       18GB      |    ✅/✅    |    ✅/✅   |    ✅/❌    |    ❌/❌    |    ❌/❌    |     ❌/❌     |
|       36GB      |    ✅/✅    |    ✅/✅   |    ✅/❌    |    ✅/❌    |    ❌/❌    |     ❌/❌     |
|       48GB      |    ✅/✅    |    ✅/✅   |    ✅/✅    |    ✅/❌    |    ❌/❌    |     ❌/❌     |
|       64GB      |    ✅/✅    |    ✅/✅   |    ✅/✅    |    ✅/✅    |    ✅/❌    |     ❌/❌     |
|       96GB      |    ✅/✅    |    ✅/✅   |    ✅/✅    |    ✅/✅    |    ✅/❌    |     ✅/❌     |
|      192GB      |    ✅/✅    |    ✅/✅   |    ✅/✅    |    ✅/✅    |    ✅/✅    |     ✅/❌     |

Note:
✅ - Usable, ❌ - Not usable

For the corresponding model size and RAM combination:
Left value in each cell -->  usability of 4-bit quantization. Right value in each cell -->  usability of 8-bit quantization.

Example:
- Model size between 14B and 34B parameters
- Machine with 48GB of RAM
you can use 4-bit quantization (✅)
8-bit quantization is not usable (❌).
"""


def get_yaml_files(directory):
    return [
        os.path.join(directory, entry)
        for entry in os.listdir(directory)
        if entry.endswith(".yaml")
    ]


def load_yaml_config(config_path):
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config


def process_yaml(yaml_path):
    config = load_yaml_config(yaml_path)
    final_config = config["original_repo"]
    model_lang = config["default_language"] if "default_language" in config else ""
    model_quant = config["quantize"] if "quantize" in config else ""
    if model_lang != "" and model_quant != "":
        final_config += f" ({flags[model_lang]},{model_quant})"
    elif model_lang != "":
        final_config += f" ({flags[model_lang]})"
    elif model_quant != "":
        final_config += f" ({model_quant})"
    else:
        final_config = final_config

    return (
        {f'{config["original_repo"]}': config["mlx-repo"]},
        {f'{config["original_repo"]}': yaml_path},
        {f"{final_config}": config["original_repo"]},
        {f"{final_config}": config["mlx-repo"]},
    )


def model_info():
    model_list = {}
    yml_list = {}
    final_cfg_list = {}
    mlx_config_list = {}
    directory_path = os.path.dirname(os.path.abspath(__file__))
    yaml_files = get_yaml_files(f"{directory_path}/configs")
    for file in yaml_files:
        model_dict, yml_path, final_cfg, mlx_config = process_yaml(file)
        model_list |= model_dict
        yml_list |= yml_path
        final_cfg_list |= final_cfg
        mlx_config_list |= mlx_config

    return model_list, yml_list, final_cfg_list, mlx_config_list
