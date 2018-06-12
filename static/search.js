var originalselection=true;

window.onload = function(evt){
    var needed = document.getElementsByClassName("selectitem");
    document.getElementById("downloaddata").disabled = true;
    for(var i = 0; i < needed.length; i++)
    {
       needed[i].oninput=turnoff;
       needed[i].onchange=turnoff;
    }
    needed = document.getElementsByClassName("projectcheck");
    for(var i = 0; i < needed.length; i++)
    {
       needed[i].oninput=checkvalid;
       needed[i].onchange=checkvalid;
    }
    
}

turnoff=function(evt){
    document.getElementById("downloaddata").disabled = true;
    originalselection=false;
}

checkvalid=function(evt){
    enabled=false;
    var needed = document.getElementsByClassName("projectcheck");
    for(var i = 0; i < needed.length; i++)
    {
       enabled = enabled || needed[i].checked;
    }
    enabled=enabled && originalselection;
    document.getElementById("downloaddata").disabled = !enabled;
}