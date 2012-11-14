function showErrorMessage() {
    $(".error-message").css({"left" : "0px"});
    setTimeout(function() {
        $(".error-message").css({"left" : "-600px"});  
    }, 3500)
}

$("document").ready(function() {
    // Hide delete and similar of new note
    $("li#xxx > .note-menu > .note-menu-item > .delete").css({"display" : "none"});
    $("li#xxx > .note-menu > .note-menu-item > .similar").css({"display" : "none"});

    // Fetch all (n) notes to display
    $.get("getnote/", {"num" : "25"})
    .success(function(data) {
        data = JSON.parse(data);
        if(data["success"] == "true") {
            // Note fetched successfully
            for(var i = 0; i < data["num"]; i++) {
                var noteHtml = "<li class=\"note\" id=\"" + data["notes"][i]["id"] + "\" new=\"false\" mod=\"false\"> \
                    <textarea class=\"note-textarea\" placeholder=\"Enter your note\">" + data["notes"][i]["note"] + "</textarea> \
                    <ul class=\"note-menu\"> \
                        <li class=\"note-menu-item\"><span class=\"save note-menu-item-text\">save</span></li> \
                        <li class=\"note-menu-item\"><span class=\"delete note-menu-item-text\">delete</span></li> \
                        <li class=\"note-menu-item\"><span class=\"similar note-menu-item-text\">similar</span></li> \
                    </ul> \
                </li>";
                $(".note-list").append(noteHtml);
            }
        }
        else {
            // Was not able to fetch note successfully
            showErrorMessage();
        }
    })
    .error(function() {
        showErrorMessage();
    });

    $(".save").click(function() {
        // Check if it actually has to be saved
        // that is add note or update note or do nothing
        var newAttr = $(this).attr("new");
        var modAttr = $(this).attr("mod");

        if(newAttr == "true" && modAttr == "true") {

            if($("this:first-child").val() > 0) {
                // It really has some content
                // Add new note
                $.get("addnote/", {"note" : encodeURIComponent($("this:first-child").val())})
                .success(function(data) {
                    data = JSON.parse(data);
                    if(data["success"] == "true") {
                        // Set the id of the note saved
                        $("#xxx").attr("id", data["id"]);
                        // Set the new and mod property
                        $("#" + data["id"]).attr("new", "false");
                        $("#" + data["id"]).attr("mod", "false");

                        // Enable delete and similar
                        $("#" + data["id"] + " > .note-menu > .note-menu-item > .delete").css({"display" : "inline"});
                        $("#" + data["id"] + " > .note-menu > .note-menu-item > .similar").css({"display" : "inline"});

                        // Create a new empty note
                        $(".note-list").prepend(" \
                            <li class=\"note\" id=\"xxx\" new=\"true\" mod=\"false\"> \
                            <textarea class=\"note-textarea\" placeholder=\"Enter your note\"></textarea> \
                            <ul class=\"note-menu\"> \
                                <li class=\"note-menu-item\"><span class=\"save note-menu-item-text\">save</span></li> \
                                <li class=\"note-menu-item\"><span class=\"delete note-menu-item-text\">delete</span></li> \
                                <li class=\"note-menu-item\"><span class=\"similar note-menu-item-text\">similar</span></li> \
                            </ul> \
                        </li>");
                    }
                    else {
                        showErrorMessage();
                    }
                })
                .error(function() {
                    showErrorMessage();
                });
            }
            else {
                // It does not have any content
                // but trying to save. So, set the mod to false
                $(this).attr("mod", "false");
            }
            
        }
        else if(newAttr == "false" && modAttr == "true") {
            if($("this:first-child").val() > 0) {
                // It really has some text. post it
                // Update the note
                $.get("updatenote/", {"note" : encodeURIComponent($("this:first-child").val()), "id" : $(this).attr("id")})
                .success(function(data) {
                    data = JSON.parse(data);
                    if(data["success"] == "true") {
                        // Set the new and mod property
                        $("#" + data["id"]).attr("new", "false");
                        $("#" + data["id"]).attr("mod", "false");

                        // Enable delete and similar
                        $("#" + data["id"] + " > .note-menu > .note-menu-item > .delete").css({"display" : "inline"});
                        $("#" + data["id"] + " > .note-menu > .note-menu-item > .similar").css({"display" : "inline"});
                    }
                    else {
                        showErrorMessage();
                    }
                })
                .error(function() {
                    showErrorMessage();
                });
            }
            else {
                // Old note's contents are just emptied and saved
                // So remove it from dom and send request to delete it

                // Remove from DOM
                $(this).remove();

                // Send request to remove
                $.get("removenote/", {"id" : $(this).attr("id")})
                .success(function(data) {
                    data = JSON.parse(data);
                    if(data["success"] == "true") {
                        // Remove successful. Do nothing
                    }
                    else {
                        showErrorMessage();
                    }
                })
                .error(function() {
                    showErrorMessage();
                });

            }
            
        }
        else if(newAttr == "true" && modAttr == "false") {
            // Do nothing
        }
        else if(newAttr == "false" && modAttr == "false") {
            // Do nothing
        }
        
    });

    $(".delete").click(function() {
        
    });

    $(".similar").click(function() {
        
    });
});