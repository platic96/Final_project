"""
Denoise a file (pass the filename as argument)
"""

def denoises():

    import os
    import argparse
    import time
    import soundfile
    from denoise import Denoiser
    from noiseProfiler import NoiseProfiler

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-i", "--input", help="the relative or absolute path of the sound file you wish to denoise", required=False, 
        default='D:/Final_project/SpeechRecognition/Record_sample/twoja.wav')
    parser.add_argument("-a", default=2, type=int,
                        help="denoiser param 'a' (default: %(default)s)")
    parser.add_argument("-b", default=1, type=int,
                        help="denoiser param 'b' (default: %(default)s)")
    parser.add_argument("-c", default=1, type=int,
                        help="denoiser param 'c' (default: %(default)s)")
    parser.add_argument("-d", default=0.1, type=float,
                        help="denoiser param 'd' (default: %(default)s)")
    parser.add_argument("-type", default=1, type=int, choices=[1, 2, 3],
                        help="filter type (default: %(default)s)")
    parser.add_argument("-akg", default=4, type=float,
                        help="grad of the Ak filter (default: %(default)s)")
    parser.add_argument("-ako", default=2, type=float,
                        help="offset of the Ak filter (default: %(default)s)")
    parser.add_argument("-aks", default="asc", choices=['asc', 'desc'],
                        help="the slope of the Ak filter - 'asc' or 'desc' (default: %(default)s)")
    parser.add_argument("-l", default=8, type=int,
                        help="wavelet packed decomposition levels (default: %(default)s)")
    parser.add_argument("-wavelet", default='db8',
                        help="the wavelet to be used (default: %(default)s)")
    parser.add_argument("-method", default="wpa", choices=['wpa', 'dwt'],
                        help="The wavelet transform method - 'wpa' or 'dwt' (default: %(default)s)")
    parser.add_argument("-t", "--time",
                        help="the period of silence present in the audio file (in seconds) eg: '0-0.5'. If none provided, the noise period will be autoimatically found ",
                        required=False)
    parser.add_argument("-v", "--verbose", help="verbose (plays the result audio)",
                        action="store_true")
    parser.add_argument("-o", "--output", required=False,
                        help="The output filename", default='D:/Final_project/SpeechRecognition/Record_sample/3.wav')

    args = parser.parse_args()

    args.input = args.input.replace("\"", "")
    args.input = args.input.replace("'", "")

    filePath = os.path.dirname(args.input)
    fileName = os.path.basename(args.input)

    print("trying to open " + args.input)
    data, sampleRate = soundfile.read(args.input)

    # if it's stereo it will have 2 columns.. so, checking for number of columns and if there is
    # more than 1, transpose & keep the first row
    if len(data.shape) > 1:
        data = data.T[0]

    print("Number of samples read: " + str(len(data)))

    denoiser = Denoiser(
        a=args.a,
        b=args.b,
        c=args.c,
        d=args.d,
        akGrad=args.akg,
        akOffset=args.ako,
        akSlope=args.aks,
        wlevels=args.l,
        method=args.method,
        waveletName=args.wavelet,
        filterType=args.type,
    )


    dataNoise = None
    if args.time != None and args.time != "":
        # removing the quotes passed
        args.time = args.time.replace("\"", "")
        args.time = args.time.replace("'", "")
        print("using defined period of noise: " + args.time)
        # keeping first 0.5s as the noise data
        timeSplitted = args.time.split("-")
        timeStart = float(timeSplitted[0])
        timeEnd = float(timeSplitted[1])
        sampleStart = int(timeStart * sampleRate)
        sampleEnd = int(timeEnd * sampleRate)
        dataNoise = data[sampleStart:sampleEnd]
        dataNoise = denoiser.padArray(dataNoise, len(data))
    else:
        noiseProfile = NoiseProfiler(data)
        dataNoise = noiseProfile.getNoiseDataPredicted()

    dataDenoised = denoiser.denoise(Xin=data, Nin=dataNoise)


    outPath = os.path.dirname(args.output)
    print(outPath)

    if(outPath and not os.path.isdir(outPath)):
        os.makedirs(outPath,exist_ok=True)

    print("will write denoised file to " + args.output)
    soundfile.write(args.output, dataDenoised, sampleRate)

    print("OK")
    if(args.verbose):
        import sounddevice
        
        sounddevice.play(dataDenoised, sampleRate)
        time.sleep(4)
