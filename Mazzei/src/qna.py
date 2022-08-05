# Piton question and answer
import simplenlg as nlg
from matcher import *
from constants import *
from frame import Frame


lexicon = nlg.Lexicon.getDefaultLexicon()
nlg_factory = nlg.NLGFactory(lexicon)
realiser = nlg.Realiser(lexicon) 

#* OK
def greetings():
    s_1 = nlg_factory.createClause(pick_random(GREETINGS))

    verb = nlg_factory.createVerbPhrase("be")
    subj = nlg_factory.createNounPhrase("your", "name?")
    s_2 = nlg_factory.createClause(subj, verb)
    s_2.setFeature(nlg.Feature.INTERROGATIVE_TYPE, nlg.InterrogativeType.WHAT_OBJECT)
    
    coord = nlg_factory.createCoordinatedPhrase()
    coord.setConjunction(",")
    coord.addCoordinate(s_1)
    coord.addCoordinate(s_2)

    output = realiser.realiseSentence(coord)
    return output

#* OK
def start_interview(frame):
    subj_2 = nlg_factory.createNounPhrase("we")
    verb_2 = nlg_factory.createVerbPhrase("start")
    verb_2.setFeature(nlg.Feature.PERSON, nlg.Person.SECOND)
    verb_2.setFeature(nlg.Feature.MODAL, "can")
    obj_2 = nlg_factory.createNounPhrase("the", "interview")
    s_2 = nlg_factory.createClause(subj_2, verb_2, obj_2)

    if frame.get_mood() == 3:
        s_0 = nlg_factory.createClause(f"Ah, yes {frame.get_student_name()}")
        if pick_random([1,2])==1:
            s_1 = nlg_factory.createClause(f"our new ... celebrity")
        else:
            s_1 = nlg_factory.createClause(f"the 'Choosen One'")
        c = nlg_factory.createCoordinatedPhrase()
        c.setConjunction(",")
        c.addCoordinate(s_0)
        c.addCoordinate(s_1)
        coord = nlg_factory.createCoordinatedPhrase()
        coord.setConjunction(",")
        coord.addCoordinate(c)
        coord.addCoordinate(s_2)
        
    else:    
        s_1 = nlg_factory.createClause(f"Well {frame.get_student_name()}")
        coord = nlg_factory.createCoordinatedPhrase()
        coord.setConjunction(",")
        coord.addCoordinate(s_1)
        coord.addCoordinate(s_2)

    output = realiser.realiseSentence(coord)
    return output

def ask_ingredients(f):
    if f.get_mood() == 0:
        return kind_question(f)
    elif f.get_mood() == 1:
        return ok_question(f)
    else:
        return angry_question(f)
    
        
#! QUESTIONS

# frase del tipo: "Which ingredients are in Polyjuice potion ingredient's list?"
#*OK
def kind_question(frame):
    n = pick_random([1,2])
    verb = nlg_factory.createVerbPhrase("be")
    if n == 2:
        verb.setFeature(nlg.Feature.MODAL, "must")
    subject = nlg_factory.createNounPhrase(pick_random(SIN_INGREDIENT))

    if n == 1:
        object = nlg_factory.createNounPhrase(pick_random(SIN_LIST))
        object.addPreModifier("in " + f"{frame.get_potion_name()}" +  f" {pick_random(SIN_INGREDIENT)}'s")
    else:
        if not frame.empty_frame():
            object = nlg_factory.createNounPhrase(f"in the {pick_random(SIN_POTION)}")
        else:
            object = nlg_factory.createNounPhrase(f"in the {frame.get_potion_name()}")

    sentence = nlg_factory.createClause(subject, verb, object)
    sentence.setFeature(nlg.Feature.INTERROGATIVE_TYPE, nlg.InterrogativeType.WHAT_SUBJECT)
    
    output = realiser.realiseSentence(sentence)
    return output

