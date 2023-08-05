var loc = [{ 
  "menu_icon_alt" : "Navigation icon",
  "search_icon_alt" : "Search icon",
  "search_placeholder" : "Search...",
  "docs_topics_title" : "Topics",
  "page_contents_title" : "Contents",
  "modal_search_title" : "Search within the documentation",
  "modal_search_placeholder" : "Use keywords...",
  "modal_search_btn" : "Search",
  "close_btn_img_alt" : "Close modal",
  "previous_label" : "Previous",
  "next_label" : "Next",
  "arrow_right_alt" : "Right arrow icon",
  "arrow_left_alt" : "Left arrow icon",
  "search_page_title" : "Search results",
  "search_page_input" : "Find in documentation",
  "search_page_no_results" : "I am sorry, but I am not able to find what you are looking for.",
  "page404_title" : "Ops... Page not found!",
  "page404_message" : "I'm sorry, but I can't find the page you are looking for."
}];

var lastUpdateDate = document.getElementById("last-update-date");
var copyRightDate = document.getElementById("copyright-date");
var splittedDate = lastUpdateDate.innerHTML.split(" ")[0];
var year = splittedDate.split("-")[0];
var month = splittedDate.split("-")[1];
var day = splittedDate.split("-")[2];

if (month == '01') {
  month = 'January';
} else if (month == '02') {
  month = 'February';
} else if (month == '03') {
  month = 'March';
} else if (month == '04') {
  month = 'April';
} else if (month == '05') {
  month = 'May';
} else if (month == '06') {
  month = 'June';
} else if (month == '07') {
  month = 'July';
} else if (month == '08') {
  month = 'August';
} else if (month == '09') {
  month = 'September';
} else if (month == '10') {
  month = 'October';
} else if (month == '11') {
  month = 'November';
} else if (month == '12') {
  month = 'December';
}

var newFormatDate = month + " " + day + ", " + year;

if (lastUpdateDate) lastUpdateDate.innerHTML = newFormatDate;
if (copyRightDate) copyRightDate.innerHTML = year;