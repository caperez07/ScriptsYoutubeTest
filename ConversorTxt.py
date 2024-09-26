import os
import re

def srt_to_txt(srt_content):
    """
    Converte o conteúdo de um arquivo .srt em texto puro.
    Remove os números das linhas e as marcações de tempo.
    """
    # Remove números das legendas e marcações de tempo
    txt_content = re.sub(r'\d+\n', '', srt_content)  # Remove números das legendas
    txt_content = re.sub(r'(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})', '', txt_content)  # Remove marcações de tempo
    txt_content = re.sub(r'\n{2,}', '\n', txt_content)  # Remove múltiplas quebras de linha
    return txt_content.strip()

def convert_srt_folder_to_txt(folder_path):
    """
    Converte todos os arquivos .srt da pasta fornecida em arquivos .txt.
    """
    for filename in os.listdir(folder_path):
        if filename.endswith(".srt"):
            srt_file_path = os.path.join(folder_path, filename)
            txt_file_path = os.path.join(folder_path, filename.replace(".srt", ".txt"))

            # Lê o conteúdo do arquivo .srt
            with open(srt_file_path, 'r', encoding='utf-8') as srt_file:
                srt_content = srt_file.read()

            # Converte para o formato de texto puro
            txt_content = srt_to_txt(srt_content)

            # Escreve o conteúdo no novo arquivo .txt
            with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write(txt_content)

            print(f"Convertido: {filename} -> {filename.replace('.srt', '.txt')}")

# Exemplo de uso
folder_path =r'C:\Users\carol\OneDrive\Documentos\ScriptsYoutubeTest\ScriptsBingo\ScriptsVanity'  # Substitua pelo caminho correto da pasta
convert_srt_folder_to_txt(folder_path)
