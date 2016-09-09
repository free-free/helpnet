$(function(){
    var geocoder;
    var geolocation;
    var wxLocationSupport = false;
    var address;

    function checkWXLocation(){
        wx.checkJsApi({
            jsApiList: ["getLocation"],
            success: function(res) {
                wxLocationSupport = res.checkResult["getLocation"];
                if(!wxLocationSupport){
                     amapLocationInit();
                }
            },
       });
    }

    function setLngLat(lng, lat){
        var longitude = document.getElementById("help_lng");
        var latitude = document.getElementById("help_lat");
        longitude.value = lng;
        latitude.value = lat; 
    }

    function setAddress(regeocode){
        
        simpleReg = regeocode.addressComponent.province+
            regeocode.addressComponent.city+
            regeocode.addressComponent.district+
            regeocode.addressComponent.township;
        simpleReg = new RegExp(simpleReg);
        address = regeocode.formattedAddress.replace(simpleReg,"");
        norepeatReg = /(.)(?=.*\1)/g;
        address = address.split("").reverse().join("").replace(norepeatReg,"");
        address = address.split("").reverse().join("");
    }

    function getLocation(){
        var addressInput = document.getElementById("help_address");
        if(addressInput.value == "" && !address){
            wxGetCurrentLocation(setLngLatAndAddr);
        }else{
            amapGetLocation();
        }
    }
    
/*
    function amapLocationInit(){
        AMap.plugin('AMap.Geolocation', function() {
            geolocation = new AMap.Geolocation({
                enableHighAccuracy: true,
                timeout: 10000,        
            });
            geolocation.getCurrentPosition();
            AMap.event.addListener(geolocation, 'complete', function(data){
                setLngLat( data.position.getLng(),data.position.getLat()); 
            });
            AMap.event.addListener(geolocation, 'error', function(){

            });      
       });
    }
*/
    function amapGetLocation(){
            var addressInput = document.getElementById("help_address");
            geocoder.getLocation(addressInput.value, function(status, result){
                if (status === 'complete' && result.info === 'OK') {
                    lng = result.geocodes[0].location.lng;
                    lat = result.geocodes[0].location.lat;
                    setLngLat(lng, lat);
                }else{
                }
            }); 
    }


    function amapGetAddress(lngLat, callback){
       geocoder.getAddress(lngLat, function(status, result) {
           if (status === 'complete' && result.info === 'OK') {
               callback && callback(result.regeocode);
           }
       });  
    }

    function amapInit(){
        AMap.plugin('AMap.Autocomplete',function(){
            var autoOptions = {input:"help_address"};
            autocomplete= new AMap.Autocomplete(autoOptions);
            AMap.event.addListener(autocomplete, "select", function(e){
                setLngLat(e.poi.location.lng, e.poi.location.lat);
            }); 
         });
        AMap.service('AMap.Geocoder',function(){
            geocoder = new AMap.Geocoder();
        });
    }

    function setLngLatAndAddr(lng, lat){
        setLngLat(lng, lat);
        amapGetAddress([lng, lat], setAddress);   
    }

    $("#help_address").blur(function(){
        getLocation();
        
    }).focus(function(){
       setTimeout(function(){
           offsetTop = parseInt($("#help_address").offset().top)-5;
           window.scrollTo(0,offsetTop);
       },800);
    });

    $("#ask_help_form").submit(function(){
        helpContent = document.getElementById("help_content");
        helpAddress = document.getElementById("help_address");
        helpPrice = document.getElementById("help_price");
        usercontact = document.getElementById("post_usercontact");
        helpLng = document.getElementById("help_lng");
        helpLat = document.getElementById("help_lat");
         
        if(helpContent.value==''||helpPrice.value==''|usercontact.value==''){
            $.toptip('求助信息不完整', 'error');
            return false;
        }
        if((helpAddress.value!="" &&(!helpLng.value || !helpLat.value))||(!address && !helpAddress.value)){
            $.toptip('获取地理位置失败', 'error');
            getLocation();
            return false;
        }
        if(!helpAddress.value && address){
            helpAddress.value = address;
        }
        
    });

    amapInit();
    wxLocationInit();
    wx.ready(function(){
        checkWXLocation();
        wxGetCurrentLocation(setLngLatAndAddr);
    });
})
