import re
import mutagen
from glob import glob
from mutagen import oggopus
from mutagen.aac import AAC
from mutagen.ac3 import AC3
from mutagen.aiff import AIFF
from mutagen.asf import ASF
from mutagen.dsdiff import DSDIFF
from mutagen.dsf import DSF
from mutagen.flac import FLAC
from mutagen.monkeysaudio import MonkeysAudio
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.musepack import Musepack
from mutagen.oggflac import OggFLAC
from mutagen.oggspeex import OggSpeex
from mutagen.oggtheora import OggTheora
from mutagen.oggvorbis import OggVorbis
from mutagen.optimfrog import OptimFROG
from mutagen.smf import SMF
from mutagen.tak import TAK
from mutagen.trueaudio import TrueAudio
from mutagen.wave import WAVE
from mutagen.wavpack import WavPack


class YTtimestamp:
    def __init__(self, path, isNum):
        self.path = path + "\*"
        self.filePaths = glob(self.path)
        self.HumanSort(self.filePaths)
        self.output = open("output.txt", "w")
        self.isNum = isNum

    def HumanSort(self, l):
        def alphanum_key(s):
            """ Turn a string into a list of string and number chunks.
                "z23a" -> ["z", 23, "a"]
            """
            return [tryint(c) for c in re.split('([0-9]+)', s)]

        def tryint(s):
            try:
                return int(s)
            except ValueError:
                return s

        l.sort(key=alphanum_key)

    def ToTwoDigitString(self, num):
        sNum = str(num)
        if len(sNum) == 1:
            return "0" + sNum
        return sNum

    def TimeCalc(self, time):
        hour = int(time // 3600)
        minute = int((time - hour * 3600) // 60)
        sec = int(time - hour * 3600 - minute * 60)
        sHour = self.ToTwoDigitString(hour)
        sMinute = self.ToTwoDigitString(minute)
        sSec = self.ToTwoDigitString(sec)
        if hour == 0:
            return sMinute + ":" + sSec
        else:
            return sHour + ":" + sMinute + ":" + sSec

    def FindClass(self, filePath):
        classTree = str(type(mutagen.File(filePath)))
        classTree = classTree[8:len(classTree)-2]
        return classTree

    def MakeAudioObj(self, classTree, filePath):
        try:
            if classTree == "mutagen.mp3.MP3":
                audio = MP3(filePath)
            elif classTree == "mutagen.aac.AAC":
                audio = AAC(filePath)
            elif classTree == "mutagen.ac3.AC3":
                audio = AC3(filePath)
            elif classTree == "mutagen.aiff.AIFF":
                audio = AIFF(filePath)
            elif classTree == "mutagen.asf.ASF":
                audio = ASF(filePath)
            elif classTree == "mutagen.dsdiff.DSDIFF":
                audio = DSDIFF(filePath)
            elif classTree == "mutagen.dsf.DSF":
                audio = DSF(filePath)
            elif classTree == "mutagen.flac.FLAC":
                audio = FLAC(filePath)
            elif classTree == "mutagen.monkeysaudio.MonkeysAudio":
                audio = MonkeysAudio(filePath)
            elif classTree == "mutagen.mp4.MP4":
                audio = MP4(filePath)
            elif classTree == "mutagen.musepack.Musepack":
                audio = Musepack(filePath)
            elif classTree == "mutagen.oggflac.OggFLAC":
                audio = OggFLAC(filePath)
            elif classTree == "mutagen.oggopus.OggOpus":
                audio = oggopus.OggOpus(filePath)
            elif classTree == "mutagen.oggspeex.OggSpeex":
                audio = OggSpeex(filePath)
            elif classTree == "mutagen.oggtheora.OggTheora":
                audio = OggTheora(filePath)
            elif classTree == "mutagen.oggvorbis.OggVorbis":
                audio = OggVorbis(filePath)
            elif classTree == "mutagen.optimfrog.OptimFROG":
                audio = OptimFROG(filePath)
            elif classTree == "mutagen.smf.SMF":
                audio = SMF(filePath)
            elif classTree == "mutagen.tak.TAK":
                audio = TAK(filePath)
            elif classTree == "mutagen.trueaudio.TrueAudio":
                audio = TrueAudio(filePath)
            elif classTree == "mutagen.wave.WAVE":
                audio = WAVE(filePath)
            elif classTree == "mutagen.wavpack.WavPack":
                audio = WavPack(filePath)
            return audio
        except mutagen.MutagenError:
            return False

    def FindFilename(self, filePath):
        pathLen = len(filePath)
        dot = pathLen-1
        while filePath[dot] != ".":
            dot -= 1
        # extension = filePath[dot+1:pathLen]
        nameStart = dot-1
        while filePath[nameStart] != "\\":
            nameStart -= 1
        fileName = filePath[nameStart+1:dot]
        return fileName

    def Run(self):
        timeStamp = 0
        hh_mm_ss = "00:00"
        num = 0
        for filePath in self.filePaths:
            classTree = self.FindClass(filePath)
            if classTree != "NoneType":
                fileName = self.FindFilename(filePath)
                if self.isNum:
                    num += 1
                    sNum = self.ToTwoDigitString(num)
                    print(f"{sNum}. {fileName} - {hh_mm_ss}", file=self.output)
                else:
                    print(f"{fileName} - {hh_mm_ss}", file=self.output)
                audio = self.MakeAudioObj(classTree, filePath)
                if audio != False:
                    timeStamp += audio.info.length
                    hh_mm_ss = self.TimeCalc(timeStamp)
                else:
                    print("An error occurred during the file length getting!",
                          file=self.output)
        self.output.close()


path = input("Enter the path of the folder: ")
isNum = input("Would you like to enumerate the tracks? (y/n) ")
if isNum.lower() == "y":
    isNum = True
else:
    isNum = False
MyYTtimestamp = YTtimestamp(path, isNum)
MyYTtimestamp.Run()
