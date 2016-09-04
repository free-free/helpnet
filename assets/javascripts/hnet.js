// init pull to refresh layer
function init_p2r(){
            $(".weui-pull-to-refresh-layer").show(); 
	    $(document.body).pullToRefresh();
	    $(document.body).on("pull-to-refresh", function() {
		setTimeout(function(){	
			$(document.body).pullToRefreshDone()
                        location.reload();
		},1000);
                
	    });
}
//文档高度


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

function getDocumentTop() {
	var scrollTop = 0,
		bodyScrollTop = 0,
		documentScrollTop = 0;
	if (document.body) {
		bodyScrollTop = document.body.scrollTop;
	}
	if (document.documentElement) {
		documentScrollTop = document.documentElement.scrollTop;
	}
	scrollTop = (bodyScrollTop - documentScrollTop > 0) ? bodyScrollTop : documentScrollTop;
	return scrollTop;
}

//可视窗口高度
function getWindowHeight() {
	var windowHeight = 0;
	if (document.compatMode == "CSS1Compat") {
		windowHeight = document.documentElement.clientHeight;
	} else {
		windowHeight = document.body.clientHeight;
	}
	return windowHeight;
}

//滚动条滚动高度
function getScrollHeight() {
	var scrollHeight = 0,
		bodyScrollHeight = 0,
		documentScrollHeight = 0;
	if (document.body) {
		bodyScrollHeight = document.body.scrollHeight;
	}
	if (document.documentElement) {
		documentScrollHeight = document.documentElement.scrollHeight;
	}
	scrollHeight = (bodyScrollHeight - documentScrollHeight > 0) ? bodyScrollHeight : documentScrollHeight;
	return scrollHeight;
}

function sendGetReq(url, qrc, context, callback){
    data = {"qrc":qrc, "context":context};
    req_params={
        "source_url":location.pathname,
        "data":JSON.stringify(data)
    }
    $.getJSON(url, req_params,function(json_data){callback(json_data);});
}
