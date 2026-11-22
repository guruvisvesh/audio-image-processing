import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import sounddevice as sd

# Function to change the speed of an audio signal
def adjust_audio_speed(audio_data, speed_factor):
    # Calculate the new length of the audio data
    new_length = int(len(audio_data) / speed_factor)
    # Create an array of new indices
    new_indices = np.linspace(0, len(audio_data) - 1, new_length)
    # Interpolate the audio data to the new length
    adjusted_audio = np.interp(new_indices, np.arange(len(audio_data)), audio_data)
    return adjusted_audio

# Function to load an audio file
def load_audio(file_path):
    audio_data, sample_rate = sf.read(file_path)
    if audio_data.ndim > 1:
        audio_data = audio_data.mean(axis=1)  # Convert to mono if stereo
    return audio_data, sample_rate

# Function to check linearity property
def check_linearity(y1, y2, speed_factor, alpha=0.5, beta=0.5):
    max_length = max(len(y1), len(y2))
    y1 = np.pad(y1, (0, max_length - len(y1)), mode='constant')
    y2 = np.pad(y2, (0, max_length - len(y2)), mode='constant')

    output1 = adjust_audio_speed(y1, speed_factor)
    output2 = adjust_audio_speed(y2, speed_factor)

    combined_input = alpha * y1 + beta * y2
    output_combined = adjust_audio_speed(combined_input, speed_factor)

    return np.allclose(alpha * output1 + beta * output2, output_combined)

# Function to check time invariance property
def check_time_invariance(y, speed_factor, shift=100):
    y_padded = np.pad(y, (shift, 0), mode='constant')
    y_shifted = np.roll(y_padded, shift)

    output_original = adjust_audio_speed(y_padded, speed_factor)
    output_shifted = adjust_audio_speed(y_shifted, speed_factor)

    return np.allclose(np.roll(output_original, shift), output_shifted)

# Function to plot the time-domain waveform
def plot_waveform(audio_signal, sample_rate, title, subplot_index):
    time_axis = np.linspace(0, len(audio_signal) / sample_rate, num=len(audio_signal))
    plt.subplot(5, 1, subplot_index)
    plt.plot(time_axis, audio_signal, alpha=0.7)
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.grid()

# Function to plot the frequency spectrum (Magnitude & Phase)
def plot_spectrum(audio_signal, sample_rate, title, subplot_index):
    N = len(audio_signal)
    freqs = np.fft.fftfreq(N, 1 / sample_rate)
    fft_values = np.fft.fft(audio_signal)
    
    plt.subplot(3, 2, subplot_index)
    plt.plot(freqs[:N // 2000], np.abs(fft_values[:N // 2000]), color='blue')
    plt.title(title + " - Magnitude")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid()
    
    plt.subplot(3, 2, subplot_index + 1)
    plt.plot(freqs[:N // 2000], np.angle(fft_values[:N // 2000]), color='red')
    plt.title(title + " - Phase")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Phase (radians)")
    plt.grid()

# Load original vocal and background music files
audio_vocal, sr_vocal = load_audio(r"vocal.wav")
audio_bgm, sr_bgm = load_audio(r"background.wav")
print(f"Original Sample Rates - Vocal: {sr_vocal} Hz, Background Music: {sr_bgm} Hz")

# Play original audio files
print("Playing original vocal audio.")
sd.play(audio_vocal, samplerate=sr_vocal)
sd.wait()

print("Playing original background music.")
sd.play(audio_bgm, samplerate=sr_bgm)
sd.wait()

# Speed factors for vocal and background music
vocal_speed_factor = 0.8
bgm_speed_factor = 1.3

# Adjust speed of audio files
audio_vocal_scaled = adjust_audio_speed(audio_vocal, vocal_speed_factor)
audio_bgm_scaled = adjust_audio_speed(audio_bgm, bgm_speed_factor)

# Display new sample rates
sr_vocal_scaled = int(sr_vocal * vocal_speed_factor)
sr_bgm_scaled = int(sr_bgm * bgm_speed_factor)
print(f"Sample Rates after Scaling - Vocal: {sr_vocal_scaled} Hz, Background Music: {sr_bgm_scaled} Hz")

sf.write("ts_vocal.wav", audio_vocal_scaled, sr_vocal_scaled)
print("Saved Time Scaled vocal.")

sf.write("ts_background.wav", audio_bgm_scaled, sr_bgm_scaled)
print("Saved Time Scaled Background audio.")

# Play time-scaled audio
print("Playing time-scaled vocal audio.")
sd.play(audio_vocal_scaled, samplerate=sr_vocal_scaled)
sd.wait()

print("Playing time-scaled background music.")
sd.play(audio_bgm_scaled, samplerate=sr_bgm_scaled)
sd.wait()

max_length = max(len(audio_vocal), len(audio_bgm))
audio_vocal = np.pad(audio_vocal, (0, max_length - len(audio_vocal)), mode='constant')
audio_bgm = np.pad(audio_bgm, (0, max_length - len(audio_bgm)), mode='constant')

# Print the sample rate of the mixed signal
print(f"Sample Rate of Mixed Audio: {sr_vocal_scaled} Hz")

# Mix the audio signals
mix_ratio = 0.7
audio_mixed = audio_vocal + mix_ratio * audio_bgm
audio_mixed = audio_mixed / np.max(np.abs(audio_mixed))  # Normalize the mixed audio

# Save and play the mixed audio
print("Playing mixed audio.")
sf.write("mixed_audio.wav", audio_mixed, sr_vocal)
print("Saved mixed audio.")
sd.play(audio_mixed, samplerate=sr_vocal)
sd.wait()

# Test system properties
time_invariance_result = check_time_invariance(audio_vocal, vocal_speed_factor)
linearity_result = check_linearity(audio_vocal, audio_bgm, vocal_speed_factor)

# Print test results
print(f"Time variance Test: {time_invariance_result}")
print(f"Linearity Test: {linearity_result}")

# Plot time-domain waveforms
plt.figure(figsize=(14, 10))
plot_waveform(audio_vocal, sr_vocal, "Original Vocal", 1)
plot_waveform(audio_bgm, sr_bgm, "Original Background Music", 2)
plot_waveform(audio_vocal_scaled, sr_vocal_scaled, "Time-Scaled Vocal", 3)
plot_waveform(audio_bgm_scaled, sr_bgm_scaled, "Time-Scaled Background Music", 4)
plot_waveform(audio_mixed, sr_vocal, "Mixed Audio", 5) 
plt.tight_layout()
plt.show()

# Plot frequency-domain spectra (Magnitude & Phase)
plt.figure(figsize=(14, 12))
plot_spectrum(audio_vocal, sr_vocal, "Original Vocal Spectrum", 1)
plot_spectrum(audio_bgm, sr_bgm, "Background Music Spectrum", 3)
plot_spectrum(audio_mixed, sr_vocal, "Mixed Audio Spectrum", 5)
plt.tight_layout()
plt.show()
