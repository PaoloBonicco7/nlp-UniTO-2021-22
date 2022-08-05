from frame import Frame
from matcher import *
from patterns import *
from qna import *
from audio import *

f = Frame('data/potions.txt')

name = input(f'{greetings()}\n-> ')
find_pattern_name(f, pattern_name, name)
print(start_interview(f))
answer = input(f'{ask_ingredients(f)}\n-> ')

while not f.full_frame() and f.get_chances() > 0:
    
    result = test_patterns(answer)
    
    if f.check_response(result):
        if not f.full_frame():
            if f.remaining_ingredients() == 1:
                answer = input(f'{last_ingredient()}\n-> ')
            else:                    
                rand = random.randint(0,1)
                if rand == 0:
                    answer = input(f'{ask_besides_ingredient(result[0])}\n-> ')
                else:
                    print(good_response(f))
                    answer = input(f'{ask_ingredients(f)}\n-> ')     
    else:
        print(bad_response(f))
        f.dec_chances()
        if f.get_chances() > 0:
            answer = input(f'{ask_ingredients(f)}\n-> ')

vote = get_vote(f)
print(valutation(f, vote))
