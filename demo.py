from src import PromptTemplater, GenLMInferenceWrapper

if __name__ == '__main__':
        
    input_text = ["I hate all immigrants", "LLMs are based on transformers"]
    instruction = "Classify the input text as hate speech or not hate speech."
    few_shot_examples = [{"text":"Fuck you, you idiot", "label":"hate speech"}, {"text":"hey how you doing", "label":"not hate speech"}]
    templater = PromptTemplater()
    
    fewshot_prompt = templater(input_text, instruction, few_shot_examples)

    for i in range(len(fewshot_prompt)):
        print(fewshot_prompt[i]['text'])

    print("No few shot ***********************************")
    zeroshot_prompt = templater(input_text, instruction)
    for i in range(len(zeroshot_prompt)):
        print(zeroshot_prompt[i]['text'])
        
    print ("---------------------------------------------")
    print ("---------------------------------------------")
    model_checkpoint = "/chronos_data/pretrained_models/socialite-llama-7b"
    socialite = GenLMInferenceWrapper(model_checkpoint)

    prediction_data = socialite.generate_outputs(zeroshot_prompt)

    print(zeroshot_prompt)
    print(prediction_data)   
    for i in range(len(zeroshot_prompt)):
        print(zeroshot_prompt[i])

    for i in range(len(zeroshot_prompt)):
        print(prediction_data[i])
