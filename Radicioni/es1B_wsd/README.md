## Es.2 - Word Sense Disambiguation

In this exercise we try to implementi the lesk algorithm for word sense disambiguation.

### Introduzione al problema

Per identificare il senso di una parola dobbiamo andare ad osservare l'intorno di parole attorno ad essa.
Ma quante parole servono per determinare il senso di una parola?
Chiamiamo questo vettore **feature vector**.

Per costruire questo vettore abbiamo intanto bisogno di effettuare alcune operazioni preliminari:
- **PoS tagging**: taggiamo le parole con il suo pos tag.
- **Lemming o Stemming**: riduciamo le parole in base alle regole di lemmatizzazione/stemming.
- **Syntactic Parsing**: analizziamo la frase con il parser sintattico per determinare le relazioni di dipendenza.

Dopo aver ripulito le frasi possiamo estrarre il *contex feature*, l'insieme di parole utili a capire il senso 
di una parola.

Abbiamo due classi di *features*:
- **Collocation features:** E' una parola o una frase con associata la posizione rispetto ad una determinata parola. 
    Inoltre associamo alle parole il loro PoS tag. Esempio: *[guitar, NN, and, CC, player, NN, stand, VB]*
    Da notare che l'ordine delle parole conta.
- **Bag of Words:** In questo caso invece l'ordine delle parole non conta. Andiamo a costruire un vettore
    a partire dalle N parole che occorrono più spesso all'interno di un corpus esterno.
    Dopo di che creiamo un vettore di 0 di lunghezza N, e andiamo a mettere +1 se una determinata parola
    appare nella frase. *[0,0,1,0,0,1,1,0,0]*

**the Lesk Algorithm**
```
function SimplifiedLesk(word,sentence)
    # returns best sense of word
    # best-sense ⇥ most frequent sense for word
    max-overlap ⇥ 0
    context ⇥ set of words in sentence
    for all senses of word do
        signature ⇥ set of words in the gloss and examples of sense
        overlap ⇥ ComputeOverlap(signature,context)
        if overlap > max-overlap then
            max-overlap ⇥ overlap
        best-sense ⇥ sense
        end if
    end for
    return best-sense
```
