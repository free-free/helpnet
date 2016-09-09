function createDohelpView(parent, data){
    
    var container = document.createElement("div");
    container.id = "container";
    
    var head = document.createElement("div");
    var headImg = document.createElement("img");
    var username = document.createElement("span");
    head.className = "head"
    headImg.className = "head-img ";
    username.className = "username"
    head.appendChild(headImg);
    head.appendChild(username);
    container.appendChild(head);

    var body = document.createElement("div");

    var contentTag= document.createElement("span");
    var content = document.createElement("p");    
    contentTag.className = "tag content-tag";
    content.innerText = data.content;
    body.appendChild(contentTag);
    body.appendChild(content);
    
    var locationTag = document.createElement("span");
    var loc = document.createElement("p");
    var locIcon = document.createElement("i");
    var locValue = document.createElement("span");

    locationTag.className = "tag location-tag";
    loc.className = "location";
    locIcon.className = "fa fa-map-marker icon";
    locValue.className = "value";
    locValue.innerText = data.address;
    loc.apendChild(locIcon);
    loc.appendChild(locValue);
    
    body.appendChild(locationTag);
    body.appendChild(loc);

    var pUserontactTag= document.createElement("span");
    var pUsercontact = document.createElement("p");  
    var pUcIcon = document.createElement("i");
    var pUcValue = document.createElement("span");

    pUsercontactTag.className = "tag post-usercontact-tag";
    pUsercontact.className = "post-usercontact";
    pUcIcon.className = "fa fa-phone icon";
    pUcValue.className = "value";
    pUcValue.innerText = data.post_usercontact;
    
    pUsercontact.appendCHild(pUcIcon);
    pUsercontact.appendCHild(pUcValue);
    body.appendChild(pUsercontactTag);
    body.appendChild(pUsercontact);
    
    
    var price = document.createElement("p");  
    var priceTag = document.createElement("span");
    var priceVal = document.createElement("span");
    price.className = "price";
    priceTag.className = "tag";
    priceVal.calssName = "value";
    priceTag.innerText = "小费：";
    if(/^[0-9]+$/.test(data.price)){
        priceVal.innerText = "￥"+data.price;
    }else{
        priceVal.innerText = data.price;
    }
    price.appendChild(priceTag);
    price.appendChild(priceVal);
    body.appendChild(price);

    var form = document.createElement("form");
    var fromContainer = document.createElement("div");
    var doUsercontactMeans = document.createElement("select");

    helpInfo.className = "help_info";
    require.className = "";
}


$(function(){
   initP2r();
   $("#do-help #form").submit(function(){
       var doUserContact = document.getElementById("do-usercontact"); 
       var dohelpBtn = document.getElementById("submit-btn");
       if(!doUserContact.value){
           $.toptip("请留下你的联系方式",1000,"error");
           return false;
       }
   }); 
});
