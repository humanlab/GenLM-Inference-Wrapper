## GenLM Inference Wrapper
### Library to run Inference using Genarative Language Models 

This repository is a wrapper around the [HuggingFace Transformers](https://www.github.com/huggingface/transformers) library. It provides a simple interface to run inference using any generative language model for any task provided as textual description to the model. 


### Installation

1. Clone the repository

```bash
git clone <>
```

2. Install the requirements

```bash
pip install -r requirements.txt
```

You can also create a conda environment and install the requirements within the requirement.

```bash
conda create -n genlm python=3.8
conda activate genlm
pip install -r requirements.txt
```

3. Run the setup install file in case you want to use the DLATK backend or if your datastore is a MySQL database.

```bash
python setup.py install
```

### Usage

You can use this library in two ways:

#### 1. Using with MySQL database

```bash
python mysql_interface -d db_name -t message_table -i 'Provide Instructions here' \
                        --output_table output_table_name \
                        --model_path '/path/to/model/or/hf_model_name' 
```

#### 2. You can use the methods inside the `src` folder to run inference within your script

```python
from src import PromptTemplator, GenLMInferenceWrapper

templater = PromptTemplater()
model = GenLMInferenceWrapper(model_checkpoint=model_path)

instruction = """Read the text thoroughly and classify the emotion of the text as one of the following: anger, fear, joy, and sadness."""
task_data = ['Words would fail to describe the feeling of being able to see the Taj Mahal for the first time. It was a surreal experience.', 
            'I don\'t know what to do. This is so frustrating that I want to break my phone to pieces.']
input_prompt = templater(input_text=task_data, instruction=instruction)
prediction_data = model.generate_outputs(input_data=input_prompt)
```

Note: You can override the implementation of the `PromptTemplator` to customize the prompts.


### Additional Information

#### Using Socialite Llama Model

Socialite Llama is an instruction tuned version of llama2-7b on a collection of 20 social scientific tasks covering 5 broad domains: Emotion/Sentiment, Offensiveness, Trustworthy, Humor, and Other Social Factors. Socialite Llama performs better than the base model, llama, on 18 / 20 seen tasks. The specific tasks and its instructions are available under `src/assets/socialite_llama_tasks.json`. These instructions can be used to run inference using the Socialite Llama model. 

```bash  
python mysql_interface -d db_name -t message_table -i emotion_4_class \
                        --output_table 'pred$socialite_emotion_4_class$message_table$message_id' \
                        --model_path '/path/to/socialite_llama/' 
```


### CITE US

If you use this library, please cite us:

```
@article{socialite_llama,
  author = {Gourab Dey, Adithya V Ganesan, Yash Kumar Lal, Manal Shah, Shreyashee Sinha, Matthew Matero, Salvatore Giorgi, Vivek Kulkarni, and H. Andrew Schwartz},
  title = {Socialite-Llama: An Instruction Tuned Language Model for Social Scientific Applications},
  year = {2023},
  publisher = {github}
}
```