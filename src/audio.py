"""Audio utilities."""
import numpy as np
import sounddevice as sd
import soundfile as sf
from loguru import logger

from constants import OUTPUT_FILE_NAME, LOOPBACK_DEVICE, SAMPLE_RATE

sd.default.samplerate = SAMPLE_RATE
sd.default.channels = 2
sd.default.device = LOOPBACK_DEVICE
class AudioRecorder:
    def __init__(self, audio_q):
        self.stream = None
        self.audio_q = audio_q
        self.recording = False

        try:
            sd.query_devices(device=LOOPBACK_DEVICE)
        except:
            devices = sd.query_devices()
            logger.error("This app requires a {device} virtual audio device to be properly installed.".format(device=LOOPBACK_DEVICE))
            logger.error("Device not found. Are any of these correct? {devices}".format(devices=devices))

    def audio_callback(self, indata, frames, time, status):
        if self.recording:
            self.audio_q.put(indata.copy())
        else:
            self.audio_q.put(None)

    def create_audio_stream(self):
        if self.stream is not None:
            self.stream.close()
        self.stream = sd.InputStream(callback=self.audio_callback)
        self.stream.start()

    def start(self):
        self.recording = True

        self.create_audio_stream()

    def stop(self):
        self.recording = False

        if self.stream is not None:
            self.stream.close()

        data = []

        while not self.audio_q.empty():
            data.append(self.audio_q.get())

        nparray = np.array(data, dtype=np.float32)
        
        save_audio_file(audio_data=nparray.reshape(-1, 2))

def save_audio_file(audio_data: np.ndarray, output_file_name: str = OUTPUT_FILE_NAME) -> None:
    """
    Saves an audio data array to a file.

    Args:
        audio_data (np.ndarray): The audio data to be saved.
        output_file_name (str): The name of the output file. Defaults to the value of OUTPUT_FILE_NAME.

    Returns:
        None

    Example:
        ```python
        audio_data = np.array([0.1, 0.2, 0.3])
        save_audio_file(audio_data, "output.wav")
        ```
    """
    logger.debug(f"Saving audio file to {output_file_name}...")
    sf.write(file=output_file_name, data=audio_data, samplerate=SAMPLE_RATE)
