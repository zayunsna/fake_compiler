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

def simulate_training(epochs, batch_size, learning_rate, dataset_size, chaos_factor):

    print("\n" + "="*60)
    print("            FAKE MACHINE LEARNING MODEL TRAINER")
    print("="*60 + "\n")
    print(f"Starting training...")
    print(f"  - Epochs:          {epochs}")
    print(f"  - Batch Size:      {batch_size}")
    print(f"  - Learning Rate:   {learning_rate}")
    print(f"  - Dataset Size:    {dataset_size}")
    print(f"  - Chaos Factor:    {chaos_factor}")
    print(f"  - Steps per Epoch: {dataset_size // batch_size}\n")
    time.sleep(2)

    # You can change these starting values for testing
    initial_loss = 1.5
    initial_accuracy = 0.6
    loss, accuracy = initial_loss, initial_accuracy
    
    history = {'loss': [], 'accuracy': [], 'val_loss': [], 'val_accuracy': []}

    total_steps = epochs * (dataset_size // batch_size)

    # BUG FIX: Fluctuation amplitude must be smaller than the base decay/increase rates
    fluctuation_amplitude = (initial_loss / total_steps) * ( 0.5 + chaos_factor)
    fluctuation_frequency = 2 * math.pi / (dataset_size // batch_size) 

    for epoch in range(1, epochs + 1):
        print(f"Epoch {epoch}/{epochs}")
        
        # As training progresses, randomness decays for stabilization
        decay_factor = (1.0 - (epoch / epochs))**1.5

        epoch_loss, epoch_accuracy = 0, 0
        steps = dataset_size // batch_size

        for i in range(1, steps + 1):
            time.sleep(random.uniform(0.01, 0.05))
            
            current_step = (epoch - 1) * steps + i

            base_loss_decay = (initial_loss / total_steps) * 1.5
            base_acc_increase = ((1 - initial_accuracy) / total_steps) * 1.2

            fluctuation = math.sin(current_step * fluctuation_frequency * random.uniform(0.8, 1.2)) * fluctuation_amplitude
            fluctuation_2 = math.sin(current_step * fluctuation_frequency * random.uniform(0.7, 1.1)) * fluctuation_amplitude

            # --- MODIFIED: Plateau Logic ---
            # If accuracy is high, enter plateau phase, otherwise continue normal training.
            if accuracy > 0.95:
                # Plateau phase: very small, symmetric fluctuations
                loss += random.uniform(-0.005, 0.005)
                accuracy += random.uniform(-0.005, 0.005)
            else:
                # Normal training phase (with chaos and decay)
                if random.random() < (chaos_factor * decay_factor):
                    # Unrealistic reversal
                    loss += (base_loss_decay - fluctuation) * random.uniform(0.1, 0.5)
                    accuracy -= (base_acc_increase + fluctuation_2/2) * random.uniform(0.1, 0.3)
                else:
                    # Realistic progression
                    loss -= (base_loss_decay - fluctuation) * random.uniform(0.1, 0.7)
                    accuracy += (base_acc_increase + fluctuation_2/2) * random.uniform(0.1, 0.3)

            # Clamp values to their allowed range
            loss, accuracy = max(0.01, loss), min(0.99, accuracy)

            epoch_loss += loss
            epoch_accuracy += accuracy

            progress = int((i / steps) * 30)
            progress_bar = f"[{'=' * progress}{' ' * (30 - progress)}]"
            print(f"  {i}/{steps} {progress_bar} - loss: {loss:.4f} - accuracy: {accuracy:.4f}", end='\r')

        avg_loss = epoch_loss / steps
        avg_accuracy = epoch_accuracy / steps

        # --- MODIFIED: Epoch-level Fluctuation ---
        # The magnitude of fluctuation also decays as training progresses for stabilization.
        base_fluctuation = random.uniform(-0.15, 0.15) # Centered around 0
        epoch_performance_factor = 1.0 + (base_fluctuation * decay_factor)
        avg_loss *= epoch_performance_factor
        # Ensure accuracy fluctuation is inversely proportional but also has some randomness
        avg_accuracy /= (epoch_performance_factor * random.uniform(0.98, 1.02))
        # --- End Modified ---

        val_loss = avg_loss * random.uniform(0.95, 1.1) # Keep some validation noise
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
    parser.add_argument('--chaos', type=float, default=0.1, help='Chance of random temporary reversal in training progress.')
    
    args = parser.parse_args()

    simulate_training(
        epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.lr,
        dataset_size=args.dataset_size,
        chaos_factor=args.chaos
    )
