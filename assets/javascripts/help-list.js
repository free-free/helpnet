
        var loading = false;
        /*
         data = {"post_userheadimgurl":"","post_username":"","helpreward":"",
                 "helpcontent":"","helpurl":"","helptimeout":""}

        */
        function create_infinite_preloader(after, data)
        {
            var parent = after.parentNode;
            var scroll = document.createElement("div");
            var preloader = document.createElement("div");
            scroll.className = "weui-infinite-scroll";
            preloader.className = "infinite-preloader";
            scroll.appendChild(preloader);
            scroll.innerHtml += "正在加载...";
            if(parent.lastChild == after)
            {
                parent.appendChild(scroll);
            }
            else
            {
                parent.insertBefore(scroll, after.nextSibling);
            }
        }

        function show_infinite_preloader()
        {
           var scroll = document.getElementsByClassName("weui-infinite-scroll");
           if(scroll.length > 0)
           {
               scroll[0].style.display = "block";
           }
        }

        function hide_infinite_preloader()
        {

           var scroll = document.getElementsByClassName("weui-infinite-scroll");
           if(scroll.length > 0)
           {
               scroll[0].style.display = "none";
           } 
        }

        function create_help_item_ui(parent, data){
            var helpListItem = document.createElement("div");
            var helpListItemContainer = document.createElement("div");
            helpListItem.className = "help_list_item center";
            helpListItemContainer.className = "help_list_item_container";

            var helpListItemHead = document.createElement("div");
            var helpPostUserHeadImg = document.createElement("img");
            var helpPostUserName = document.createElement("span");
            var helpReward = document.createElement("span");
            helpListItemHead.className = "help_list_item_head";
            helpPostUserHeadImg.className = "help_post_user_head_img";
            helpPostUserName.className = "help_post_user_name"; 
            helpReward.className = "help_reward";
            helpPostUserHeadImg.src = data.post_userheadimgurl;
            helpPostUserName.innerText = data.post_username;
            helpReward.innerText = data.helpreward;
            helpListItemHead.appendChild(helpPostUserHeadImg);
            helpListItemHead.appendChild(helpPostUserName);
            helpListItemHead.appendChild(helpReward);

            var helpListItemMain = document.createElement("div");
            var helpContent = document.createElement("p");
            helpListItemMain.className = "help_list_item_main";
            helpContent.className = "help_content";
            helpContent.innerText = data.helpcontent;
            helpListItemMain.appendChild(helpContent);
             
            var helpListItemFooter = document.createElement("div");
            var helpTimeout = document.createElement("span");
            var helpDetailBtn = document.createElement("a");
            helpListItemFooter.className = "help_list_item_footer";
            helpTimeout.className = "help_timeout";
            helpTimeout.innerText = data.helptimeout;
            helpDetailBtn.className = "weui_btn weui_btn_primary";
            helpDetailBtn.href = data.helpurl;
            helpDetailBtn.innerText = "帮助";
            helpListItemFooter.appendChild(helpTimeout);
            helpListItemFooter.appendChild(helpDetailBtn);
           
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
        function init_ui()
        {
	    var list = document.getElementById("help_list_container");
	    $(document.body).pullToRefresh();
	    $(document.body).on("pull-to-refresh", function() {
		setTimeout(function(){	
			$(document.body).pullToRefreshDone()
                        location.reload();
		},1000);
                
	    });
            create_infinite_preloader(list);
            $(document.body).infinite(200).on("infinite", function(){
                if(loading) return ;
                load_help_data();
            })
            load_help_data();
        }

