import numpy as np

from training.data.safe_loader import load_data_safe
from training.model.model_train import train_classifier, save_model

"""CLI для обучения и сохранения моделей"""


def train_main(args):
    embeddings, labels = load_data_safe(args.file)
    print(labels.items())
    for name, label in labels.items():
        print(f"Обучаем модель {name}")
        classifier = train_classifier(embeddings, label)
        save_model(name, classifier)
        
        