# frase del tipo: "What does Polyjuice potion contain?"
#*OK
def ok_question(frame):
    n = pick_random([1,2])
    verb = nlg_factory.createVerbPhrase(pick_random(SIN_VERBS))
    verb.setFeature(nlg.Feature.PERSON, nlg.Person.THIRD)
    if not frame.empty_frame():
        verb.addModifier("else")
        if n == 1:
            subject = nlg_factory.createNounPhrase(f"{frame.get_potion_name()}")
        else:
            subject = nlg_factory.createNounPhrase(f"the {pick_random(SIN_POTION)}")
    else:
        subject = nlg_factory.createNounPhrase(f"{frame.get_potion_name()}")
        
    sentence = nlg_factory.createClause(subject, verb)
    sentence.setFeature(nlg.Feature.INTERROGATIVE_TYPE, nlg.InterrogativeType.WHAT_OBJECT)
    output = realiser.realiseSentence(sentence)
    return output

# frase del tipo: "Tell me the ingredients of the potion"
#*OK
def angry_question(frame):
    n = pick_random([1,2,3])
    verb = nlg_factory.createVerbPhrase("Tell")
    verb.setFeature(nlg.Feature.PERSON, nlg.Person.SECOND)
    verb.addPostModifier("me")
    if frame.empty_frame():
        obj = nlg_factory.createNounPhrase(f"{pick_random(SIN_INGREDIENT)}")
        obj.addPreModifier("the")
        obj.addPostModifier(f"of the {frame.get_potion_name()}")
    else:
        if n == 3:
            obj = nlg_factory.createNounPhrase("one,")
            obj.addPostModifier(f"{pick_random(SIN_INSULTS)}")
        elif n == 2:
            obj = nlg_factory.createNounPhrase(f"{pick_random(SIN_INGREDIENT)}")
            obj.addPostModifier(f"of the {frame.get_potion_name()}")
        else:
            obj = nlg_factory.createNounPhrase(f"{pick_random(SIN_INGREDIENT)}")
            obj.addPostModifier(f"of the {pick_random(SIN_POTION)}") 
        
        obj.addPreModifier("another")
    
    sentence = nlg_factory.createClause(verb, obj)
    output = realiser.realiseSentence(sentence)
    return output
    
#! ANSWERS

def bad_response(frame):
    n = pick_random([1,2])
    if frame.get_mood() >= 2:
        subj = nlg_factory.createNounPhrase("you")
        if n == 1:
            verb = nlg_factory.createVerbPhrase("want")
            verb.addPostModifier(f"me as an enemy, {frame.get_student_name()}")
            sentence = nlg_factory.createClause(subj, verb)
            sentence.setNegated(True)
        else:
            verb = nlg_factory.createVerbPhrase("be")   
            verb.setFeature(nlg.Feature.MODAL, "can")
            obj = nlg_factory.createNounPhrase("so", "stupid")
            sentence = nlg_factory.createClause(subj, verb, obj)
            sentence.setFeature(nlg.Feature.INTERROGATIVE_TYPE, nlg.InterrogativeType.HOW)
    elif frame.get_mood() == 1:
        if n == 1:
            verb = nlg_factory.createVerbPhrase("waste")
            verb.setNegated(True)
            verb.setFeature(nlg.Feature.PERSON, nlg.Person.SECOND)
            dobj = nlg_factory.createNounPhrase("my", "time")
            
            sentence = nlg_factory.createClause(verb, dobj)
        else:
            subj = nlg_factory.createNounPhrase("That")
            verb = nlg_factory.createVerbPhrase("be")
            obj = nlg_factory.createNounPhrase("totally", "wrong")

            sentence = nlg_factory.createClause(subj, verb, obj)
    else:
        if n == 1:
            verb =  nlg_factory.createVerbPhrase("try")
            verb.setFeature(nlg.Feature.PERSON, nlg.Person.SECOND)
            verb.addPostModifier("again")
            
            sentence = nlg_factory.createClause(verb)
        else: 
            verb = nlg_factory.createVerbPhrase("be")
            verb.setNegated(True)
            subj = nlg_factory.createNounPhrase("That")
            obj = nlg_factory.createNounPhrase(f"the {pick_random(SIN_CORRECT)}", f"{pick_random(SIN_INGREDIENT)}")

            sentence = nlg_factory.createClause(subj, verb, obj)
            
    output = realiser.realiseSentence(sentence)
    return output

