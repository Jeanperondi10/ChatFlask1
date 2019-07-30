var intervalo, n;
window.onload = function() {
    n=1;
    if (document.getElementById("img-painel1") != null) {
        intervalo=setInterval(painel, 3000);
    }else{
        clearInterval(intervalo);
    }

    var objScrDiv = document.getElementById("scroll");
    objScrDiv.scrollTop = objScrDiv.scrollHeight;
};

var text=[];
    text[0]="Seja bem vindo a esta aplicação!";
    text[1]="É um prazer ter você aqui, conosco";
    text[2]="Socialize-se com toda a comunidade";
    text[3]="Queremos que aproveite o máximo";
    text[4]="Somos excelentes desenvolvedores";

function painel(){
    for (x=0;x<5;x++){
        document.getElementById("img-painel"+x).style="display:none";
        document.getElementById("img-painel"+x).style.visibility="hidden";

    }
    document.getElementById("img-painel"+n).style="display:block";
    document.getElementById("img-painel"+n).style.visibility="visible";




    document.getElementById("text-painel").innerHTML=text[n];
    n++;
    if(n==5){n=0}
}
function geraMaiusculo(n){
	return n.toUpperCase();
}

function togle() {
  var x = document.getElementById('blocklado');
  if (x.style.visibility === 'hidden') {
    x.style = 'display:block';
      x.style.visibility = 'visible';
  } else {
      x.style = 'display:none';
    x.style.visibility = 'hidden';
  }
}