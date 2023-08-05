let loc_obj = loc[0];

/* Elements to tranlate */
let menuIconAlt = document.querySelector('.tool-docs-navigation .tool-trigger img');
let searchIconAlt = document.querySelector('.tool-search .tool-trigger img');
let searchPlaceholder = document.querySelector('#side-menu-search');
let docsTopicTitle = document.querySelector('#docs-topics-title');
let pageContentsTitle = document.querySelector('#page-contents-title');
let modalSearchTitle = document.querySelector('#modal-search-title');
let modalSearchPlaceholder = document.querySelector('#modal-search');
let modalSearchBtn = document.querySelector('.modal-search button');
let closeBtnImgAlt = document.querySelectorAll('.close img');
let previousLabel = document.querySelector('.internal-nav-link-previous-label h6');
let nextLabel = document.querySelector('.internal-nav-link-next-label h6');
let arrowRightAlt = document.querySelector('.arrow-right img');
let arrowLeftAlt = document.querySelector('.arrow-left img');
let searchPageTitle = document.querySelector('h1#search');
let searchPageInput = document.querySelector('#mkdocs-search-query');
let fourZeroFourTitle = document.querySelector('h3#page404');
let fourZeroFourMessage = document.querySelector('.page404-message');

/* Apply localization */
if (menuIconAlt) menuIconAlt.alt = loc_obj.menu_icon_alt;
if (searchIconAlt) searchIconAlt.alt = loc_obj.search_icon_alt;
if (searchPlaceholder) searchPlaceholder.placeholder = loc_obj.search_placeholder;
if (docsTopicTitle) docsTopicTitle.innerHTML = loc_obj.docs_topics_title;
if (pageContentsTitle) pageContentsTitle.innerHTML = loc_obj.page_contents_title;
if (modalSearchTitle) modalSearchTitle.innerHTML = loc_obj.modal_search_title;
if (modalSearchPlaceholder) modalSearchPlaceholder.placeholder = loc_obj.modal_search_placeholder;
if (modalSearchBtn) modalSearchBtn.innerHTML = loc_obj.modal_search_btn;
if (closeBtnImgAlt) {
  for (var i = 0; i < closeBtnImgAlt.length; i++) {
    closeBtnImgAlt[i].alt = loc_obj.close_btn_img_alt;
  }
}
if (previousLabel) previousLabel.innerHTML = loc_obj.previous_label;
if (nextLabel) nextLabel.innerHTML = loc_obj.next_label;
if (arrowRightAlt) arrowRightAlt.alt = loc_obj.arrow_right_alt;
if (arrowLeftAlt) arrowLeftAlt.alt = loc_obj.arrow_left_alt;
if (searchPageTitle) searchPageTitle.innerHTML = loc_obj.search_page_title;
if (searchPageInput) searchPageInput.placeholder = loc_obj.search_page_input;
if (fourZeroFourTitle) fourZeroFourTitle.innerHTML = loc_obj.page404_title;
if (fourZeroFourMessage) fourZeroFourMessage.innerHTML = loc_obj.page404_message;

