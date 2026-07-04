import numpy as np
import pandas as pd
from openpyxl import load_workbook
from sentence_transformers import SentenceTransformer

def save_embeddings(embeddings, labels):
    np.savez('data.npz', embeddings=embeddings, labels=labels)


def create_embeddings():
    wb = load_workbook('data_ml.xlsx')
    sheet = wb.active
    phrase = []
    is_useful = []
    for row in sheet['A1:D311']:
        phrase.append(str(row[0].value))
        is_useful.append(1 if row[3].value == 'да' else 0)
        
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    embeddings = model.encode(phrase[1::], show_progress_bar=True)

    return np.array(embeddings), np.array(is_useful[1::])

def load_data():
    try:
        data = np.load('data.npz', allow_pickle=True)
        embeddings = data['embeddings']
        labels = data['labels']
        
    except FileNotFoundError:
        embeddings, labels = create_embeddings()
        save_embeddings(embeddings, labels)
        
    return embeddings, labels


def main():
    embeddings, labels = load_data()
    print(f"Embeddings shape: {embeddings.shape}")
    print(f"Labels shape: {labels.shape}")

if __name__ == "__main__":
    main()