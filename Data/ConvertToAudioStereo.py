import numpy as np
from scipy.io.wavfile import write

def convert_raw_audio_to_wav(samples, sample_rate, bit_depth, output_file):
    # Normalize samples to the range of the bit depth
    max_val = 2 ** (bit_depth - 1) - 1
    normalized_samples = np.clip(samples, -max_val, max_val).astype(np.int16)
    
    # Write the samples to a WAV file
    write(output_file, sample_rate, normalized_samples)

# Example usage
file_path = "North.txt"  # Replace with the path to your text file containing raw stereo audio samples
sample_rate = 4000  # Replace with the sample rate of your audio
bit_depth = 32  # Replace with the bit depth of your audio
output_file = "output-stereo.wav"  # Replace with the desired output file path

# Read raw stereo audio samples from the file
with open(file_path, 'r') as file:
    lines = file.readlines()
    left_samples = []
    right_samples = []
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) != 3:  # Assuming each line contains timestamp, left sample, and right sample
            continue
        try:
            left_sample = int(parts[1])
            right_sample = int(parts[2])
            left_samples.append(left_sample)
            right_samples.append(right_sample)
        except ValueError:
            continue

# Convert raw stereo audio samples to WAV file
stereo_samples = np.column_stack((left_samples, right_samples))
convert_raw_audio_to_wav(stereo_samples, sample_rate, bit_depth, output_file)
