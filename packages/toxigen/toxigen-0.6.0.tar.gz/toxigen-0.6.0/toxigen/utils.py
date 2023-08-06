from toxigen.language_models import GPT3, ALICE

def generate_with_gpt3(prompt, classifier, endpoint_url, api_key, mode="neutral", num_to_generate=1, device="cpu"):
    language_model = ALICE(GPT3(endpoint_url=endpoint_url, apikey=api_key), classifier, mode, device="cpu")
    
    return [language_model(prompt) for _ in range(num_to_generate)]
