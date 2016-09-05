
        var loading = false;

        function init_timeago(){
           jQuery.timeago.settings.strings = {
                        prefixAgo: null,
                        prefixFromNow: "从现在开始",
                        suffixAgo: null,
                        suffixFromNow: null,
                        seconds: "刚刚",
                        minute: "1分钟之前",
                        minutes: "%d分钟之前",
                        hour: "1小时之前",
                        hours: "%d小时之前",
                        day: "1天之前",
                        days: "%d天之前",
                        month: "大约1个月之前",
                        months: "%d月之前",
                        year: "大约1年之前",
                        years: "%d年",
                        numbers: [],
                        wordSeparator: ""
            };
        }

        function create_help_item_ui(parent, data){
            pt = new Date(parseFloat(data.posttime)*1000);
            var helpListItem = document.createElement("div");
            var helpListItemContainer = document.createElement("div");
            helpListItem.className = "help_list_item center";
            helpListItemContainer.className = "help_list_item_container";

            var helpListItemHead = document.createElement("div");
            var helpPostUserHeadImg = document.createElement("img");
            var helpPostUserName = document.createElement("span");
            var helpPrice = document.createElement("span");
            var helpPriceNum = document.createElement("span");
            var helpPriceTag = document.createElement("span");
            helpListItemHead.className = "help_list_item_head";
            helpPostUserHeadImg.className = "help_post_user_head_img";
            helpPostUserName.className = "help_post_user_name"; 
            helpPrice.className = "help_price";
            helpPriceTag.className= "help_price_tag";
            helpPriceNum.className = "help_price_num";
            helpPriceTag.innerText = "小费  ";
            reg = /^[0-9]+$/;
            if(reg.test(data.price)){
                helpPriceNum.innerText = "￥"+data.price;
            }else{
                helpPriceNum.innerText = data.price;
            }
            helpPostUserHeadImg.src = data.post_userheadimgurl;
            helpPostUserName.innerText = data.post_username;
            helpPrice.appendChild(helpPriceTag);
            helpPrice.appendChild(helpPriceNum);
            helpListItemHead.appendChild(helpPostUserHeadImg);
            helpListItemHead.appendChild(helpPostUserName);
            helpListItemHead.appendChild(helpPrice);

            var helpListItemMain = document.createElement("div");
            var helpContent = document.createElement("p");
            helpListItemMain.className = "help_list_item_main";
            helpContent.className = "help_content";
            helpContent.innerText = data.content;
            helpListItemMain.appendChild(helpContent);
             
            var helpListItemFooter = document.createElement("div");
            var infoBox = document.createElement("div");
            var hLocation = document.createElement("span");
            var locationIcon = document.createElement("i");
            var locationValue = document.createElement("span");
            var posttime = document.createElement("addr");
            var clear = document.createElement("div");
            var btn = document.createElement("a");
            helpListItemFooter.className = "help_list_item_footer";
            hLocation.className = "location";
            locationIcon.className = "icon fa fa-map-marker"
            locationValue.className = "value";
            locationValue.innerText = data.address;
            posttime.className = "timeago posttime";
            posttime.title = pt.toISOString();
            clear.className="clear-fix";
            btn.className = "weui_btn weui_btn_primary";
            btn.href = data.url;
            btn.innerText = "去帮助Ta";
            hLocation.appendChild(locationIcon);
            hLocation.appendChild(locationValue);
            infoBox.appendChild(hLocation); 
            infoBox.appendChild(posttime);
            infoBox.appendChild(clear);
            helpListItemFooter.appendChild(infoBox);
            helpListItemFooter.appendChild(btn);
           
            helpListItemContainer.appendChild(helpListItemHead);
            helpListItemContainer.appendChild(helpListItemMain);
            helpListItemContainer.appendChild(helpListItemFooter);
            
            helpListItem.appendChild(helpListItemContainer);
            parent.appendChild(helpListItem);
            
        }

        function load_help_data_success(json_data)
        {
            var length = json_data.resp.length;
            var list = document.getElementById("help_list_container");
            for(var i = 0; i < length; i++)
            {
                create_help_item_ui(list, json_data.resp[i]);
                $(".timeago").timeago();
            }
          
        }

        function load_help_data()
        {
            loading = true;
            url = "/resource/UpdatesHelpResource/get/";
            data = {
                "context":"updates",
                "qrc":"",
            }
             
            req_params = { 
                "source_url":location.pathname,
                "data":JSON.stringify(data)
            };
            $.getJSON(url, req_params, function(json_data){
                load_help_data_success(json_data);
                loading = false;
            })
        }

        function init()
        {
	    var list = document.getElementById("help_list_container");
            init_timeago();
            init_p2r();
            create_infinite_preloader(list);
            $(document.body).infinite(200).on("infinite", function(){
                if(loading) return ;
                load_help_data();
            })
            load_help_data();
        }


$(function(){
    init();
});
