window.onload = function() {
    escreveCampo();
  setInterval(function (){recarregar();}, 2000)
  var div=document.getElementById("scroll");
  window.scrollTo(0,div.offsetHeight);
};
function recarregar(){
    console.log("Gravado="+document.getElementById("body").value+"");
    localStorage.setItem("campo", document.getElementById("body").value+"");
    location.reload();
}
function escreveCampo(){
    togle('blocklado')
    console.log("Recuperado="+localStorage.getItem("campo")+"");
    document.getElementById("body").value=localStorage.getItem("campo")+"";
}
function limpar(){
    localStorage.setItem("campo", "");
    alert("Limpando="+localStorage.setItem("campo", ""))
}