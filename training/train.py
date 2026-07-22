import numpy as np

from training.data.safe_loader import load_data_safe
from training.model.model_train import train_classifier, save_model

def main(args):
    """CLI для обучения и сохранения моделей"""
    
    embeddings, labels = load_data_safe(args.file)
    
    
    for key, value in labels.items():
        label = np.array(value)
        classifier = train_classifier(embeddings[label != -1], label[label != -1])
        save_model(key, classifier)
        
        
    
        
