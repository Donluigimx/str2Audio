# str2audio
---
## What it is
A python program who encrypts strings into an audio file and decrypts the audio into a string.

For now, it only encrypts the string into a C scale audio.
---
## Dependencies

* [Timidity](http://timidity.sourceforge.net/)
* [Pyknon](https://github.com/kroger/pyknon)
* [Numpy](http://www.numpy.org/)
* [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/)

---
## How to use it
### str2Audio
```shell
$ python str2Audio.py [message] [filename]
```
###audio2Str
```shell
$ python str2Audio.py [filename.wav]
```
*if you dont choose a filename, the audio recorder starts automatically*
