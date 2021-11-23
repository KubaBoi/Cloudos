var table = document.querySelector("#tableId");

function getFiles() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            json = JSON.parse(this.responseText);
            table.innerHTML = "";
            addHeadRow();
            for (var i = 0; i < json.length; i++) {
                addRow(json[i]);
            } 
        }
    };
    xhttp.open("GET", "/getFiles", true);
    xhttp.send();
}

function addRow(data) {
    var name = data.filename;
    var size = data.size;
    var type = data.type;
    var date = formatDate(data.date);

    var row = document.createElement("tr");

    var cellName = document.createElement("td");
    var cellDate = document.createElement("td");
    var cellSize = document.createElement("td");
    var cellDownload = document.createElement("td");
    var cellRemove = document.createElement("td");

    cellName.innerHTML = "<a href=\"/files/" + name + "\">" + name + "</a>";
    cellDate.innerHTML = date;
    cellSize.innerHTML = size;
    cellDownload.innerHTML = "<a href=\"/files/" + name + "\" download=\"" + name + "\"><img src=\"/images/downloadIcon.png\" width=20 heigth=20></a>";
    cellRemove.innerHTML = "<img src=\"/images/removeIcon.png\" onclick=\"removeFile('" + name + "')\" width=20 heigth=20>";

    cellDownload.setAttribute("style", "width: 1%;");
    cellRemove.setAttribute("style", "width: 1%;");

    row.appendChild(cellName);
    row.appendChild(cellDate);
    row.appendChild(cellSize);
    row.appendChild(cellDownload);
    row.appendChild(cellRemove);

    table.appendChild(row);
}

function formatDate(unixTime) {
    var date = new Date(unixTime * 1000);

    var year = date.getFullYear();
    var month = date.getMonth();
    var day = date.getDay();
    var hours = date.getHours();
    var minutes = "0" + date.getMinutes();

    // Will display time in 10:30:23 format
    return  day + "." + month + "." + year + " " + hours + ':' + minutes.substr(-2);
}

function addHeadRow() {
    var row = document.createElement("tr");

    var cellName = document.createElement("th");
    var cellDate = document.createElement("th");
    var cellSize = document.createElement("th");

    cellName.innerHTML = "Název/Zobrazit soubor";
    cellDate.innerHTML = "Čas uploadu";
    cellSize.innerHTML = "Velikost";

    row.appendChild(cellName);
    row.appendChild(cellDate);
    row.appendChild(cellSize);

    table.appendChild(row);
}