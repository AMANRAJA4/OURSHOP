function onlystring()
{
    var first_name = document.getElementById('first_name');
    var last_name = document.getElementById('last_name');
    var letters = /^[A-Za-z]+$/;
    if (first_name.match(letters) && last_name.match(letters))
    {
        return true;
    }
    else
    {
        alert("PLEASE ENTER VALID NAME.");
        return false;
    }
}
function onlynumber()
{
    var num = document.myform.mobile.value;
    if (isNaN(num))
    {
        alert("Please enter valid credentials.")
    }
    else{
        return true;
    }
}

setTimeout(TimeOut,5000)

function TimeOut()
{
    document.getElementById('timeout').style.display = "none"
}
