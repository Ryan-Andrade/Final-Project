function myFunction() {
    const algorithm = document.getElementById("algorithms").value;
    const period = document.getElementById("period").value;
    const ticker = document.getElementById("search").value.toUpperCase();
    const dict_values = {algorithm, ticker, period};

    const s = JSON.stringify(dict_values); // Stringify converts a JavaScript object or value to a JSON string
    $.ajax({
        url:"/test",
        type:"POST",
        contentType: "application/json",
        data: JSON.stringify(s)});
}