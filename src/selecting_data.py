import pandas as pd
import ollama
from tqdm import tqdm


def generate_messages(data):
    base_prompt = (
        'Considere a frase a seguir, responda apenas com "sim" ou "não". '
        '"sim" se a frase remete a bebida Cachaça diretamente ou indiretamente e '
        '"não" se a frase não tem nenhuma relação com a bebida Cachaça:\n\n{sentence}'
    )
    return [
        {'role': 'user', 'content': base_prompt.format(sentence=sentence)}
        for sentence in data.text
    ]


def classify_messages(messages):
    is_about_cachaca = []
    for message in tqdm(messages):
        try:
            response = ollama.chat(model='llama3', messages=[message])
            response_normalized = response['message']['content'].lower().strip()
            is_about_cachaca.append(
                True if 'sim' in response_normalized else False
            )
        except Exception as e:
            print(f'Error: {e}')
            is_about_cachaca.append(None)
    return is_about_cachaca


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
    data['is_about_cachaca'] = classify_messages(messages)
    save_data(data, output_path)


if __name__ == '__main__':
    process_data()
