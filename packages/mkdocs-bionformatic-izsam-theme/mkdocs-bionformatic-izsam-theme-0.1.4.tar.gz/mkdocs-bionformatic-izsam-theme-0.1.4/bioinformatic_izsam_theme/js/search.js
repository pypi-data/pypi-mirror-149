/* Get indexed configurations parameters */
// s_config is declared in search_docs.js built with mkdocs-izsam-search
let config = s_config;
/* Get indexed docs */
// s_index is declared in search_docs.js built with mkdocs-izsam-search
let documents = s_index;
let idx;

var lang = s_config[0].lang[0];
var min_search_length = s_config[0].min_search_length;

function getSearchTermFromLocation() {
  var sPageURL = window.location.search.substring(1);
  var sURLVariables = sPageURL.split('&');
  for (var i = 0; i < sURLVariables.length; i++) {
    var sParameterName = sURLVariables[i].split('=');
    if (sParameterName[0] == 'q') {
      return decodeURIComponent(sParameterName[1].replace(/\+/g, '%20'));
    }
  }
}

function joinUrl (base, path) {
  if (path.substring(0, 1) === "/") {
    // path starts with `/`. Thus it is absolute.
    return path;
  }
  if (base.substring(base.length-1) === "/") {
    // base ends with `/`
    return base + path;
  }
  return base + "/" + path;
}

function formatResult (location, title, summary) {
  return '<article><h3><a href="' + joinUrl(base_url, location) + '">'+ title + '</a></h3><p class="location">' + location + '</p><p>' + summary +'</p></article>';
}

function displayResults (results) {
  var search_results = document.getElementById("mkdocs-search-results");
  while (search_results.firstChild) {
    search_results.removeChild(search_results.firstChild);
  }
  if (results.length > 0){
    // compare object and return an object of matched elements
    var filtered_results = documents.filter(function (o1) {
      return results.some(function (o2) {
        return o1.location === o2.ref; // return the ones with equal location and ref
      });
    });
    // now we need to reorder the keys with the scores given in results object
    // first I will make the same order of the two matching objects
    var ordered_results = results.sort(function(a, b) {
       return a.ref.toLowerCase().localeCompare(b.ref);
    });
    var ordered_filtered_results = filtered_results.sort(function(a, b) {
       return a.location.toLowerCase().localeCompare(b.location);
    });
    // now I will assign the score to the filtered results
    function isEqual(object1, object2) {
      return object1.location === object2.ref;
    }
    for (i=0; i < ordered_filtered_results.length; i++){
      if (isEqual( ordered_filtered_results, ordered_results)) {
         ordered_filtered_results[i].score = ordered_results[i].score;
       }
    }
    var sorted_results = ordered_filtered_results.sort(function(a, b) {
      return b.score - a.score;
    });
    for (var i=0; i < sorted_results.length; i++){
      var result = sorted_results[i];
      // control if is an internal anchor to avoid duplicate results with page link
      // if (result.location.toLowerCase().indexOf("#") > -1) {
        var summary = (result.text.substring(0, 200) + " [...]");
        var html = formatResult(result.location, result.title, summary);
        search_results.insertAdjacentHTML('beforeend', html);
      // }
    }
  } else {
    var noResultsText = search_results.getAttribute('data-no-results-text');
    if (!noResultsText) {
      //loc_obj is in theme-loc-**.js
      noResultsText = loc_obj.search_page_no_results;
    }
    search_results.insertAdjacentHTML('beforeend', '<p>' + noResultsText + '</p>');
  }
}

function doSearch () {
  var query = document.getElementById('mkdocs-search-query').value;
  if (query.length > min_search_length) {
    displayResults(idx.search(query));
  } else {
    // Clear results for short queries
    displayResults([]);
  }
}

function initSearch () {
  var search_input = document.getElementById('mkdocs-search-query');
  if (search_input) {
    search_input.addEventListener("keyup", doSearch);
  }
  var term = getSearchTermFromLocation();
  if (term) {
    search_input.value = term;
    doSearch();
  }
}

/* Start the magic */
if (documents) {
  idx = lunr(function () {
    if ((lang.length > 0) && (lang != 'en')) {
      this.use(lunr[lang])
    }
    this.ref('location')
    this.field('text')
    this.field('title')
    documents.forEach(function (doc) {
      this.add(doc)
    }, this)
  });
  allow_search = true;
  initSearch (allow_search);
  console.log(idx);
} else {
  initSearch (allow_search);
}
