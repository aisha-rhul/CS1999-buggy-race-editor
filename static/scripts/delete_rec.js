function confirmChoice() {
    if(selected_id > 0) {
        if (confirm("Are you sure?")) {
            alert("You pressed OK!");
        } else {
            alert("You pressed Cancel!");
    }
    }  else
        alert("Select a record")

}