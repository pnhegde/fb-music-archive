function showErrorMessage() {
    $(".error-message").css({"left" : "0px"});
    setTimeout(function() {
        $(".error-message").css({"left" : "-600px"});  
    }, 3500)
}


function bindSaveClicked(sel) {
    $(sel).click(function() {
        // Check if it actually has to be saved
        // that is add note or update note or do nothing
        var newAttr = $(this).parent().parent().parent().attr("new");
        var modAttr = $(this).parent().parent().parent().attr("mod");

        console.log(newAttr)
        console.log(modAttr)

        if(newAttr == "true" && modAttr == "true") {

            if($(this).parent().parent().parent().children(".note > .note-textarea").val().length > 0) {
                // It really has some content
                // Add new note
                $.get("addnote/", {"note" : encodeURIComponent($(this).parent().parent().parent().children(".note > .note-textarea").val())})
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

                        bindSaveClicked("li#xxx > .note-menu > .note-menu-item > .save");
                        bindDeleteClicked("li#xxx > .note-menu > .note-menu-item > .delete");
                        bindSimilarClicked("li#xxx > .note-menu > .note-menu-item > .similar");
                        bindKeyUp("li#xxx > .note-textarea");

                        $("li#xxx > .note-menu > .note-menu-item > .delete").css({"display" : "none"});
                        $("li#xxx > .note-menu > .note-menu-item > .similar").css({"display" : "none"});


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
                $(this).parent().parent().parent().attr("mod", "false");
            }
            
        }
        else if(newAttr == "false" && modAttr == "true") {
            // console.log($(this).parent().parent().parent().children(".note > .note-textarea").val());
            if($(this).parent().parent().parent().children(".note > .note-textarea").val().length > 0) {
                // It really has some text. post it
                // Update the note
                $.get("updatenote/", {"note" : encodeURIComponent($(this).parent().parent().parent().children(".note > .note-textarea").val()), "id" : $(this).parent().parent().parent().attr("id")})
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
                $(this).parent().parent().parent().remove();

                // Send request to remove
                $.get("deletenote/", {"id" : $(this).parent().parent().parent().attr("id")})
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
}


function bindDeleteClicked(sel) {
    $(sel).click(function() {
        // Remove from DOM
        $(this).parent().parent().parent().remove();

        // Send request to remove
        $.get("deletenote/", {"id" : $(this).parent().parent().parent().attr("id")})
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
    });
}


function bindSimilarClicked(sel) {
    $(sel).click(function() {
        // Fetch the id and note contents of the clicked note
        var id = $(this).parent().parent().parent().attr("id");
        var note = $(this).parent().parent().parent().children(".note > .note-textarea").val();

        // Clear the DOM
        $(".note-list").html("");

        // Create unique note
        var noteHtml = "<li class=\"note\" id=\"" + id + "\" new=\"false\" mod=\"false\"> \
                    <textarea class=\"note-textarea\" placeholder=\"Enter your note\">" + note + "</textarea> \
                    <ul class=\"note-menu\"> \
                        <li class=\"note-menu-item\"><span class=\"save note-menu-item-text\">save</span></li> \
                        <li class=\"note-menu-item\"><span class=\"delete note-menu-item-text\">delete</span></li> \
                        <li class=\"note-menu-item\"><span class=\"similar note-menu-item-text\">similar</span></li> \
                    </ul> \
                </li>";
        $(".note-list").append(noteHtml);

        // Binding event handlers
        bindSaveClicked("li#" + id + " > .note-menu > .note-menu-item > .save");
        bindDeleteClicked("li#" + id + " > .note-menu > .note-menu-item > .delete");
        bindSimilarClicked("li#" + id + " > .note-menu > .note-menu-item > .similar");
        bindKeyUp("li#" + id + " > .note-textarea");

        // Set some style to make it unique
        $("#" + id).css({"background-color" : "#DDEEFF"});
        $("#" + id).children(".note > .note-textarea").css({"background-color" : "#DDEEFF"});

        // Send request for similar notes
        $.get("similar/", {"id" : id})
        .success(function(data) {
            // Got the response successfully!
            data = JSON.parse(data);
            if(data["success"] == "true") {
                // success!
                for(var i = 0; i < data["num"]; i++) {
                    var noteHtml = "<li class=\"note\" id=\"" + data["notes"][i]["id"] + "\" new=\"false\" mod=\"false\"> \
                    <div title=\"Similarity Value\" class=\"corner\"><span class=\"corner-text\">" + Math.round(parseFloat(data["notes"][i]["similarity"]) * 100)/100 + "</span></div> \
                    <textarea class=\"note-textarea\" placeholder=\"Enter your note\">" + data["notes"][i]["note"] + "</textarea> \
                    <ul class=\"note-menu\"> \
                        <li class=\"note-menu-item\"><span class=\"save note-menu-item-text\">save</span></li> \
                        <li class=\"note-menu-item\"><span class=\"delete note-menu-item-text\">delete</span></li> \
                        <li class=\"note-menu-item\"><span class=\"similar note-menu-item-text\">similar</span></li> \
                    </ul> \
                </li>";
                    $(".note-list").append(noteHtml);

                    // Current note loaded! bind the event handlers now!
                    bindSaveClicked("li#" + data["notes"][i]["id"] + " > .note-menu > .note-menu-item > .save");
                    bindDeleteClicked("li#" + data["notes"][i]["id"] + " > .note-menu > .note-menu-item > .delete");
                    bindSimilarClicked("li#" + data["notes"][i]["id"] + " > .note-menu > .note-menu-item > .similar");
                    bindKeyUp("li#" + data["notes"][i]["id"] + " > .note-textarea");
                }

            }
            else {
                // something is wrong
                showErrorMessage();
            }

            //Show the back button
            $(".back-button").css({"left" : "-25px"});

        })
        .error(function() {
            showErrorMessage();
        });

    });
}

function bindKeyUp(sel) {
    $(sel).keyup(function() {
        // As user has typed something, setting modified as true!
        $(this).parent().attr("mod", "true");
    });
}

$("document").ready(function() {
    // Hide delete and similar of new note
    $("li#xxx > .note-menu > .note-menu-item > .delete").css({"display" : "none"});
    $("li#xxx > .note-menu > .note-menu-item > .similar").css({"display" : "none"});

    // Binding event handlers
    bindSaveClicked("li#xxx > .note-menu > .note-menu-item > .save");
    bindDeleteClicked("li#xxx > .note-menu > .note-menu-item > .delete");
    bindSimilarClicked("li#xxx > .note-menu > .note-menu-item > .similar");
    bindKeyUp("li#xxx > .note-textarea");

    // Fetch all (n) notes to display
    $.get("getnote/", {"num" : "100"})
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

                // Current note loaded! bind the event handlers now!
                bindSaveClicked("li#" + data["notes"][i]["id"] + " > .note-menu > .note-menu-item > .save");
                bindDeleteClicked("li#" + data["notes"][i]["id"] + " > .note-menu > .note-menu-item > .delete");
                bindSimilarClicked("li#" + data["notes"][i]["id"] + " > .note-menu > .note-menu-item > .similar");
                bindKeyUp("li#" + data["notes"][i]["id"] + " > .note-textarea");
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

    $(".search-query").keydown(function(e) {
        if(e.keyCode == 13) {
            // Enter key was pressed. initiate search!
            if($(this).val().length > 0) {
                // Something is there in the search bar
                $.get("/search/", {"q" : encodeURIComponent($(this).val())})
                .success(function(data) {
                    //results has arrived successfully
                    data = JSON.parse(data);

                    if(data["success"] == "true") {
                        $(".note-list").html("");

                        if(data["num"] > 0) {
                            // more than 0 results

                            for(var i = 0; i < data["num"]; i++) {
                            var noteHtml = "<li class=\"note\" id=\"" + data["notes"][i]["id"] + "\" new=\"false\" mod=\"false\"> \
                            <div title=\"Relevance Score\" class=\"corner\"><span class=\"corner-text\">" + Math.round(parseFloat(data["notes"][i]["score"]) * 100)/100 + "</span></div> \
                            <textarea class=\"note-textarea\" placeholder=\"Enter your note\">" + data["notes"][i]["note"] + "</textarea> \
                            <ul class=\"note-menu\"> \
                                <li class=\"note-menu-item\"><span class=\"save note-menu-item-text\">save</span></li> \
                                <li class=\"note-menu-item\"><span class=\"delete note-menu-item-text\">delete</span></li> \
                                <li class=\"note-menu-item\"><span class=\"similar note-menu-item-text\">similar</span></li> \
                            </ul> \
                        </li>";
                            $(".note-list").append(noteHtml);

                            // Current note loaded! bind the event handlers now!
                            bindSaveClicked("li#" + data["notes"][i]["id"] + " > .note-menu > .note-menu-item > .save");
                            bindDeleteClicked("li#" + data["notes"][i]["id"] + " > .note-menu > .note-menu-item > .delete");
                            bindSimilarClicked("li#" + data["notes"][i]["id"] + " > .note-menu > .note-menu-item > .similar");
                            bindKeyUp("li#" + data["notes"][i]["id"] + " > .note-textarea");
                            }
                        }
                        else {
                            noResults = "<span class=\"no-result\">Sorry! No results!</span>";
                            $(".note-list").html(noResults);
                        }

                        // Display the back button 
                        // $(".back-button").css({"left" : "-25px"});
                    }
                    else {
                        showErrorMessage();
                    }

                    //Show the back button
                    $(".back-button").css({"left" : "-25px"});
                })
                .error(function() {
                    showErrorMessage();
                });
            }
            else {
                // Return pressed but search bar is empty.
                // So display all the notes

                // But first clear current results
                $(".note-list").html("");

                // Fetch all (n) notes to display
                $.get("getnote/", {"num" : "100"})
                .success(function(data) {
                    data = JSON.parse(data);
                    if(data["success"] == "true") {
                        // Note fetched successfully

                        
                        if(data["num"] > 0) {
                            // If there are notes
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

                                // Current note loaded! bind the event handlers now!
                                bindSaveClicked("li#" + data["notes"][i]["id"] + " > .note-menu > .note-menu-item > .save");
                                bindDeleteClicked("li#" + data["notes"][i]["id"] + " > .note-menu > .note-menu-item > .delete");
                                bindSimilarClicked("li#" + data["notes"][i]["id"] + " > .note-menu > .note-menu-item > .similar");
                                bindKeyUp("li#" + data["notes"][i]["id"] + " > .note-textarea");
                            }
                        }
                        else {
                            // No notes to diaplay
                            noResults = "<span class=\"no-result\">Sorry! No notes to display!</span>";
                            $(".note-list").html(noResults);

                        }
                        

                        
                        
                    }
                    else {
                        // Was not able to fetch note successfully
                        showErrorMessage();
                    }

                    //Show the back button
                    $(".back-button").css({"left" : "-25px"});
                })
                .error(function() {
                    showErrorMessage();
                });
            }
            
        }
    });

    $(".back-button").click(function() {
        //Hide the back button
        $(".back-button").css({"left" : "-110px"});

        $(".note-list").html("");
        // Display the home area with exisitng notes + create new note option
        var noteHtml = "<li class=\"note\" id=\"xxx\" new=\"true\" mod=\"false\"> \
                        <textarea class=\"note-textarea\" placeholder=\"Enter your note\"></textarea> \
                        <ul class=\"note-menu\"> \
                            <li class=\"note-menu-item\"><span class=\"save note-menu-item-text\">save</span></li> \
                            <li class=\"note-menu-item\"><span class=\"delete note-menu-item-text\">delete</span></li> \
                            <li class=\"note-menu-item\"><span class=\"similar note-menu-item-text\">similar</span></li> \
                        </ul> \
                    </li>";
        $(".note-list").append(noteHtml);
        // Hide delete and similar of new note
        $("li#xxx > .note-menu > .note-menu-item > .delete").css({"display" : "none"});
        $("li#xxx > .note-menu > .note-menu-item > .similar").css({"display" : "none"});

        // Binding event handlers
        bindSaveClicked("li#xxx > .note-menu > .note-menu-item > .save");
        bindDeleteClicked("li#xxx > .note-menu > .note-menu-item > .delete");
        bindSimilarClicked("li#xxx > .note-menu > .note-menu-item > .similar");
        bindKeyUp("li#xxx > .note-textarea");

        // Fetch all (n) notes to display
        $.get("getnote/", {"num" : "100"})
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

                    // Current note loaded! bind the event handlers now!
                    bindSaveClicked("li#" + data["notes"][i]["id"] + " > .note-menu > .note-menu-item > .save");
                    bindDeleteClicked("li#" + data["notes"][i]["id"] + " > .note-menu > .note-menu-item > .delete");
                    bindSimilarClicked("li#" + data["notes"][i]["id"] + " > .note-menu > .note-menu-item > .similar");
                    bindKeyUp("li#" + data["notes"][i]["id"] + " > .note-textarea");
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
    });
    
    
    

    
});