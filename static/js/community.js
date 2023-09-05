/*
Created: 09/05/2023
Created by: Andrew Roney

Last Modified: 09/05/2023
Modified by: Andrew Roney
*/


$(document).ready(function() {

    // Show the new post form when the button is clicked
    $("#newPostButton").click(function() {
        $("#newPostFormDiv").show(); // Toggle the display of the form
    });

    $("#newPostForm").submit(function(event) {
        event.preventDefault();  // Prevent the form from submitting via the browser
        var csrfToken = $("input[name=csrfmiddlewaretoken]").val();
        var title = $("#postTitle").val().trim();
        var content = $("#postContent").val().trim();

        // Validate form fields
        if (title === "" || content === "") {
            alert("Please fill out all fields.");
            return;
        }

        // Send AJAX request to create new post
        $.ajax({
            url: '/community/',
            type: 'POST',
            headers: {'X-CSRFToken': csrfToken},
            data: {
                'title': title,
                'content': content
            },
            success: function(response) {
                if (response.status === 'success') {
                    // Create new post element
                    var newPost = '<div class="single_post">';
                    newPost += '<h4>' + response.title + '</h4>';
                    newPost += '<p>' + response.content + '</p>';
                    newPost += '</div>';
            
                    // Append new post to a designated area (e.g., a div with the ID "posts")
                    $('#posts').append(newPost);
            
                    // Clear the form fields
                    $('#postTitle').val('');
                    $('#postContent').val('');
            
                    alert("New post created!");
                } else {
                    alert("An error occurred. Could not create post.");
                }
            },
            error: function(response) {
                // Handle error
                alert("An error occurred. Could not create post.");
            }
        });
    });
});