
/********  start *****************************************/
function createDoneHelpEmptyNote(parent){
    var container = document.getElementById("donehelp-note");
    if(!container){
        container = document.createElement("div");
        var text = document.createElement("p");
        container.id = "donehelp-note";
        text.id = "text";
        text.innerText = "你还没有帮助";
        container.style = "padding-top:0.5rem;";
        text.style = "text-align:center;color:#b3b3b3";
        container.appendChild(text);
        parent.appendChild(container);
    }
}

function hideDoneHelpEmptyNote(){
    var noteContainer = document.getElementById("donehelp-note");
    if(noteContainer){
        noteContainer.style.display = "none";
    }
}
// end 


function createDoneHelpView(container, data){

/********************************************************************/
    var container = container;
    var view = document.createElement("div");
    var viewBox = document.createElement("div");
    
    view.className = "help-view";
    view.id = data.helpid;
    viewBox.className = "container";
/*****************************************************************/
    helpNoteText = document.createElement("span");
    helpNoteText.className = "note-text font-green";
    helpNoteText.innerText = "你帮助了Ta";
    viewBox.appendChild(helpNoteText); 
/****************************************************************/
    var  infoBox = document.createElement("div");
    var loc = document.createElement("span");
    var locIcon = document.createElement("i");
    var locVal = document.createElement("span");
    var posttime = document.createElement("span");
    var clear = document.createElement("div");
    clear.className = "clear-fix"; 
    infoBox.className = "info";
    loc.className = "location";
    locIcon.className = "fa fa-map-marker icon";
    locVal.className = "value";
    locVal.innerText = data.address,
    loc.appendChild(locIcon);
    loc.appendChild(locVal);
 
    posttime.className = "posttime";
    posttime.innerText = data.post_datetime;
    
    infoBox.appendChild(loc);
    infoBox.appendChild(posttime);
    infoBox.appendChild(clear);
    viewBox.appendChild(infoBox);
/****************************************************************/
    var helpHead = document.createElement("div");
    var userInfo = document.createElement("span");  
    var userHeadImg = document.createElement("img");
    var username = document.createElement("span");
    var price = document.createElement("span");
    var priceTag = document.createElement("span");
    var priceVal = document.createElement("span");
    var clear = document.createElement("div");

    var contact = document.createElement("span");
    var cIcon = document.createElement("i");
    var cValue = document.createElement("span");

    helpHead.className = "help-head";
    userInfo.className = "post-user";
    userHeadImg.className = "head-img";
    username.className = "name";
    price.className = "price";
    clear.className = "clear-fix";
    priceTag.className = "tag";
    priceVal.className = "value";
    contact.className = "contact";
    cValue.className = "value";
    switch(data.post_usercontact_means+""){
        case "1":
            cIcon.className = "fa fa-phone icon";
            break;
        case "2":
            cIcon.className = "fa fa-weixin icon";
            break;
        case "3":
            cIcon.className = "fa fa-qq icon";
            break;
        default:
            cIcon.className = "fa fa-phone icon";
            break;
    }
    userHeadImg.src = data.post_userheadimgurl;
    username.innerText = data.post_username;
    priceTag.innerText = "小费";
    if (/^[0-9]+$/.test(data.price)){
        priceVal.innerText =  "￥"+data.price;
    }else{
        priceVal.innerText =  data.price;
    }
    cValue.innerText = data.post_usercontact;

    userInfo.appendChild(userHeadImg);
    userInfo.appendChild(username);
    
    price.appendChild(priceTag);
    price.appendChild(priceVal);
   
    contact.appendChild(cIcon);
    contact.appendChild(cValue);
    helpHead.appendChild(userInfo);
    helpHead.appendChild(price);
    helpHead.appendChild(clear);
    helpHead.appendChild(contact);
    viewBox.appendChild(helpHead);
  
/*******************************************************************/
    var content = document.createElement("p");
    content.className = "content";
    content.innerText = data.content;
    viewBox.appendChild(content);
    
/********************************************************************/
    view.appendChild(viewBox);
    container.appendChild(view);
}


function checkDoneHelpEmpty(){
    var container = document.getElementById("container")
    var helpView = document.getElementsByClassName("help-view");
    if(helpView.length == 0){
        hideInfinitePreloader();
        createDoneHelpEmptyNote(container);
    }else{
	showInfinitePreloader();
        hideDoneHelpEmptyNote();
    }
}

function createDynamicDoneHelpView(data){
    var container = document.getElementById("container");
    var dtLen = data.resp_qrc.rcd_num;
    for(var i = 0; i < dtLen; i++){
        createDoneHelpView(container, data.resp[i]);
    }
    if(dtLen == 0){
        checkDoneHelpEmpty();
    }
}


$(function(){ 
   
    var container = document.getElementById("container")
    /* init pull to refresh component */
    initP2r();
    /* create infinite preloader component */
    createInfinitePreloader(container);
    /* load done help resource data */
    doneHelpResource.getResource(createDynamicDoneHelpView);
    /* bind event for infinite preloader */
    $(document.body).infinite(200).on("infinite", function(){
         doneHelpResource.getResource(createDynamicDoneHelpView);
    });
});
