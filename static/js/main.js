$("document").ready(function() {
    $.get("/geturl",{"num": "50"})
    .success(function(data) {
        data = JSON.parse(data);
        if(data["success"] == "true") {
            // url fetched successfully
            for(var i = 0; i < data["num"]; i++) {
                var urlHtml = "<li class=\"url\" id=\"" + data['songs'][i]["id"] + "\" new=\"false\" mod=\"false\"> \
                <div class=\"url-textarea\" title=\"Open this link\" onclick=\"window.open('"+data['songs'][i]['url']+"')\">" + data["songs"][i]["title"] + "</div> \
                <div class=\"url-menu\" > Category: <strong>"+ data['songs'][i]['category']+" </strong> submitted by - <strong>"+data["songs"][i]["name"]+"</strong></div> \
                <br/><img src='"+data['songs'][i]['thumbnail']+"' /></li>";
                $(".url-list").append(urlHtml);

            }
        }
        else {
            // Was not able to fetch url successfully
            showErrorMessage();
        }
    })

    // $.get("getCategory/")
    // .success(function(data) {
    //     data = JSON.parse(data);
    //     if(data["success"] == "true") {
    //         for(var i = 0; i < data["categories"].length; i++) {
    //             var urlHtml = "<li><a href= 'getComingSoon/'> "+data["categories"][i]+" </a></li>";
    //             $(".nav-list").append(urlHtml);

    //         }
    //     }
    //     else {
    //         // Was not able to fetch url successfully
    //         showErrorMessage();
    //     }
    // });
});
