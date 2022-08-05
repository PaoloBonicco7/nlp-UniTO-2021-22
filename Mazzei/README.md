# **Relazione Progetto TLN Parte 1 - Mazzei**

# Severus Python

## Introduzione
Severus Python è un Dialog System che simula un'interrogazione ispirata alla saga di Harry Potter, nello specifico del corso di pozioni, tenuto dal professor Severus Piton.
Il nostro sistema è *task based*, infatti il suo scopo è domandare allo studente, che non è altro che l'utente che interagisce con il sistema, quali sono gli ingredienti di una pozione.

## Funzionamento di base
Quello che caratterizza il nostro sistema è la rappresentazione dello stato dell'umore del professore, in grado di influenzare la generazione del testo e il numero di tentativi a disposizione dello studente.
Nello specifico il sistema risponderà in maniera più fredda e irritata a seconda dell'umore.
All'inizio di ogni simulazione il dialog manager setterà una variabile che rappresenta il numero di tentivi a disposizione dello studente.
Tale numero si decrementerà di 1 ogni votla che lo studente sbaglierà una risposta. 
All'esaurirsi dei tentativi il sistema terminerà la simulazione, fornendo un voto all'utente.

Il sistema andrà a domandare allo studente di elencare uno alla volta gli ingredienti di una pozione. 
Dovrà quindi capire ed estrarre l'ingrediente dalla frase, controllare se è corretto e comunicarlo allo studente.
La simulazione terminerà quando lo studente avrà detto tutti gli ingredienti della pozione, o quando avrà esaurito i tentativi.

## Come estraiamo le informazioni dalla frase
Per trovare le informazioni utili all'interno della frase, come gli ingredienti e il nome dello studente, utilizziamo il `DependecyMatcher` di spacy, grazie al quale troviamo le relazioni di dipendenza all'interno delle frasi.
Abbiamo analizzato un insieme di possibili frasi in input e abbiamo scoperto che le frasi avevano una struttura simile.
Da questa conclusione abbiamo costruito la struttura dei pattern, che sono in grado di isolare porzioni dell'albero a dipendenze della frase in input.
Queste porzioni corrispondono alle informazioni che vogliamo estrarre dalla frase, come gli ingredienti e il nome dello studente.
Abbiamo generato 11 pattern in grado di riconoscere tutti gli ingredienti presenti nelle 3 pozioni che abbiamo selezionato.

## Le frasi in input
Abbiamo selezionato un insieme di frasi in input e abbiamo deciso di restringere il dominio del nostro sistema a queste frasi.

Le frasi su cui abbiamo lavorato sono:

- X is contained in the potion

- X are contained in the potion

- X is used in the potion

- X are used in the potion

- X is needed in the potion

- X are needed in the potion

- The potion contains X

- The potion uses X

- The potion needs X

- X

- The answer is X

Dove al posto di X ci sono i vari ingredienti delle pozioni.

Nella file `test.py` abbiamo definito delle funzioni che permettono di testare il corretto funzionamento del sistema.
Nello specifico nella classe `TestSentences` abbiamo testato tutte le possibili combinazioni, ottenendo, per il nostro insieme di ingredinenti e il nostro insieme di frasi,
un accuratezza del 100%. 
In pratica il nostro sistema è sempre in grado di estrarre un ingrediente da una delle frasi sopra citate se l'ingrediente è presente nella nostra lista di ingredienti.

## Come abbiamo strutturato il comportamento del dialog system
Dovendo simulare il comportamento di un professore come Piton, noto per essere particolarmente scorbutico, le risposte del nostro sistema di dialogo sono guidate dal suo umore, caratterizzato da una variabile `mood`.
La variabile `mood` è un intero che rappresenta l'umore del professore. 
Questo valore oscilla tra 0 (stato di quiete/felicità) e 2 (stato di irritazione massima).
L'umore del professore è generato in maniera randomica. Quando irritato sarà molto più secco con le risposte, sopratutto in caso di errore.
Inoltre più è arrabbiato, meno chance avrà lo studente di sbagliare.

## Diamo un'occhiata al codice

### **frame**
Un frame è una struttura dati che utilizziamo per salvare tutte le informazioni ricavate dall'interazione tra utente e sistema.
Nello specifico salviamo le seguenti variabili:

* `potions` -> La lista di pozioni
* `student_ingridients` -> La lista degli ingredienti corretti detti da uno studente
* `potion_name` -> Il nome della pozione corrente, oggetto dell'interrogazione
* `student_name` -> Il nome dello studente
* `mood` -> Indica l'umore del professore

Oltre ai metodi getter e setter, abbiamo altri due metodi:

- `add_potions` -> Va a leggere il file contenente le pozioni (potions.txt) e le aggiunge alla lista di pozioni del frame
- `check_response` -> Prende in input l'ingrediente detto dall'utente e se l'ingrendiente è corretto e non è stato già detto, aggiunge l'ingrediente alla lista degli ingredienti corretti.

