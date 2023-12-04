from typing import List, Optional, Dict

class PromptTemplater:
    def __call__(self, input_text: List[str], instruction: str, few_shot_examples: Optional[List[Dict[str, str]]] = None) -> List[Dict[str, str]]:
        """
        Format input instances into instruction instances.

        Args:
            input_text (List[str]): List of input text that will be classified by Socialite-Llama.
            instruction (str): Base instruction for the task.
            few_shot_examples (Optional[List[Dict[str, str]]]): List of few-shot examples (default is None).

        Returns:
            List[Dict[str, str]]: List of formatted instructions.
        """
        if few_shot_examples is not None:
            for example in few_shot_examples:
                assert set(example.keys()) == {"text", "label"}, "Each entry in few_shot_examples should have 'text' and 'label' as keys."

        few_shot_instruction_prompt = "\nBelow are a few examples to help you understand the task better."
        base_instruction = instruction.strip()
        if few_shot_examples is not None:
            base_instruction += few_shot_instruction_prompt
            for i in range(len(few_shot_examples)):
                base_instruction = base_instruction + "\n" + few_shot_examples[i]['text'] + " - " + few_shot_examples[i]['label']
            
            base_instruction += "\nBased on the above examples, perform the mentioned task as provided in the instruction."

        input_instruction_data = [
            {
                "text": f"""Instruction: {base_instruction}
Input: {input_text[i]}
Output:"""
            }
            for i in range(len(input_text))
        ]
        return input_instruction_data
