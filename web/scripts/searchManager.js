var searchInp = document.querySelector("#search");
var oldJsonData = [];

window.setInterval(search, 1000);
function search() {
    if (searchInp.value != "") {
        jsonData = [];
        for (var i = 0; i < allData.length; i++) {
            if (allData[i].filename.startsWith(searchInp.value)) {
                jsonData.push(allData[i]);
            }
        }
    }
    else {
        jsonData = allData;
    }

    if (oldJsonData != jsonData) {
        sort();
        oldJsonData = jsonData;
    }
}