### **dialogmanager**
Questo file contiene i metodi in grado di riconoscere le informazioni rilevanti all'interno di una frase, tramite l'ausilio di vari patter.

- `get_matched_patterns` -> Data una frase in input, un pattern e il nome del pattern restituisce la porzione di frase che rispetta il pattern. Questo metodo utilizza il `DependecyMatcher` di spacy.
Ritorna la sotto sequenza di parole più lunga trovata nella frase, e se non ha trovato nessuna parola ritorna "No Match". Questo metodo verrà richiamato più volte, in modo da trovare almeno un pattern che fa match con la
frase in input.
Visto che gli ingredienti delle pozioni hanno nomi caratterizzati da più parole, ritorniamo sempre la sotto sequenza più lunga perchè altrimenti il sistema di dialogo potrebbe estrarre 
solamente una parte dell'ingrediente (es. *"The Crisopa"* e non *"The Crisopa Fly"*).
- `find_pattern_name` -> Utilizzata per trovare il nome dello studente all'interno di una frase. Il meccanismo è simile a quello di prima. Il metodo viene richiamato all'inizio della simulazione, 
quando allo studente viene cheisto il nome.
- `test_pattern` -> Questo metodo richiama il metodo `get_matched_patterns` per ogni pattern, e restituisce la sotto sequenza che rispetta il pattern. Se non lo trova ritorna tutta la frase. 
Questo perchè se non viene trovato un pattern assumiamo che la frase contenga solo un ingrediente.
- `get_vote` -> Questo metodo restituisce il voto dell'interrogazione. Il voto sarà influenzato dal numero di ingredienti detti dallo studente, 
dal numero di errori commessi e, infine, come ogni interrogazione che si rispetti, dall'umore del professore.

### qna
Questo è il file in cui generiamo le frasi con la libreria `simpleNLG`.
La libreria è scritta in Java, quindi noi abbiamo sfruttato il porting in python per il nostro progetto.
Questa liberia si è rivelata particolarmente utile per generare più frasi con un solo metodo, in quanto permette di cambiare verbi e modificatori in
poche linee di codice, senza dover riscrivere intere frasi.
Ciò ci ha permesso di generare frasi diverse in base alle condizioni interne del dialog manager, come l'umore e lo stato dell'interrogazione.

### **main**
Nel main simuliamo il funzionamento dell'intero dialogo. 

**Modalità audio**:

Abbiamo implementato anche la possibilità di avere un dialogo verbale con il nostro Dialog System.
Per farlo abbiamo utilizzato una libreria di google, grazie alla quale siamo riusciti a riprodurre le frasi dagli autoparlanti del computer e ad inserire le risposte tramite il microfono.

*Problematiche modalità audio:*

Purtroppo gli ingredienti delle pozioni sono per la maggior parte parole inventate, che il sintetizzatore di google non riesce a capire.
Per questa ragione abbiamo disabilitato questa funzionalità in quanto gli ingredienti non venivano riconosciuti.
Inoltre le performance del **TTS** sono influenzate dal microfono e dal rumore ambientale.

*Possibili soluzioni:*

 - Abbiamo sperimentato il sistema con parole di uso comune e abbiamo visto che il sistema è in grado di capire gli ingredienti.
 - Un'altra possibile soluzione è sfruttare una funzione di google (`recognize_google_cloud`) che ti permette di specificare il testo atteso e guidare il traduttore verso la corretta parola.

**Inizio Interazione**

Il sistema inizia generando un'istanza della classe Frame, in cui saranno salvate tutte le informazioni riguardanti l'interazione, come i dettagli della pozione.
La pozione sarà estratta a caso tra una lista di 3 pozioni dal file *potions.txt*.
I dettagli della classe Frame li vedremo in seguito.

Una volta selezionata una pozione, l'interazione avrà inizio con la richiesta del nome del partecipante.
Andiamo a ricercare nella frase il nome utilizzando, come sempre faremo, il `DependecyMatcher` di spacy. 
Il sistema di dialogo è quindi in grado di capire se il nome è presente nella frase o meno, anche se la frase contiene altre parole oltre al nome (come ad esempio **"My name is Ron Weasley"**).

### **constants**
Contiene tutte le costanti che abbiamo utilizzato nel dialog system, come le liste di stringhe e le valutazioni da assegnare.
Le valutazioni sono, ovviamente, appartenenti all'universo di Harry Potter e vanno da *"Troll"* a *"Outstanding"*.

### **patterns**
In questo file invece abbiamo messo tutti i pattern che abbiamo utilizzato per riconoscere gli ingredienti e i nomi degli studenti all'interno delle frasi.

### **test**
Questo file contiene tutti i test per verificare il corretto funzionamento del sistema di dialogo.

