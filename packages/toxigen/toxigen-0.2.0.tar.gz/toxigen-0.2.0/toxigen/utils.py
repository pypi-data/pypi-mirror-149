from toxigen.language_models import GPT3, ALICE

def generate_with_gpt3(prompt, classifier, num_to_generate, endpoint_url, api_key):
    language_model = ALICE(GPT3(endpoint_url=endpoint_url, apikey=api_key), classifier)
    
    return [language_model(prompt) for _ in range(num_to_generate)]
