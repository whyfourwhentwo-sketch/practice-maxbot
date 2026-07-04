import numpy as np
import pandas as pd
from openpyxl import load_workbook
from sentence_transformers import SentenceTransformer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')


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
    
    X_train, X_test, y_train, y_test = train_test_split(embeddings, labels, test_size=0.2, random_state=42)
    clf = LogisticRegression(class_weight='balanced', max_iter=1000)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))
    
    
    text = ""
    while text != "exit":
        text = input("Сообщение: ")
        embedding = model.encode([text])
        prediction = clf.predict(embedding)
        print ("Полезное" if prediction == 1 else "Бесполезное")
        

if __name__ == "__main__":
    main()