/*
 * This JavaScript doesn't do anything. The file exists just to demonstrate
 * including static assets from the HTML in themes.
 */

const bodyEl = document.body;
const html = document.documentElement;

var viewportHeight;
var navChild;
var setIntervalVar;
var tableOfContents = document.getElementsByClassName("table-of-contents")[0];
var tableOfContentsContainer = document.querySelector(".columns-table-of-contents");
var searchResults = document.getElementById("mkdocs-search-results");
var page404 = document.getElementById("page404");
var mainSection = document.getElementsByClassName("main")[0];
var mainSectionHeight;
var headerSection = document.getElementsByClassName("header")[0];
var headerSectionHeight;

bodyEl.onload = function() {
  mainSectionHeight = mainSection.clientHeight;
  headerSectionHeight = headerSection.clientHeight;
  viewportHeight = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
  var navChild = document.getElementsByClassName("nav-child");
  for (var i = 0; i < navChild.length; i++) {
    var navChildItemActive = navChild[i].getElementsByClassName("active");
    if (navChildItemActive.length) {
        navChild[i].parentElement.classList.add("show-nav-child");
    }
  }
  if (page404) {
    bodyEl.classList.add("page-404");
  }
  if (searchResults) {
    bodyEl.classList.add("search-page");
  }
}

bodyEl.onresize = function() {
  viewportHeight = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
  mainSectionHeight = mainSection.clientHeight;
  headerSectionHeight = headerSection.clientHeight;
};

function toggleModalImg() {
  bodyEl.classList.toggle("show-modal-img");
}

function toggleModalSearch() {
  bodyEl.classList.toggle("show-modal-search");
  setTimeout(function() {
    document.querySelector("#modal-search").focus();
  }, 600);
}

function toggleDocsNav() {
  bodyEl.classList.toggle("show-docs-nav");
}

function toggleButton(e) {
  e = e || window.event;
  var targ = e.target || e.srcElement || e;
  if (targ.nodeType == 3) targ = targ.parentNode;
  var parent = targ.parentElement;
  var searchInput = parent.getElementsByTagName('input')[0].value;
  if (searchInput != "") {
      parent.getElementsByTagName('button')[0].removeAttribute("disabled");
  } else {
      parent.getElementsByTagName('button')[0].setAttribute("disabled", null);
  }
}

function toggleNavChild(e) {
  e = e || window.event;
  var targ = e.target || e.srcElement || e;
  if (targ.nodeType == 3) targ = targ.parentNode;
  var parent = targ.parentElement;
  parent.classList.toggle("show-nav-child");
}

window.addEventListener("scroll", onScroll);

var sticky = tableOfContentsContainer.offsetTop;
var stickyController = mainSection.offsetTop;

function onScroll() {
  var scrollValue = window.scrollY || window.scrollTop || document.getElementsByTagName("html")[0].scrollTop;
  if (mainSectionHeight >= (viewportHeight*2)) {
    if (scrollValue >= stickyController) {
      tableOfContentsContainer.classList.add("sticky");
    } else {
      tableOfContentsContainer.classList.remove("sticky");
    }
    if (scrollValue >= ((mainSectionHeight + headerSectionHeight)-viewportHeight)) {
      tableOfContentsContainer.classList.add("hide");
    } else {
      tableOfContentsContainer.classList.remove("hide");
    }
  }
}

var internalLinks = tableOfContents.getElementsByTagName("a");

for (var i = 0; i < internalLinks.length; i++) {
  internalLinks[i].onclick = function(e) {
    e = e || window.event;
    var targ = e.target || e.srcElement || e;
    if (targ.nodeType == 3) targ = targ.parentNode;
    var internalLinksHref = targ.getAttribute("href");
    var internalAnchorId = internalLinksHref.replace('#','');
    var titleEl = document.getElementById(internalAnchorId);
    titleEl.classList.add("highlight");
    setTimeout(function(){
      titleEl.classList.remove("highlight");;
    }, 1200);
  };
}
