var loc = [{ 
  "menu_icon_alt": "Icona bottone menu",
  "search_icon_alt": "Icona bottone ricerca",
  "search_placeholder": "Cerca...",
  "docs_topics_title": "Argomenti",
  "page_contents_title": "Contenuti",
  "modal_search_title": "Cerca all'interno della documentazione",
  "modal_search_placeholder": "Usa parole chiave...",
  "modal_search_btn": "Cerca",
  "close_btn_img_alt": "Chiudi modale",
  "previous_label": "Argomento precedente",
  "next_label": "Argomento successivo",
  "arrow_right_alt": "Icona freccia destra",
  "arrow_left_alt": "Icona freccia sinistra",
  "search_page_title": "Risultati della ricerca",
  "search_page_input": "Cerca nella documentazione",
  "search_page_no_results": "Mi dispiace, ma non riesco a trovare quello che stai cercando.",
  "page404_title": "Ops... Pagina non trovata!",
  "page404_message": "Mi dispiace, ma non riesco a trovare la pagina che stai cercando."
}];

var lastUpdateDate = document.getElementById("last-update-date");
var copyRightDate = document.getElementById("copyright-date");
var splittedDate = lastUpdateDate.innerHTML.split(" ")[0];
var year = splittedDate.split("-")[0];
var month = splittedDate.split("-")[1];
var day = splittedDate.split("-")[2];

if (month == '01') {
  month = 'Gennaio';
} else if (month == '02') {
  month = 'Febbraio';
} else if (month == '03') {
  month = 'Marzo';
} else if (month == '04') {
  month = 'Aprile';
} else if (month == '05') {
  month = 'Maggio';
} else if (month == '06') {
  month = 'Giugno';
} else if (month == '07') {
  month = 'Luglio';
} else if (month == '08') {
  month = 'Agosto';
} else if (month == '09') {
  month = 'Settembre';
} else if (month == '10') {
  month = 'Ottobre';
} else if (month == '11') {
  month = 'Novembre';
} else if (month == '12') {
  month = 'Dicembre';
}

var newFormatDate = day + " " + month + " " + year;

if (lastUpdateDate) lastUpdateDate.innerHTML = newFormatDate;
if (copyRightDate) copyRightDate.innerHTML = year;