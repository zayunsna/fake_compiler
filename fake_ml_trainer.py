

import time
import random
import argparse
import math

def generate_sparkline(series):
    spark_chars = [' ', '▂', '▃', '▄', '▅', '▆', '▇', '█']
    min_val, max_val = min(series), max(series)
    data_range = max_val - min_val

    if data_range == 0:
        return ''.join([spark_chars[len(spark_chars) // 2]] * len(series))

    def get_char(val):
        index = int(((val - min_val) / data_range) * (len(spark_chars) - 1))
        return spark_chars[index]

    return ''.join(get_char(v) for v in series)

def display_summary(history):
    print("\n" + "="*60)
    print("                 TRAINING RUN SUMMARY")
    print("="*60 + "\n")
    
    labels = ["accuracy", "val_accuracy", "loss", "val_loss"]
    max_label_len = max(len(label) for label in labels)

    for label in labels:
        if history.get(label):
            sparkline = generate_sparkline(history[label])
            print(f"TRAINER LOG: {label.rjust(max_label_len)}   {sparkline}")
    
    print("\n" + "="*60 + "\n")

def simulate_training(epochs, batch_size, learning_rate, dataset_size):

    print("\n" + "="*60)
    print("            FAKE MACHINE LEARNING MODEL TRAINER")
    print("="*60 + "\n")
    print(f"Starting training...")
    print(f"  - Epochs:          {epochs}")
    print(f"  - Batch Size:      {batch_size}")
    print(f"  - Learning Rate:   {learning_rate}")
    print(f"  - Dataset Size:    {dataset_size}")
    print(f"  - Steps per Epoch: {dataset_size // batch_size}\n")
    time.sleep(2)

    initial_loss = random.uniform(1.5, 2.5)
    initial_accuracy = random.uniform(0.3, 0.5)
    loss, accuracy = initial_loss, initial_accuracy
    
    history = {'loss': [], 'accuracy': [], 'val_loss': [], 'val_accuracy': []}

    fluctuation_amplitude = (initial_loss - 0.1) / 5 
    fluctuation_frequency = 2 * math.pi / (dataset_size // batch_size) 

    total_steps = epochs * (dataset_size // batch_size)

    for epoch in range(1, epochs + 1):
        print(f"Epoch {epoch}/{epochs}")
        epoch_loss, epoch_accuracy = 0, 0
        steps = dataset_size // batch_size

        for i in range(1, steps + 1):
            time.sleep(random.uniform(0.01, 0.05))
            
            current_step = (epoch - 1) * steps + i

            base_loss_decay = (initial_loss / total_steps) * 1.5
            base_acc_increase = ((1 - initial_accuracy) / total_steps) * 1.2

            fluctuation = math.sin(current_step * fluctuation_frequency * random.uniform(0.8, 1.2)) * fluctuation_amplitude
            fluctuation_2 = math.sin(current_step * fluctuation_frequency * random.uniform(0.7, 1.1)) * fluctuation_amplitude

            loss -= (base_loss_decay - fluctuation) * random.uniform(0.1, 0.3)
            accuracy += (base_acc_increase + fluctuation_2/2) * random.uniform(0.1, 0.3) 

            loss, accuracy = max(0.01, loss), min(0.99, accuracy)

            epoch_loss += loss
            epoch_accuracy += accuracy

            progress = int((i / steps) * 30)
            progress_bar = f"[{'=' * progress}{' ' * (30 - progress)}]"
            print(f"  {i}/{steps} {progress_bar} - loss: {loss:.4f} - accuracy: {accuracy:.4f}", end='\r')

        avg_loss = epoch_loss / steps
        avg_accuracy = epoch_accuracy / steps
        val_loss = avg_loss * random.uniform(0.95, 1.1)
        val_accuracy = avg_accuracy * random.uniform(0.95, 1.05)

        history['loss'].append(avg_loss)
        history['accuracy'].append(avg_accuracy)
        history['val_loss'].append(val_loss)
        history['val_accuracy'].append(val_accuracy)

        time.sleep(1)

    print(f"{'='*60}\nTRAINING COMPLETE\nFinal Model Performance:\n  - Final Loss:     {loss:.4f}\n  - Final Accuracy: {accuracy:.4f}")
    print("Saving model to 'final_model.h5'...")
    time.sleep(1.5)
    print(f"Model saved.")

    display_summary(history)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Simulate a machine learning model training process.')
    parser.add_argument('--epochs', type=int, default=25, help='Number of epochs to simulate.')
    parser.add_argument('--batch_size', type=int, default=64, help='Batch size for training.')
    parser.add_argument('--lr', type=float, default=0.001, help='Learning rate.')
    parser.add_argument('--dataset_size', type=int, default=10000, help='Total size of the fake dataset.')
    
    args = parser.parse_args()

    simulate_training(
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.lr,
        dataset_size=args.dataset_size
    )
