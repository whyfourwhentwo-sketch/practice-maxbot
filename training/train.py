"""CLI для обучения классификатора."""

from training.data.prepare_data import prepare_data
from training.model.model_train import train_classifier


def main() -> None:
    print("Preparing training data...")
    embeddings, labels = prepare_data()
    print(f"Training on {len(labels)} samples...")
    train_classifier(embeddings, labels)
    print("Training complete.")


if __name__ == "__main__":
    main()
