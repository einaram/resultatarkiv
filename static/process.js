
var fatalerrors=false;

window.onload = function(evt){
    var warns = document.getElementsByClassName("warncheck");
    for(var i = 0; i < warns.length; i++)
    {
       warns[i].onclick=checkwarn;
    }
    warnings=!!document.getElementById("Warningheader");
    fatalerrors=!!document.getElementById("Errorheader")
    if (warnings || fatalerrors){
        document.getElementById("importdata").disabled = true;
    }
}

checkwarn=function(evt){
    enabled=true
    var warns = document.getElementsByClassName("warncheck");
    for(var i = 0; i < warns.length; i++)
    {
       enabled=enabled && warns[i].checked
    }
    document.getElementById("importdata").disabled = !enabled || fatalerrors;
}