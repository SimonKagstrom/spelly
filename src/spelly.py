import pyttsx3
import random
import blessed
import time

def changeVoice(engine, language, gender='VoiceGenderFemale'):
    for voice in engine.getProperty('voices'):
        if language in voice.languages and gender == voice.gender:
            engine.setProperty('voice', voice.id)
            return True

    raise RuntimeError("Language '{}' for gender '{}' not found".format(language, gender))

class Spelly:
    ST_WELCOME = 1
    ST_PRESENT_WORD = 2
    ST_WAIT_KEYS = 3
    ST_WORD_DONE = 4

    def __init__(self, term):
        self.term = term
        self.nicks = ["Roy", "Roy Gunnar", "Roy Ramstedt", "Gubba-lubben"]
        self.words = ["kalkon", "måne", "ninja", "lego", "linda", "moa", "simon", "skola"]
        self.shuffledWords = self.words

        self.talkQueue = []
        self.curWord = ""
        self.curGuess = ""
        self.chars = []
        self.state = Spelly.ST_WELCOME

        engine.connect('finished-utterance', self.onEnd)

        random.shuffle(self.shuffledWords)

    def getNick(self):
        return random.choice(self.nicks)

    def getWord(self, length):
        if len(self.shuffledWords) == 0:
            return None

        out = self.shuffledWords.pop()

        return out

    def getCharacter(self):
        with term.cbreak(), term.hidden_cursor():
            inp = term.inkey()
            return inp

    def onEnd(self, name, completed):
        if len(self.talkQueue) != 0:
            cur = self.talkQueue.pop()
            engine.say(cur)
        self.event()

    def event(self):
        if self.state == Spelly.ST_PRESENT_WORD:
            self.curWord = self.getWord(2)
            if self.curWord == None:
                return
            self.state = Spelly.ST_WAIT_KEYS
            self.chars = []
            self.curGuess = "_" * len(self.curWord)
            print(term.home + term.clear + term.move_y(term.height // 2))
            print(term.black_on_darkslategray3(term.center(self.curGuess)))
            engine.say(f"{self.getNick()}, stava till ordet {self.curWord}, {len(self.curWord)} bokstäver")

        elif self.state == Spelly.ST_WAIT_KEYS:
            if len(self.curWord) == len(self.chars):
                self.state = Spelly.ST_WORD_DONE
                what = "".join(self.chars)
                engine.say(f"Du svarade {what}")
            else:
                c = self.getCharacter()
                left = len(self.curWord) - len(self.chars) - 1
                self.chars.append(c)
                self.curGuess = "".join(self.chars) + "_" * left
                print(term.home + term.clear + term.move_y(term.height // 2))
                print(term.black_on_chartreuse3(term.center(self.curGuess)))
                engine.say(c)

        elif self.state == Spelly.ST_WORD_DONE:
            what = "".join(self.chars)
            self.state = Spelly.ST_PRESENT_WORD

            text = f"Nästan rätt, försök igen!"
            prettyText = term.black_on_darkorange1(term.center(text))
            if what == self.curWord:
                text = f"Helt rätt, ta ett nytt ord!"
                prettyText = term.black_on_chartreuse3(term.center(text))

            print(term.home + term.clear + term.move_y(term.height // 2))
            print(prettyText)
            engine.say(text)


    def run(self):
        self.state = Spelly.ST_PRESENT_WORD
        engine.say("Välkommen!")
        engine.startLoop()

if __name__ == "__main__":

    term = blessed.Terminal()

    print(term.home + term.clear + term.move_y(term.height // 2))
    print(term.black_on_darkkhaki(term.center('Stavning!')))

    engine = pyttsx3.init()
    spelly = Spelly(term)
    changeVoice(engine, "sv_SE", "VoiceGenderFemale")

    spelly.run()
