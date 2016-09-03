
function load_create_dohelp_data(){
}
function check_mobile_number(target){

}

function create_dohelp_ui(parent, data){
    
    var doHelpContainer = document.createElement("div");
    doHelpContainer.className = "do_help_container";
    
    var doHelpHead = document.createElement("div");
    var postUserHeadImg = document.createElement("img");
    var postUserName = document.createElement("span");
    doHelpHead.className = "do_help_head"
    postUserHeadImg.className = "post_user_head_img user_head_img";
    postUserName.className = "post_username user_name"
    doHelpHead.appendChild(postUserHeadImg);
    doHelpHead.appendChild(postUserName);
    

    var doHelpBody = document.createElement("div");
    var helpContentTag= document.createElement("span");
    var helContent = document.createElement("p");    
    var postUserContactTag= document.createElement("span");
    var postUserContact = document.createElement("p");    
    var helpPrice = document.createElement("p");    
    var doHelpForm = document.createElement("form");
    var doHelpFromContainer = document.createElement("div");
    var doUserContactMeans = document.createElement("select");

    helpInfo.className = "help_info";
    require.className = "";
}


$(function(){
   init_p2r();
   $("#do_help_form").submit(function(){
       var doUserContact = document.getElementById("do_usercontact"); 
       var dohelpBtn = document.getElementById("dohelp_btn");
       if(doUserContact.value == ""||doUserContact.value== "undefined"){
           $.toptip("请留下你的联系方式","error");
           return false;
       }
   }); 
});
