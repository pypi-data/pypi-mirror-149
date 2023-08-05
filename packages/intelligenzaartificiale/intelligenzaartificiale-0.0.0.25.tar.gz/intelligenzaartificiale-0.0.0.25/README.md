###### 🚧 La libreria è ancora in fase di SVILUPPO 🚧
#
#
#
# Intelligenza Artificiale
##### _La libreira python creata per neofiti e datascientist che semplifica l'analisi dati e lo sviluppo di modelli di apprendimento automatico e profondo_
#
#
Intelligenza-Artificiale è l'unica libreria python MADE in ITALY che permette a qualsiasi persona di :

- Leggere, Manipolare, Pulire dataset di ogni tipo
- Analizzare i dati per trasformarli in importanti informazioni
- Creare in meno di 5 righe di codice modelli di ML
- Sviluppare reti neurali
- & molto molto altro ancora

##### **richiamando i metodi in italiano !**
#
#
#

##  Installazione Libreria

La libreria intelligenzaartificiale richiede [PYTHON](https://PYTHON.org/) v3.6+ 

Per installare la libreria puoi usare il comando pip3 .

```sh
pip3 install intelligenzaartificiale
```

se invece utilizzi google colab...

```sh
!pip install intelligenzaartificiale
```

## Partizione Libreria

Al momento abbiamo deciso di partizionare la libreria in moduli, per rendere il codice il più portabile e leggero possibile.

| Modulo | Import | Utilizzo
| ------ | ------ | ------
| Dataset | from intelligenzaartificiale import dataset as dt | lettura e manipolazine set di dati ( .csv , .xlsx , .xls , .html , .json , sql )
| BigDataset | from intelligenzaartificiale import bigdataset as bdt | lettura e manipolazine set di dati molto grandi compresi bigdata
| Statistica | from intelligenzaartificiale import statistica as st | analisi dati
| Preprocessing | from intelligenzaartificiale import preprocessing as pp | pulizia, manipolazione e preprocessing dei dati
| TextPreprocessing | from intelligenzaartificiale import textpreprocessing as tpp | pulizia, manipolazione e preprocessing per dati testuali
| Machine Learning | from intelligenzaartificiale import machinelearning as ml | creazione di modelli di apprendimento automatico
| Deep Learning | from intelligenzaartificiale import depplearning as dl | creazione di reti neurali 
| NLP | from intelligenzaartificiale import nlp | trattamento delle informazioni testuali 

# Esempi

Qui sotto troverai elencati tutti i metodi della libreria con degli esempi

## _Step 1 ---_  **Modulo Dataset e BigDataset**

Con questo modulo potrai leggere qualsiasi tipo di dataset
#
Leggere un file .csv
```sh
from intelligenzaartificiale import dataset as dt
il_mio_dataset = dt.leggi_csv("file_name.csv")
```
#
Leggere file .csv enormi
```sh
from intelligenzaartificiale import bigdataset as bdt
il_mio_dataset = bdt.leggi_csv("Bigfile.csv")

#per convertire il file molto grande in un file leggibile anche con il modulo DATASET
bdt.salva_feather(il_mio_dataset,"nuovoFile")

from intelligenzaartificiale import dataset as dt
il_mio_dataset = dt.leggi_feather("nuovoFile.feather")
```

#
Leggere un file excel
```sh
from intelligenzaartificiale import dataset as dt
il_mio_dataset = dt.leggi_xls("file_name.xls")
```
Leggere un foglio specifico di un file excel
```sh
from intelligenzaartificiale import dataset as dt
il_mio_dataset = dt.leggi_sheet("file_name.xls","nome_foglio")
```

#
Leggere un file html
```sh
from intelligenzaartificiale import dataset as dt
il_mio_dataset = dt.leggi_html("file_name.html")
```

#
Leggere un file json
```sh
from intelligenzaartificiale import dataset as dt
il_mio_dataset = dt.leggi_json("file_name.json")
```

#
Leggere un file sql
```sh
from intelligenzaartificiale import dataset as dt
il_mio_dataset = dt.leggi_json("file_name.sql")
```
#
Carica e lavora su oltre 750+ dataset già caricati 
```sh
from intelligenzaartificiale import dataset as dt

#ritorna la lista dei nomi degli oltre 750 dataset disponibili
print(dt.lista_datasets())

#ritorna la documentazione del dataset scelto
print(dt.documentazione_dataset("iris"))

#ritorna il dataframe del dataset richiesto
il_mio_dataset= dt.importa_dataset("iris")
```

#
Ottenere informazioni di base sulle colonne
```sh
from intelligenzaartificiale import dataset as dt
il_mio_dataset = dt.leggi_csv("file_name.csv")
print(dt.lista_colonne(il_mio_dataset))
print(dt.tipo_colonne(il_mio_dataset))
```

#
Rimuovere una o più colonne
```sh
from intelligenzaartificiale import dataset as dt
il_mio_dataset = dt.leggi_csv("file_name.csv")
nuovo_dataset = dt.rimuovi_colonna(il_mio_dataset, "colonna_da_eliminare")

colonne_inutili = ["colonna3", "colonna12" , "colonna33"]
nuovo_dataset = dt.rimuovi_colonne(il_mio_dataset, colonne_inutili)

```

#
Separare i vari tipi di dato
```sh
from intelligenzaartificiale import dataset as dt
il_mio_dataset = dt.leggi_csv("file_name.csv")
valori_numerici = dt.numerici(il_mio_dataset)
valori_categorici = dt.categorici(il_mio_dataset)
valori_booleani = dt.booleani(il_mio_dataset)
```

#
Eseguire semplici query sul dataset
```sh
from intelligenzaartificiale import dataset as dt

il_mio_dataset = dt.leggi_csv("file_name.csv")
acquisti_alti = dt.esegui_query(il_mio_dataset,il_mio_dataset["prezzo"]>1000)

```
#
#
#

## _Step 2 ---_  **Modulo Statistica**

Con questo modulo potrai fare statistiche, report e analisi sui tuoi dati
#
Valori Nulli o Corrotti
```sh
from intelligenzaartificiale import dataset as dt
from intelligenzaartificiale import statistica as st

il_mio_dataset = dt.leggi_csv("file_name.csv")
print(st.valori_nan(il_mio_dataset))
print(st.percentuale_nan(il_mio_dataset))
#nel modulo preprocessing vedremmo come eliminare o sostituire i valori null o corrotti
```

#
Statistiche di base
```sh
from intelligenzaartificiale import dataset as dt
from intelligenzaartificiale import statistica as st

il_mio_dataset = dt.leggi_csv("file_name.csv")

#statistiche su tutto il dataset
print(st.valori_nan(il_mio_dataset))

#statistiche su specifica colonna del dataset
print(st.statistiche_colonna(il_mio_dataset,"nome_colonna"))

#contare valori unici di una specifica colonna
print(st.conta_valori_unici(il_mio_dataset,"nome_colonna"))
```

#
Statistiche di base su colonna
```sh
from intelligenzaartificiale import dataset as dt
from intelligenzaartificiale import statistica as st

il_mio_dataset = dt.leggi_csv("file_name.csv")

#media
print(st.media(il_mio_dataset,"nome_colonna"))

#varianza
print(st.varianza(il_mio_dataset,"nome_colonna"))

#covarianza
print(st.covarianza(il_mio_dataset,"nome_colonna"))

#quantili
print(st.quantile_25(il_mio_dataset,"nome_colonna"))
print(st.quantile_50(il_mio_dataset,"nome_colonna"))
print(st.quantile_75(il_mio_dataset,"nome_colonna"))

#min e max
print(st.min(il_mio_dataset,"nome_colonna"))
print(st.max(il_mio_dataset,"nome_colonna"))
```

#
Analizzare le correlazioni 
```sh
from intelligenzaartificiale import dataset as dt
from intelligenzaartificiale import statistica as st

il_mio_dataset = dt.leggi_csv("file_name.csv")

#Correlazione tra i campi del dataset
print(st.correlazione(il_mio_dataset))

#correlazione tra una colonna target e un altra colonna
print(st.correlazione_radio(il_mio_dataset, "colonna" ,"target_colonna"))

#correlazione di Spearman tra una colonna target e un altra colonna
print(st.correlazione_spearman(il_mio_dataset, "colonna" ,"target_colonna"))

#correlazione di Pearson tra una colonna target e un altra colonna
print(st.correlazione_pearson(il_mio_dataset, "colonna" ,"target_colonna"))

#classifica correlazione tra una colonna target e un altra colonna
print(st.classifica_correlazione_colonna(il_mio_dataset, target_colonna"))
```

#
Report Automatizzati 
```sh
from intelligenzaartificiale import dataset as dt
from intelligenzaartificiale import statistica as st

il_mio_dataset = dt.leggi_csv("file_name.csv")

#Scarica report html
st.report_dataset(il_mio_dataset")
#Salverà nella corrente un report html

#apri il tuo dataset sul web
st.apri_dataframe_nel_browser(il_mio_dataset)
#Ti consigliamo viviamente di provare questa funzione sul tuo set di dati
```

#
#
#

## _Step 3 ---_  **Modulo PreProcessing**

Con questo modulo potrai pulire, manipolare, standardizzare e scalare i tuoi dati
#
Gestire Nulli o Corrotti

```sh
from intelligenzaartificiale import dataset as dt
from intelligenzaartificiale import preprocessing as pp

il_mio_dataset = dt.leggi_csv("file_name.csv")

#rimuovere righe con valori nulli o corrotti
il_mio_dataset = pp.rimuovi_nan(il_mio_dataset)

#sostituire valori nulli o corrotti con il valore medio
il_mio_dataset["colonna"] = pp.sostituisci_nan_media(il_mio_dataset,"colonna")

#sostituire valori nulli o corrotti con il valore più frequente
il_mio_dataset["colonna"] = pp.sostituisci_nan_frequenti(il_mio_dataset,"colonna")

#rimuovi una colonna se i valori mancanti sono più di un valore passato
il_mio_dataset = pp.rimuovi_colonna_se_nan(il_mio_dataset,"colonna",500)
```
#
Gestire gli outliers
```sh
from intelligenzaartificiale import dataset as dt
from intelligenzaartificiale import preprocessing as pp

il_mio_dataset = dt.leggi_csv("file_name.csv")

#Rimuovere i valori outlier
il_mio_dataset["colonna"] = pp.rimuovi_outliers(il_mio_dataset,"colonna")

#Rimuovere i valori outlier e valori nulli
il_mio_dataset["colonna"] = pp.rimuovi_outliers_nan(il_mio_dataset,"colonna")

```
#
Gestire variabili testuali e categoriche
```sh
from intelligenzaartificiale import dataset as dt
from intelligenzaartificiale import preprocessing as pp

il_mio_dataset = dt.leggi_csv("file_name.csv")

#effettuare il labelencoding
il_mio_dataset["nuova_colonna"] = pp.label_encoding(il_mio_dataset,"colonna")

#effettuare il labelencoding con sklearn
il_mio_dataset["nuova_colonna"] = pp.label_encoding_sklearn(il_mio_dataset,"colonna")

#effettuare il one hot encoding
il_mio_dataset["nuova_colonna"] = pp.onehot_encoding(il_mio_dataset,"colonna")

#per rimuovere la vecchia colonna
il_mio_dataset = dt.rimuovi_colonna(il_mio_dataset, "colonna")

```
#
Normalizzare i dati
```sh
from intelligenzaartificiale import dataset as dt
from intelligenzaartificiale import preprocessing as pp

il_mio_dataset = dt.leggi_csv("file_name.csv")

#normalizza intero datatset
dataset_normalizzato = pp.normalizza(il_mio_dataset,"colonna")

#normalizza una specifica colonna
il_mio_dataset["colonna"] = pp.normalizza_colonne(il_mio_dataset,"colonna")

#standardizza intero datatset
dataset_normalizzato = pp.standardizza(il_mio_dataset,"colonna")

#standardizza una specifica colonna
il_mio_dataset["colonna"] = pp.standardizza_colonne(il_mio_dataset,"colonna")

# dividi i dati in test e train
X_train, X_test, y_train, y_test = pp.dividi_train_test(il_mio_dataset, "target", 0.25 )
```
#
#
#
## _Step 3.1 ---_  **Modulo Text-PreProcessing**

Con questo modulo potrai pulire, manipolare, standardizzare e scalare i tuoi dati Testuali
#
Pulizia di Base

```sh
from intelligenzaartificiale import dataset as dt
from intelligenzaartificiale import textpreprocessing as tpp

il_mio_dataset = dt.leggi_csv("file_name.csv")

#pulire l'intera colonna con una riga
il_mio_dataset["testo_email"] = tpp.pulisci_testo(il_mio_dataset,"testo_email")

#trasforma in minuscolo il tetso
il_mio_dataset["testo_email"] = tpp.trasforma_in_minuscolo(il_mio_dataset, "testo_email")

#rimuovi caratteri speciali e cifre !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~0123456789
il_mio_dataset["colonna"] = tpp.rimuovi_caratteri_speciali_e_cifre(il_mio_dataset,"colonna")

#rimuovi caratteri speciali !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~
il_mio_dataset["colonna"] = tpp.rimuovi_caratteri_speciali(il_mio_dataset,"colonna")

#rimuovi stopwords
il_mio_dataset["colonna"] = tpp.rimuovi_stopwords(il_mio_dataset,"colonna", "english")
```
#
Tokenizzazione e vettorizzazione del testo

```sh
from intelligenzaartificiale import dataset as dt
from intelligenzaartificiale import textpreprocessing as tpp

il_mio_dataset = dt.leggi_csv("file_name.csv")

#vettorizzare il testo (tfidf)
il_mio_dataset["testo_vet"] = tpp.vettorizza_testo(il_mio_dataset,"testo_email")
#oppure
il_mio_dataset["testo_vet"] = tpp.vettorizza_testo_sklearn(il_mio_dataset,"testo_email")

#analisi componenti principali
il_mio_dataset["pca"] = tpp.vettorizza_testo_sklearn(il_mio_dataset,"testo_vet")

#tokenizzare il testo 
il_mio_dataset["testo_tok"] = tpp.tokenizza_testo(il_mio_dataset,"testo_email")
#oppure
il_mio_dataset["testo_tok"] = tpp.tokenizza_testo_sklearn(il_mio_dataset,"testo_email")
```

#
Altre funzioni

```sh
from intelligenzaartificiale import dataset as dt
from intelligenzaartificiale import textpreprocessing as tpp

il_mio_dataset = dt.leggi_csv("file_name.csv")

#Bag of words
il_mio_dataset["wordbags"] = tpp.bag_of_words(il_mio_dataset,"testo_email","italian")

#genera grafico words cloud
crea_wordcloud(il_mio_dataset,"testo_email","english")

```
#
#
#
## _Step 4 ---_  **Modulo Apprendimento Automatico**

Con questo modulo potrai :
- Scoprire l'algoritmo più performante sui tuoi dati
- Implementare e allenare con una riga oltre 20 algoritmi
- Valutare, spiegare, salvare e caricare il tuo modello
- Fare previsioni su nuovi dati con il tuo modello
- & molto molto altro ancora


###### 🚧 La libreria è ancora in fase di SVILUPPO 🚧
#
#
## Licenza

MIT  
**© Copyright 2020-2022 Intelligenza Artificiale Italia!**

