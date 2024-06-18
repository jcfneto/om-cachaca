import pandas as pd
import ollama
from tqdm import tqdm


def generate_messages(data):
    base_prompt = """
    Se a sentença a seguir for apenas um nome próprio, só nome próprio com emoji,
    só emoji, só uma palavra, só um número, só um caractere, só uma palavra,
    só arrobas de perfis ou só hashtags, responda true, caso contrário, responda false.

    Sentença: {sentence}

    A resposta deverá conter apenas uma palavra: true ou false.
    """
    return [
        {'role': 'user', 'content': base_prompt.format(sentence=sentence)}
        for sentence in data.text
    ]


def classify_messages(messages):
    to_remove = []
    for message in tqdm(messages):
        try:
            response = ollama.chat(model='llama3', messages=[message])
            to_remove.append(response['message']['content'].lower().strip())
        except Exception as e:
            print(f'Error: {e}')
            to_remove.append(None)
    return to_remove


def save_data(data, path):
    data.to_csv(path, index=False)


def process_data():
    input_path = input('Insira o caminho do arquivo CSV: ')
    if_output_is_same_as_input = input('O arquivo de saída será o mesmo do arquivo de entrada? (s/n): ')
    if if_output_is_same_as_input == 's':
        output_path = input_path
    else:
        output_path = input('Insira o caminho do arquivo de saída CSV: ')
    data = pd.read_csv(input_path)
    messages = generate_messages(data)
    data['to_remove'] = classify_messages(messages)
    save_data(data, output_path)


if __name__ == '__main__':
    process_data()
