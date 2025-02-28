import serial
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter
from sklearn.decomposition import FastICA
from matplotlib.animation import FuncAnimation

# Initialize serial port (update 'COM13' or your port)
serial_port = "COM8"  # Replace with the correct port for your system
baud_rate = 9600       # Match the baud rate in your Arduino code
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# Bandpass filter for specific frequency bands
def butter_bandpass(lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype="band")
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=4):
    b, a = butter_bandpass(lowcut, highcut, fs, order)
    return lfilter(b, a, data)

# Parameters for alpha, beta, and delta waves
sampling_rate = 100  # Sampling rate in Hz
alpha_range = (8, 13)  # Hz
beta_range = (13, 30)  # Hz
delta_range = (0.5, 4)  # Hz

# Initialize data buffers
raw_data = []
alpha_data = []
beta_data = []
delta_data = []
ica_cleaned_data = []
alpha_percentages = []
beta_percentages = []
window_size = 500  # Number of points in the rolling window

# Create 2 different figure windows for plots
fig_signal = plt.figure("Alpha, Beta, and Delta Waves (After ICA)")
fig_percentage = plt.figure("Real-Time Alpha/Beta Percentages")

# Set up the plot for signals
ax_signal = fig_signal.add_subplot(111)
ax_signal.set_title("Alpha, Beta, and Delta Waves (After ICA)")
ax_signal.set_xlabel("Time (s)")
ax_signal.set_ylabel("Voltage (V)")
lines_raw, = ax_signal.plot([], [], label="Raw Signal", lw=1, color="blue")
lines_alpha, = ax_signal.plot([], [], label="Alpha (8-13 Hz)", lw=1, color="orange")
lines_beta, = ax_signal.plot([], [], label="Beta (13-30 Hz)", lw=1, color="green")
lines_delta, = ax_signal.plot([], [], label="Delta (0.5-4 Hz)", lw=1, color="red")
ax_signal.set_ylim(-3, 3)  # Visualization range
ax_signal.legend()

# Set up the plot for percentages
ax_percentage = fig_percentage.add_subplot(111)
ax_percentage.set_title("Real-Time Alpha/Beta Percentages")
ax_percentage.set_xlabel("Time (s)")
ax_percentage.set_ylabel("Percentage (%)")
lines_alpha_percent, = ax_percentage.plot([], [], label="Alpha Percentage", lw=1, color="orange")
lines_beta_percent, = ax_percentage.plot([], [], label="Beta Percentage", lw=1, color="green")
ax_percentage.set_ylim(0, 100)  # Percentage range
ax_percentage.legend()

# Function to compute real-time percentages
def compute_percentages(alpha_power, beta_power, delta_power):
    total_power = alpha_power + beta_power + delta_power
    if total_power == 0:
        return 0, 0
    alpha_percent = (alpha_power / total_power) * 100
    beta_percent = (beta_power / total_power) * 100
    return alpha_percent, beta_percent



# Function to apply ICA for artifact removal
def apply_ica(data):
    if len(data) < window_size:
        return np.array(data)
    ica = FastICA(n_components=1, random_state=0)  # One component (single-channel data)
    data_reshaped = np.array(data).reshape(-1, 1)
    try:
        cleaned_data = ica.fit_transform(data_reshaped)
        return cleaned_data.flatten()
    except Exception as e:
        print(f"ICA Error: {e}")
        return np.array(data)

# Function to update plots and compute metrics
# ...existing code...

# Function to compute cognitive score
# ...existing code...

# Function to compute cognitive score using only beta waves
def compute_cognitive_score(beta_power):
    return beta_power

# Initialize data buffer for cognitive score
cognitive_scores = []

# Create a new figure window for cognitive score plot
fig_cognitive = plt.figure("Real-Time Cognitive Score")
ax_cognitive = fig_cognitive.add_subplot(111)
ax_cognitive.set_title("Real-Time Cognitive Score")
ax_cognitive.set_xlabel("Time (s)")
ax_cognitive.set_ylabel("Cognitive Score")
lines_cognitive, = ax_cognitive.plot([], [], label="Cognitive Score", lw=1, color="purple")
ax_cognitive.set_ylim(0, 100)  # Adjust the range as needed
ax_cognitive.legend()

# Update the update function to include cognitive score calculation and plotting
def update(frame):
    global raw_data, alpha_data, beta_data, delta_data, ica_cleaned_data
    global alpha_percentages, beta_percentages, cognitive_scores

    # Read data from the Arduino
    try:
        line = ser.readline().decode("utf-8").strip()
        if line:
            voltage = float(line.split(":")[-1].strip())
            raw_data.append(voltage)

            # Keep the window size fixed
            if len(raw_data) > window_size:
                raw_data = raw_data[-window_size:]

            # Apply ICA for artifact removal
            ica_cleaned_data = apply_ica(raw_data)

            # Bandpass filtering for alpha, beta, and delta waves
            alpha_filtered = bandpass_filter(ica_cleaned_data, alpha_range[0], alpha_range[1], sampling_rate)
            beta_filtered = bandpass_filter(ica_cleaned_data, beta_range[0], beta_range[1], sampling_rate)
            delta_filtered = bandpass_filter(ica_cleaned_data, delta_range[0], delta_range[1], sampling_rate)

            alpha_data = list(alpha_filtered)
            beta_data = list(beta_filtered)
            delta_data = list(delta_filtered)

            # Compute Real-Time Percentages
            alpha_power = np.mean(np.square(alpha_data))
            beta_power = np.mean(np.square(beta_data))
            delta_power = np.mean(np.square(delta_data))
            alpha_percent, beta_percent = compute_percentages(alpha_power, beta_power, delta_power)
            alpha_percentages.append(alpha_percent)
            beta_percentages.append(beta_percent)

            # Compute Cognitive Score using only beta power
            cognitive_score = compute_cognitive_score(beta_power)
            cognitive_scores.append(cognitive_score)

            # Update plot lines for raw and filtered signals
            lines_raw.set_data(range(len(raw_data)), raw_data)
            lines_alpha.set_data(range(len(alpha_data)), alpha_data)
            lines_beta.set_data(range(len(beta_data)), beta_data)
            lines_delta.set_data(range(len(delta_data)), delta_data)
            lines_alpha_percent.set_data(range(len(alpha_percentages)), alpha_percentages)
            lines_beta_percent.set_data(range(len(beta_percentages)), beta_percentages)
            lines_cognitive.set_data(range(len(cognitive_scores)), cognitive_scores)

            # Adjust axes for all plots
            ax_signal.set_xlim(0, len(raw_data))
            ax_percentage.set_xlim(0, len(alpha_percentages))
            ax_cognitive.set_xlim(0, len(cognitive_scores))

    except Exception as e:
        print(f"Error: {e}")

    return (lines_raw, lines_alpha, lines_beta, lines_delta,
            lines_alpha_percent, lines_beta_percent, lines_cognitive)

# Animate the plot for each figure
ani_signal = FuncAnimation(fig_signal, update, interval=100)
ani_percentage = FuncAnimation(fig_percentage, update, interval=100)
ani_cognitive = FuncAnimation(fig_cognitive, update, interval=100)

# Show the figures
plt.show()

# Close the serial connection
ser.close()
