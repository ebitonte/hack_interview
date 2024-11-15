# Avoca take-home take 2

### Audio requirements:

The project used some audio techniques that are unsupported on MacOS (using speaker output as an input device). This incompatibility requires a third party software to create a virtual loopback device. [BlackHole](https://github.com/ExistentialAudio/BlackHole) is a popular, free choice with a good usage tutorial in their [README](https://github.com/ExistentialAudio/BlackHole?tab=readme-ov-file#record-system-audio).

Previously this project used an audio package that assumed loopback support, and used a speaker as a microphone. Unable to do this, and with BlackHole as a middleman, I've modified audio recording to require a device specification in [constants.py](./src/constants.py).

### Usage:

Set the following constants.

```python
OPENAI_API_KEY = ""
DEEPGRAM_API_KEY = ""
```

```sh
pip install -r requirements.txt
python ./src/simple_ui.py
```