#* OK
def good_response(frame):
    if frame.get_mood() == 3:
        verb = nlg_factory.createVerbPhrase("be")
        verb.setFeature(nlg.Feature.PERSON, nlg.Person.FIRST)
        subj = nlg_factory.createNounPhrase("this")
        obj = nlg_factory.createNounPhrase("the best")
        s = nlg_factory.createClause(subj, verb, obj)
        s.setFeature(nlg.Feature.INTERROGATIVE_TYPE, nlg.InterrogativeType.YES_NO)

        verb_1 = nlg_factory.createVerbPhrase(f"can do {frame.get_student_name()}?")
        verb_1.setFeature(nlg.Feature.PERSON, nlg.Person.SECOND)
        subj_1 = nlg_factory.createNounPhrase("you")
        s_1 = nlg_factory.createClause(subj_1, verb_1)

        coord = nlg_factory.createPrepositionPhrase(s, s_1)

        '''coord.setFeature(nlg.Feature.INTERROGATIVE_TYPE, nlg.InterrogativeType.HOW)'''

        output = realiser.realiseSentence(coord)

    elif frame.get_mood() == 2:    
        verb_1 = nlg_factory.createVerbPhrase("be")
        subj_1 = nlg_factory.createNounPhrase("That")
        obj_1 = nlg_factory.createNounPhrase("slightly", "sufficient")
        s_1 = nlg_factory.createClause(subj_1, verb_1, obj_1)

        verb_2 = nlg_factory.createVerbPhrase("go on")
        verb_2.setFeature(nlg.Feature.MODAL, "can")
        subj_2 = nlg_factory.createNounPhrase("you")
        s_2 = nlg_factory.createClause(subj_2, verb_2)

        coord = nlg_factory.createCoordinatedPhrase()
        coord.setConjunction(",")
        coord.addCoordinate(s_1)
        coord.addCoordinate(s_2)

        output = realiser.realiseSentence(coord)
        
    elif frame.get_mood() == 1:
        s_1 = nlg_factory.createClause("Ok")

        subj_2 = nlg_factory.createNounPhrase("it")
        verb_2 = nlg_factory.createVerbPhrase("be")
        obj_2 = nlg_factory.createNounPhrase(f"{pick_random(SIN_CORRECT)}")
        s_2 = nlg_factory.createClause(subj_2, verb_2, obj_2)

        coord = nlg_factory.createCoordinatedPhrase()
        coord.setConjunction(",")
        coord.addCoordinate(s_1)
        coord.addCoordinate(s_2)

        output = realiser.realiseSentence(coord)
        
    elif frame.get_mood() == 0:
        verb = nlg_factory.createVerbPhrase("be")
        subj = nlg_factory.createNounPhrase("That")
        obj = nlg_factory.createNounPhrase(f"the {pick_random(SIN_CORRECT)}", f"{pick_random(SIN_INGREDIENT)}")
        s_1 = nlg_factory.createClause(subj, verb, obj)

        output = realiser.realiseSentence(s_1)

    return output

