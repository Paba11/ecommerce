# ecommerce
PPM Django project, eCommerce.
Paolo Sbarzagli

Il progetto consiste in un eCommerce con varie funzionalità, elencate di seguito.

È possibile accedere ed effettuare azioni sull'eCommerce sia con un profilo sia in assenza di esso. 
Infatti grazie alla presenza di cookies il browser terrà traccia di tutte le azioni (aggiunte/rimozioni dal carrello ed ordini) effettuate anche dagli utenti non loggati, consentendo loro di mantenere i dati del carrello anche a seguito di refresh.

È possibile registrarsi al sito compilando un form. Nel caso in cui un utente abbia effettuato acquisti prima di registrarsi, questi verranno direttamente collegati al nuovo profilo creato (nel caso in cui la mail del profilo corrisponda con la stessa dei precedenti acquisti).

Distingue due tipologie di prodotto:
- Digitale --> non richiede indirizzo di spedizione.
- Fisico --> Richiede indirizzo di spedizione.

Le principali funzionalità dell'eCommerce sono:

NAVBAR:
- Responsive con alcune semplici animazioni.
- Permette di navigare tra le varie pagine.
- Consente di accedere a Login, Logout e al form di registrazione

PAGINA PRODUCTS:
- Visualizzazzione completa degli oggetti con brevi info.
- Filtro per nome degli oggetti tramite la barra di ricerca posta in alto (premendo invio o il tasto search).
- Refresh del filtro sui prodotti tramite il tasto refresh.
- Possibilità di accedere ai dettagli dell'oggetto.
- Possibilità di aggiungere i prodotti al carrello.

PAGINA CARRELLO:
- Tramite il tasto Back To Shop ritorna alla pagina Products
- Tramite l'utilizzo delle due frecce consente di aumentare o diminuire la quantità dei prodotti salvati nel carrello.
- Rimozione di un prodotto portando la quantità a zero.
- Tramite il tasto Checkout naviga alla pagina di pagamento.

PAGINA CHECKOUT:
- Iserimento nome ed email (se l'utente non è loggato).
- Se si acquista un prodotto fisico inserimento dei dati di spedizione.
- Tramite il pulsante Make Payment l'ordine viene effettuato.

Per consentire il funzionamento corretto del sito si deve abilitare l'utilizzo dei cookies
