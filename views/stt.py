from SpeechRecognition.bin.inference import Synthesizer_Kospeech

#sys.path.append('C:/Users/User/inference_/Final_project/SpeechRecognition/bin')
#sys.path.append('C:/Users/User/inference_/Final_project/SpeechRecognition/wavelet_denoiser/src')

# μμ±μΈμ
def stt(s):
    kospeechModel = Synthesizer_Kospeech(s)
    text = kospeechModel.sinfer()
    return text

