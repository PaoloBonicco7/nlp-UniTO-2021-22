# Esercizio 2: Mapping di FrameNet su WordNet

Dato un frame, dobbiamo costruire un insieme chiamato FrameTerms che sarà composto dal nome del frame, dai FE, e dalle LU. A questo punto dobbiamo costruire una funzione $\mu$ che mappi ogni termine contenuto in FrameTerms in un synset.

In particolare l'obiettivo è trovare per ogni termine $f$ il senso di WN $s$ che massimizza una certa misura di similarità. 
 
$$
\mu(f) = argmax_{s \in Senses_WN}  sim(f,s)
$$

Il calcolo della similiarità si basa sulla costruzione di due contesti di disambiguazione, uno per il frame e uno per il synset. Li chiameremo rispettivamente $Ctx(f)$ e $Ctx(s)$.
Per quanto riguarda $Ctx(f)$, viene costruito utilizzando la definizione del frame e le definizioni di tutti i Frame Elements che lo compongono. $Ctx(s)$, invece, viene costruito a partire dal gloss e dai sensi dei synset collegati al termine $f$, eventualmente aggiungendo anche quelli di iponimi o iperonimi.

In particolare, per calcolare la similarità possiamo seguire due approcci:
- Bag of words  
In maniera analoga a BabelNet nell'approccio bag of words la similarità è definito come
$$
sim(f,s) = |Ctx(f) \cap Ctx(s)| + 1
$$
- Grafico 
Nell'approccio grafico, invece, la similarità viene definita come probabilità condizionata di s dato f, cioè come la probabilità che al termine $f$ corrisponda il senso $s$.
$$ sim(f,s) = p(s|f) $$
Da notare che dovendo calcolare l'$argmax$ possiamo considerare, invece, la probabilità congiunta $p(s,f)$.
Per calcolare tale probabilità

$$
p(s,f) = \frac{score(s,f)}{\sum_{s',f'} score(s',f')}
$$

dove $s'$ spazia nei sensi di WN collegati al nome del frame $f$, e $f' \in Ctx(f)$. La funzione $score(s,f)$ in questo caso dipende dalla distanza in WN di $s$ dai sensi di WN di tutte i termini di $Ctx(f)$.