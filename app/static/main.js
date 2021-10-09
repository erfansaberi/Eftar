function checkTime(i) {
  if (i < 10) {
    i = "0" + i;
  }
  return i;
}

function startTime() {
  var today = new Date();
  var h = today.getHours();
  var m = today.getMinutes();
  var s = today.getSeconds();
  // add a zero in front of numbers<10
  m = checkTime(m);
  s = checkTime(s);
  document.getElementById("show_time").innerHTML = h + ":" + m + ":" + s;
  t = setTimeout(function () {
    startTime();
  }, 500);
}

function show_date(){
    let element = document.getElementById('show_date');

    switch(new Date().getDay()){
        case 0:{
            element.innerHTML = "یکشنبه";
            break;
        } 
            
        case 1:{
            element.innerHTML = "دوشنبه";
            break;
        }
        case 2:{
            element.innerHTML = "سه شنبه";
            break;
        } 
        case 3:{
            element.innerHTML = "چهارشنبه";
            break;
        } 
        case 4:{
            element.innerHTML = "پنجشنبه";
            break;
        } 
        case 5:{
            element.innerHTML = "جمعه";
            break;
        } 
        case 6:{
            element.innerHTML = "شنبه";
            break;
        } 
    }
    console.log(new Date().getDay());
    
}


function change_footer_text()
{
    let element = document.getElementById('footer_copy_right_msg'); 
    element.innerHTML = "@Amirmahdi_kaheh | https://github.com/erfansaberi";
}
function set_default_footer_text()
{
    let element = document.getElementById('footer_copy_right_msg'); 
    element.innerHTML = "Desigend By AMK with ❤ | Developed By Erfan Saberi";
} 
startTime();
show_date();



