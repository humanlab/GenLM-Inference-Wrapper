from transformers import AutoModelForCausalLM, AutoTokenizer
from typing import List, Dict
import torch

from .constants import BATCH_SIZE, MAX_SEQ_LEN


class GenLMInferenceWrapper:
    def __init__(self, model_checkpoint: str, max_seq_len: int=MAX_SEQ_LEN):
        """
        Initialize the GenLMInferenceWrapper with the given model.

        Args:
        model_checkpoint (str): Path to the model checkpoint.
        max_seq_len (int): Maximum sequence length for the model.
        """
        print ("Loading the model...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
        if self.tokenizer.pad_token is None: self.tokenizer.pad_token = self.tokenizer.unk_token
        self.model = AutoModelForCausalLM.from_pretrained(model_checkpoint)
        
        if torch.cuda.is_available():
            self.device = torch.device('cuda')
            self.model = self.model.to(self.device).eval()
            print ("Model loaded to GPU.")
        else:
            self.device = torch.device('cpu')
            print ("No GPU available, using the CPU instead.")
            
        self.max_seq_len = max_seq_len
                

    def _tokenize(self, text_instance: str) -> torch.Tensor:
        """
        Tokenize the input text instance.

        Args:
        text_instance (str): The text to be tokenized.

        Returns:
        torch.Tensor: Tokenized version of the input text.
        """
        tokenized_input = self.tokenizer(text_instance, padding=True, max_length=self.max_seq_len, truncation=True, return_tensors="pt")
        return tokenized_input

    
    def _postprocess(self, tokenized_input: torch.Tensor, generated_output: torch.Tensor) -> torch.Tensor:
        """
        Postprocess the generated output to remove the input tokens and return only the generated text.

        Args:
        tokenized_input (torch.Tensor): The tokenized version of the input text.
        generated_output (torch.Tensor): The raw output from the model including both input and generated text.

        Returns:
        str: The postprocessed output containing only the generated text.
        """        
        tokenized_output = generated_output[len(tokenized_input):]
        return self.tokenizer.decode(tokenized_output, skip_special_tokens=True)


    def generate_outputs(self, input_data: List[str], max_tokens: int = 10) -> List[Dict[str, str]]:
        """
        Generate outputs based on the input data.

        Args:
        input_data (list): A list of input instances
        max_tokens (int): The maximum number of new tokens to generate.

        Returns:
        list: A list of dictionaries with 'text' and 'generated_text' as keys.
        """
        prediction_data = []
        for i in range(0, len(input_data), BATCH_SIZE):
            input_text = [input_data[j]['text'] for j in range(i, i+BATCH_SIZE)]
            tokenized_input = self._tokenize(input_text)
            outputs = self.model.generate(input_ids=tokenized_input["input_ids"].to(self.device), attention_mask=tokenized_input["attention_mask"].to(self.device), \
                                        do_sample=False, max_new_tokens = max_tokens)
            for j in range(BATCH_SIZE):
                decoded_output = self._postprocess(tokenized_input["input_ids"][j], outputs[j])
                data_dict = dict(text=input_text[j], generated_text=decoded_output)
                prediction_data.append(data_dict)
        return prediction_data
