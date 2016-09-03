
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
            if(reg.test(data.help_price)){
                helpPriceNum.innerText = "￥"+data.help_price;
            }else{
                helpPriceNum.innerText = data.help_price;
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
            helpContent.innerText = data.help_content;
            helpListItemMain.appendChild(helpContent);
             
            var helpListItemFooter = document.createElement("div");
            var helpTimeBox = document.createElement("div");
            var helpTimeout = document.createElement("span");
            var clear = document.createElement("div");
            var helpPosttime = document.createElement("addr");
            var helpBtn = document.createElement("a");
            helpListItemFooter.className = "help_list_item_footer";
            helpTimeBox.className = "help_time_box";
            helpTimeout.className = "help_timeout help_time";
            helpTimeout.innerText = data.expiretime;
            helpPosttime.className = "timeago help_posttime help_time";
            helpPosttime.title = pt.toISOString();
            clear.className="clear-fix";
            helpBtn.className = "weui_btn weui_btn_primary";
            helpBtn.href = data.help_url;
            helpBtn.innerText = "去帮助Ta";
            helpTimeBox.appendChild(helpTimeout); 
            helpTimeBox.appendChild(helpPosttime);
            helpTimeBox.appendChild(clear);
            helpListItemFooter.appendChild(helpTimeBox);
            helpListItemFooter.appendChild(helpBtn);
           
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
            url = "/resource/HelpResource/get/";
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
