window.onload = function(evt){
    document.getElementById("savedata").disabled=true;
    var needed = document.getElementsByClassName("needed");
    for(var i = 0; i < needed.length; i++)
    {
       needed[i].oninput=checkvalid;
    }
    
}

checkvalid=function(evt){
    enabled=true
    var needed = document.getElementsByClassName("needed");
    for(var i = 0; i < needed.length; i++)
    {
       enabled=enabled && needed[i].value>"";
    }
    document.getElementById("savedata").disabled = !enabled;
}

