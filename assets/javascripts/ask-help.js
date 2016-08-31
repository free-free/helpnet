$(function(){
    var geocoder;
    var geolocation;
    var wx_location_support = false;

    function wx_location_init(){
        url = "/resource/WXJSApiResource/get/";
        data = {"context":{"req_url":location.href+location.search}, "qrc":""};
        req_params = {
            'source_url': location.pathname,
            'data': JSON.stringify(data)
        };
        $.getJSON(url, req_params, function(json_data){
            wx.config({
                debug: false, 
                appId: json_data.resp[0].appid, 
                timestamp:json_data.resp[0].timestamp,
                nonceStr: json_data.resp[0].noncestr, 
                signature: json_data.resp[0].signature,
                jsApiList: json_data.resp[0].api_list 
            })
        });
    }

    function check_wx_location(){
        wx.checkJsApi({
            jsApiList: ["getLocation"], // 需要检测的JS接口列表，所有JS接口列表见附录2,
            success: function(res) {
                wx_location_support = res.checkResult["getLocation"];
                if(!wx_location_support){
                     amap_location_init();
                }
            },
       });
    }

    function set_lng_lat(lng, lat){
        var longitude = document.getElementById("help_lng");
        var latitude = document.getElementById("help_lat");
        longitude.value = lng;
        latitude.value = lat; 
    }

    function wx_get_current_location(){
            wx.getLocation({
                type: 'wgs84', 
                success: function (res) {
                    set_lng_lat(res.longitude, res.latitude)
                }
            });
    }

    function amap_location_init(){
        AMap.plugin('AMap.Geolocation', function() {
            geolocation = new AMap.Geolocation({
                enableHighAccuracy: true,
                timeout: 10000,        
            });
            geolocation.getCurrentPosition();
            AMap.event.addListener(geolocation, 'complete', function(data){
                set_lng_lat( data.position.getLng(),data.position.getLat()); 
            });
            AMap.event.addListener(geolocation, 'error', function(){

            });      
       });
    }

    function amap_get_location(){
            var address_input = document.getElementById("help_address");
            geocoder.getLocation(address_input.value, function(status, result){
                if (status === 'complete' && result.info === 'OK') {
                    lng = result.geocodes[0].location.lng;
                    lat = result.geocodes[0].location.lat;
                    set_lng_lat(lng, lat);
                }else{
                }
            }); 
    }

    function get_location(){
        var address_input = document.getElementById("help_address");
        if(address_input.value == ""){
            wx_get_current_location();
        }else{
            amap_get_location();
        }
    }

    function amap_get_address(){
        var help_address = document.getElementById("help_address");
        if(help_address.value == ""){
            var longitude = document.getElementById("help_lng");
            var latitude = document.getElementById("help_lat");
            lng = longitude.value ;
            lat = latitude.value ; 
            lnglat = [lng, lat];
            geocoder.getAddress(lnglat, function(status, result) {
                 if (status === 'complete' && result.info === 'OK') {
                     result.regeocode.formattedAddress;
                 }
            });
       }  
    }

    function amap_init(){
        AMap.plugin('AMap.Autocomplete',function(){
            var autoOptions = {input:"help_address"};
            autocomplete= new AMap.Autocomplete(autoOptions);
            AMap.event.addListener(autocomplete, "select", function(e){
                set_lng_lat(e.poi.location.lng, e.poi.location.lat);
            }); 
         });
        AMap.service('AMap.Geocoder',function(){
            geocoder = new AMap.Geocoder();
        });
    }

    amap_init();
    wx_location_init();
    wx.ready(function(){
        check_wx_location();
        wx_get_current_location();
    });

    $("#help_address").blur(function(){
        get_location();
    }).focus(function(){
       setTimeout(function(){
           offsetTop = parseInt($("#help_address").offset().top)-5;
           window.scrollTo(0,offsetTop);
       },800);
    });

    $("#ask_help_form").submit(function(){
        help_content = document.getElementById("help_content");
        help_price = document.getElementById("help_price");
        usercontact = document.getElementById("post_usercontact");
        help_address = document.getElementById("help_address");
        help_lng = document.getElementById("help_lng");
        help_lat = document.getElementById("help_lat");
        help_expiretime = document.getElementById("help_expiretime");
         
        if(help_content.value==''||help_price.value==''|usercontact.value==''){
            $.toptip('求助信息不完整', 'error');
            return false;
        }
        if(help_address.value!="" &&(help_lng.value == "" || help_lng.value == "undefined"  || help_lat.value=="" ||help_lat.value == "undefined")){
            $.toptip('获取地理位置失败', 'error');
            get_location();
            return false;
        }
        
    });
})