def ask_besides_ingredient(ingredient):
    s_0 = nlg_factory.createClause("Ok")

    subj_2 = nlg_factory.createNounPhrase("it")
    verb_2 = nlg_factory.createVerbPhrase("be")
    obj_2 = nlg_factory.createNounPhrase(f"{pick_random(SIN_CORRECT)}")
    s_2 = nlg_factory.createClause(subj_2, verb_2, obj_2)

    coord = nlg_factory.createCoordinatedPhrase()
    coord.setConjunction(",")
    coord.addCoordinate(s_0)
    coord.addCoordinate(s_2)
    subj = nlg_factory.createNounPhrase("the", f"{pick_random(SIN_POTION)}")
    verb = nlg_factory.createVerbPhrase(f"{pick_random(SIN_VERBS)}")
    obj = nlg_factory.createNounPhrase(f"{pick_random(SIN_INGREDIENT)}")
    p_2 = nlg_factory.createNounPhrase(f"{pick_random(SIN_BESIDES)} {ingredient}")
    s_1 = nlg_factory.createClause(subj, verb, obj)
    s_1.addPostModifier(p_2)
    s_1.setFeature(nlg.Feature.INTERROGATIVE_TYPE, nlg.InterrogativeType.WHAT_OBJECT)

    output = realiser.realiseSentence(coord) + " " + realiser.realiseSentence(s_1)
    return output

def last_ingredient():
    verb = nlg_factory.createVerbPhrase("be")
    subj = nlg_factory.createNounPhrase("That")
    obj = nlg_factory.createNounPhrase(f"the {pick_random(SIN_CORRECT)}", f"{pick_random(SIN_INGREDIENT)}")
    s_1 = nlg_factory.createClause(subj, verb, obj)
    
    verb_2 = nlg_factory.createVerbPhrase("be")
    verb_2.setFeature(nlg.Feature.TENSE, nlg.Tense.PRESENT)
    subj_2 = nlg_factory.createNounPhrase("the last", f"{pick_random(SIN_INGREDIENT)}")
    s_2 = nlg_factory.createClause(subj_2, verb_2)
    s_2.setFeature(nlg.Feature.INTERROGATIVE_TYPE, nlg.InterrogativeType.WHAT_OBJECT)
    output = realiser.realiseSentence(s_1) + " " + realiser.realiseSentence(s_2)
    return output

#*OK
def valutation(frame, vote):
    if frame.get_mood() == 3:
        subj_potter = nlg_factory.createNounPhrase("you")
        verb_potter = nlg_factory.createVerbPhrase("be just like")
        obj_potter = nlg_factory.createNounPhrase("dad")
        obj_potter.setDeterminer("your")
        s_potter_1 = nlg_factory.createClause(subj_potter, verb_potter, obj_potter)

        #noun_potter = nlg_factory.createClause(f"{frame.get_student_name()}")

        coord = nlg_factory.createCoordinatedPhrase()
        coord.setConjunction(",")
        coord.addCoordinate(s_potter_1)
        coord.addCoordinate(f"{frame.get_student_name()}")

        potter = realiser.realiseSentence(coord)

    if frame.get_mood() == 3:
        s_1 = nlg_factory.createClause(f"I don't care how much you studied")
    else:    
        s_1 = nlg_factory.createClause(f"Well {frame.get_student_name()}")

    verb_2 = nlg_factory.createVerbPhrase("go")
    verb_2.setFeature(nlg.Feature.TENSE, nlg.Tense.PAST)
    subj_2 = nlg_factory.createNounPhrase("the", "interview")
    
    if vote == "Troll":
        obj_2 = nlg_factory.createNounPhrase("very", "bad")
    elif vote == "Poor" or vote == "Dreadful":
        obj_2 = nlg_factory.createNounPhrase("bad")
    elif vote == "Acceptable" or vote == "Exceeds Expectations":
        obj_2 = nlg_factory.createNounPhrase("well")
    else:
        obj_2 = nlg_factory.createNounPhrase("very", "well")

    s_2 = nlg_factory.createClause(subj_2, verb_2, obj_2)
    
    subj_3 = nlg_factory.createNounPhrase("your", "vote")
    verb_3 = nlg_factory.createVerbPhrase("be")
    obj_3 = nlg_factory.createNounPhrase(vote)
    s_3 = nlg_factory.createClause(subj_3, verb_3, obj_3)

    coord = nlg_factory.createCoordinatedPhrase()
    coord.addCoordinate(s_1)
    coord.addCoordinate(s_2)
    coord.addCoordinate(s_3)

    output = realiser.realiseSentence(coord)

    if frame.get_mood() == 3:
        output = potter + " " + output
    return output
