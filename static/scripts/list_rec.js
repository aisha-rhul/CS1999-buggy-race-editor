function submitEdit() {
    if(selected_id > 0) {
        document.getElementById("action").value = "edit";
        selected_action = "edit";
        document.getElementById("edit_list").submit();
    }  else
        alert("Select a record")
}

function submitDelete() {
    if(selected_id > 0) {
        if (confirm("Press OK to confirm!")) {
            document.getElementById("action").value = "delete"
            document.getElementById("edit_list").submit();
        } else {
    }
    }  else
        alert("Select a record")

}

function submitJSON() {
    if(selected_id > 0) {
        document.getElementById("action").value = "json";
        selected_action = "json";
        document.getElementById("edit_list").submit();
    }  else
        alert("Select a record")

}


