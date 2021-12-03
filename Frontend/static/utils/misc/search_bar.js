// ============================================
// The id of the search bar is "main-search-input"
// ============================================

var search_id = "main-search-input";

function remove_from_search_bar(str) {
  var searchString = document.getElementById(search_id).value;
  if(str && str.length > 0) {
    var search_array = splitSearchToArray(searchString, str)
    var searchString = searchArrayToSearchString(search_array)
    document.getElementById(search_id).value = searchString;
  }
}

function searchArrayToSearchString(searchArray) {
  searchString = ""
  for (let i = 0; i < searchArray.length; i++) {
    for (let a = 0; a < searchArray[i].length; a++) {
      searchString = searchString + ", " + searchArray[i][a];
    }

    // To make sure we don't add "|" in last loop
    if(i < searchArray.length-1) {
      searchString = searchString + "|";
    }
  }

  // Make sure there are no trailing commas
  return searchString.replace(/(^[,\s]+)|([,\s]+$)/g, '');
}

function splitSearchToArray(searchString, str) {
  var final_search = []

  if(str && str.length > 0) {
    //var searchValue = document.getElementById(search_id).value;
    var groups = searchString.split("|");

    for (let i = 0; i < groups.length; i++) {
      var searchTerms = groups[i].split(",")
      var singleSearch = [];

      for (let a = 0; a < searchTerms.length; a++) {
        trimmedTerm = searchTerms[a].trim();
        
        if(trimmedTerm !== str && trimmedTerm.length > 0) {
          singleSearch.push(searchTerms[a].trim())
        }
      }

      final_search.push(singleSearch);
    }
  }
  return final_search;
}

function append_to_search_bar(str) {
  var searchValue = document.getElementById(search_id).value

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

  document.getElementById(search_id).value = searchValue;
}

