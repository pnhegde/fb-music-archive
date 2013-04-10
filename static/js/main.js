$("document").ready(function() {
    $.get("geturl/", {"num" : "100"})
    .success(function(data) {
        data = JSON.parse(data);
        if(data["success"] == "true") {
            // url fetched successfully
            for(var i = 0; i < data["num"]; i++) {
                var urlHtml = "<li class=\"url\" id=\"" + data['songs'][i]["id"] + "\" new=\"false\" mod=\"false\"> \
                <div class=\"url-textarea\" title=\"Open this link\" onclick=\"window.open('"+data['songs'][i]['url']+"')\">" + data["songs"][i]["title"] + "</div> \
                <div class=\"url-menu\" > submitted by - <strong>"+data["songs"][i]["name"]+"</strong></div> \
                </li>";
                $(".url-list").append(urlHtml);

            }
        }
        else {
            // Was not able to fetch url successfully
            showErrorMessage();
        }
    })
});