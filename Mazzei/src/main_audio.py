from frame import Frame
from matcher import *
from patterns import *
from qna import *
from audio import *

f = Frame('/home/andrea/Desktop/Università/TLN/Parte 1/Severus-Python/data/potions_audio.txt')

text = greetings()
text_to_speech(text)
name = speech_recognition()
find_pattern_name(f, pattern_name, name)
text = start_interview(f)
text_to_speech(text)
text = ask_ingredients(f)
text_to_speech(text)
answer = speech_recognition()

while not f.full_frame() and f.get_chances() > 0:

    result = test_patterns(answer)
    
    if f.check_response(result):
        if not f.full_frame():
            if f.remaining_ingredients() == 1:
                text = last_ingredient()
                text_to_speech(text)
            else:
                rand = random.randint(0,1)
                if rand == 0:
                    text = ask_besides_ingredient(result[0])
                    text_to_speech(text)
                    answer = speech_recognition()
                else:
                    text = good_response(f)
                    text_to_speech(text)
                    answer = speech_recognition()    
    else:
        text = bad_response(f)
        text_to_speech(text)
        f.dec_chances()
        if f.get_chances() > 0:
            text = ask_ingredients(f)
            text_to_speech(text)
            answer = speech_recognition()
    
vote = get_vote(f)
text = valutation(f, vote)
text_to_speech(text)