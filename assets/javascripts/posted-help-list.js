
function removePostedHelpView(helpid){
    var view = document.getElementById(helpid);
    view.parentNode.removeChild(view); 
    helpView = document.getElementsByClassName("help-view");
    if(helpView.length <= 2  ){
        postedHelpResource.getResource(createDynamicPostedHelpView);
    }
    
}


function createPostedHelpView(container, data){

/********************************************************************/
    var container = container;
    var view = document.createElement("div");
    var viewBox = document.createElement("div");
    
    view.className = "help-view";
    view.id = data.helpid;
    viewBox.className = "container";
    
/*****************************************************************/
    var headBox = document.createElement("div");
    var state = document.createElement("span"); 
    var dataOper = document.createElement("div");
    var ul =document.createElement("ul");
    var delBtnLi = document.createElement("li");
    var clear = document.createElement("div");
    var deleteBtn = document.createElement("a");
    
    deleteBtn.className = "del-btn weui_btn weui_btn_mini weui_btn_primary";
    deleteBtn.href="javscript:void(0);"
    deleteBtn.innerText = "删除";
    deleteBtn.addEventListener('click',function(){
        helpResource.delResource(
            data.helpid,
            removePostedHelpView,
            function(){$.toptip("删除失败", 1000, "error");}
        );
    },false);
    clear.className = "clear-fix";
    delBtnLi.appendChild(deleteBtn);
    ul.appendChild(delBtnLi);
    dataOper.className = "operation";
    dataOper.appendChild(ul);
  
    switch (data.state+""){
        case "0":
            state.className = "state font-green";
            state.innerText = "寻求帮助中...";
            break;
        case "1":
            state.className = "state font-green";
            state.innerText = "已得到帮助";
            break;
        case "2":
            state.className = "state font-red";
            state.innerText = "已过期";
            break; 
    }
     
    headBox.className = "head"
    headBox.appendChild(state);
    headBox.appendChild(dataOper);
    headBox.appendChild(clear);
    
    viewBox.appendChild(headBox);

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
    helpHead.className = "help-head";
    userInfo.className = "post-user";
    userHeadImg.className = "head-img";
    username.className = "name";
    price.className = "price";
    clear.className = "clear-fix";
    priceTag.className = "tag";
    priceVal.className = "value";

    userHeadImg.src = data.post_userheadimgurl;
    username.innerText = data.post_username;
    priceTag.innerText = "小费";
    if(/^[0-9]+$/.test(data.price)){
        priceVal.innerText = "￥"+data.price;
    }else{
        priceVal.innerText =  data.price;
    }

    userInfo.appendChild(userHeadImg);
    userInfo.appendChild(username);
    
    price.appendChild(priceTag);
    price.appendChild(priceVal);
    
    helpHead.appendChild(userInfo);
    helpHead.appendChild(price);
    helpHead.appendChild(clear);
    viewBox.appendChild(helpHead);
/*******************************************************************/
    var content = document.createElement("p");
    content.className = "content";
    content.innerText = data.content;
    viewBox.appendChild(content);
/********************************************************************/
    
    if((data.state+"") == "1")
    {
        var helpFooter = document.createElement("div");
        var doneUser = document.createElement("span");
        var name = document.createElement("span");
        var headImg = document.createElement("img");
        var note = document.createElement("span");
        var contact = document.createElement("div");
        var cMeans =  document.createElement("i");
        var cValue = document.createElement("span");
        clear = document.createElement("div");
   
        helpFooter.className = "help-footer";
        doneUser.className = "done-user";
        name.className = "name";
        headImg.className = "head-img";
        note.className = "note";
        contact.className = "contact";
        cValue.className = "value";
        clear.className = "clear-fix";
        switch (data.do_usercontact_means+""){
            case "1":
                cMeans.className = "fa fa-phone means";
                break;
            case "2":
                cMeans.className = "fa fa-weixin means";
                break;
            case "3":
                cMeans.className = "fa fa-qq means";
                break;
            default:
                cMeans.className = "fa fa-phone means";
                break;
        }

        name.innerText = data.do_username;
        headImg.src = data.do_userheadimgurl;
        note.innerText = "帮助了你";
        cValue.innerText = data.do_usercontact; 

        contact.appendChild(cMeans);
        contact.appendChild(cValue);

        doneUser.appendChild(headImg);
        doneUser.appendChild(name);
        doneUser.appendChild(note);
        doneUser.appendChild(contact);
 
        helpFooter.appendChild(doneUser);
        helpFooter.appendChild(clear);

        viewBox.appendChild(helpFooter);
    }
    view.appendChild(viewBox);
    container.appendChild(view);
}

function createDynamicPostedHelpView(data){
    var container = document.getElementById("container")
    var dtLen = data.resp_qrc.rcd_num;
    for(var i = 0; i < dtLen; i++){
        createPostedHelpView(container, data.resp[i]);
    }
}


$(function(){ 
   
    var container = document.getElementById("container")
    initP2r();
    createInfinitePreloader(container);
    postedHelpResource.getResource(createDynamicPostedHelpView);
    $(document.body).infinite(200).on("infinite", function(){
         postedHelpResource.getResource(createDynamicPostedHelpView);
    });
});
