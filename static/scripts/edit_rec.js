function submitEditForm() {
    document.getElementById("action").value = "edit";
    document.getElementById("bid").value = sessionStorage.getItem('buggy_id');
    //document.getElementById("new_buggy_form").submit();
    let x = document.getElementsByClassName("button");
    x[0].submit();
}
