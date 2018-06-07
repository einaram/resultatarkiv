

window.onload = function(evt){
    var needed = document.getElementsByClassName("selectitem");
    for(var i = 0; i < needed.length; i++)
    {
       needed[i].oninput=checkvalid;
       needed[i].onchange=checkvalid;
    }
    
}

checkvalid=function(evt){
    document.getElementById("downloaddata").disabled = true;
}
