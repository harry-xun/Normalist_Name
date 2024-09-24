function submitSearchForm() {
    var searchName = document.getElementById("searchName").value;
    var form = document.getElementById("searchForm");
    form.action = "/search/" + encodeURIComponent(searchName) + "/";
    form.submit();
}