## I limiti del nostro sistema:
 - **Frasi in input:** Il nostro sistema, allo stato attuale, è in grado di riconoscre gli ingredienti delle 3 pozioni che abbiamo selezionato.
Inolte si comporta molto bene per le frasi che abbiamo testato, se però in input viene fornita una frase che non abbamo previsto potrebbe fallire nella ricerca dell'ingrediente nella frase.

 - **Frasi in output:** Il nostro sistema genera frasi in output utilizzando la libreria `simpleNLG`. Questa libreria si è rivelata molto potente per generare frasi in maniera automatica. 
Si potrebbe però estendere il nostro sistema per generare frasi in output in modo da renderlo ancora più parametrico, andando ad estendere le possibili alternative selezionabili all'interno di una frase.
Noi ci siamo limitati a generare alcune frasi, che venivano selezionate in base all'umore del professore e allo stato dell'interrogazione.

 - **Audio mode:** Come già detto il nostro sistema funziona bene sul testo scritto, mentre sull'input vocale fa più fatica. 
Questo è causato dal fatto che gli ingredienti delle pozioni non sono parole "reali" visto che appartengono a dominio Fantasy. 

## Vediamo insieme qualche simulazione di esecuzione del programma

Abbiamo fatto 3 simulazioni con 3 pozioni diverse. Normalmente la variabile `mood` viene impostata in maniera randomica,
ma in questo caso abbiamo forzato la variabile prima a 0 (prof. felice) e poi a 2 (prof. arabbiato).
Per la terza esecuzione invece il `mood` era settato a 3 siccome, quando lo studente si chiama potter, il sistema si irrita
subito entrando in *potter mode*. Il sistema di dialogo in questo caso è al massimo del suo stato di irritazione.

Gli input dello studente sono preceduti da dal simbolo `"->"`.

### Simulazione 1 - mood = 0

Nella seguente esecuzione del programma possiamo notare come il tono del professore sia particolarmente tranquillo e pacato.

In questo caso lo studente no ha commesso errori e infatti ha ottenuto il massimo dei voti: Outstanding.

![Simulazione 1](/images/Simulazione_1.png "Simulazione 1")

### Simulazione 2 - mood = 2

Nella seguente esecuzione del programma possiamo notare come il tono del professore sia particolarmente tranquillo e pacato.

In questo caso lo studente no ha commesso errori e infatti ha ottenuto il massimo dei voti: Outstanding.

![Simulazione 2](/images/Simulazione_2.png "Simulazione 2")



## Concetti da rivedere

La parte difficile riguarda proprio il dominio. Infatti abbiamo avuto molti problemi siccome gli ingredienti delle pozioni, 
che appartengono all'universo di Harry Potter, non sono parole che vengono usate tutti i giorni. Questo ha reso particolarmente difficile
l'estrazione delle informazioni dalle frasi. Per risolvere questo problema abbiamo generato dei pattern che riconoscano tutti gli ingredienti delle nostre 3 pozioni.

## Dialog System Architecture:

- **speech recognition**: la parte di speech recognition del nostro sistema è parzialmente funzionante siccome, come già detto prima, non è in grado
di riconoscere le parole inventate delle pozioni di Harry Potter, per questa ragione l'input del nostro sistema è un input testuale.
- **language understanding**: per comprendere il linguaggio abbiamo utilizato il `DependencyMatcher` di spacy e, tramite l'ausilio dei pattern, estraiamo l'informazione importante della frase, 
che consiste nell'ingrediente della pozione. Questa è la parte più complicata, infatti il nostro sistema funziona solo con un insieme ristretto di frasi in input.
- **dialog manager**: questa è il cuore pulsante del nostro sistema, in cui si valuta l'input in ingresso (l'ingrediente) e si prendere una decisione su come proseguire la simulazione.
Nel nostro caso specifico andiamo a controllare se l'ingrediente in ingresso è corretto e, sulla base delle condizioni del sistema (numero di tentativi rimasti, numero di ingredienti mancanti e umore del professore)
decidiamo che frase generare in output.
- **response generator**: Questo è il momento in cui andiamo effettivamente a generare la frase in output. 
Il **text planning* la facciamo nella classe dialog manager, in cui appunto andiamo ad analizzare lo stato del sistema e decidiamo che frase generare.
Per quanto riguarda il *sentence planning* e la *linguistic realization* usiamo la classe qna in cui abbiamo sfruttato la libreria `simpleNLG`.
- **text to speech synthesis**: Come per lo *speech reconition* questa caratteristica del sistema e funzionante ma disabilitata siccome l'utente può interagire solo in maniera scritta con il sistema


## Notes:
Use class.funcion().__doc__ to get the documentation of a function.
Sito utilizzato pe conversione in pdf: https://cloudconvert.com/md-to-pdf