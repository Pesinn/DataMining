// ============================================
// The id of the search bar is "main-search-input"
// ============================================

function append_to_search_bar(str) {
  var searchValue = document.getElementById("main-search-input").value

  if(!searchValue) {
    searchValue = searchValue + str    
  }
  else {
    lastLetter = searchValue.charAt(searchValue.length-1);
    if(lastLetter === ",") {
      searchValue = searchValue + str
    }
    else {
      searchValue = searchValue + ", " + str
    }
  }

  document.getElementById("main-search-input").value = searchValue;
}

