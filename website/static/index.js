function deleteNote(noteId) {
    fetch('/delete-note', {
        method: "POST",
        body: JSON.stringify({ noteId: noteId }),
        }).then((_res) => {
        window.location.href = "/";
    });
}

function updateNote(noteId) {
    if (document.getElementById(noteId).contentEditable == "false") {
        document.getElementById(noteId).contentEditable = "true";
        document.getElementById(noteId).focus();
    } else if (document.getElementById(noteId).contentEditable == "true") {
        var data = document.getElementById(noteId).innerHTML;
        fetch('/update-note', {
            method: "POST",
            body: JSON.stringify({ noteId: noteId, noteData: data}),
            }).then((_res) => {
            window.location.href = "/";
        });
    }
}