postedHelpResource = {
    'get_url':"/resource/PostedHelpResource/get/",
    'resLoadFailedCnt':0,
    'lastHelpPt':0.0,
    'resLoading':false,
    'qrc':"",
    'context':"",
    'getResource':function(callback){
         if(this.resLoading) return ;
         if(this.resLoadFailedCnt >= 3) return ;
         this.resLoading = true;
         this.context = {"last_help_pt":this.lastHelpPt};
         this.qrc = {"rcd_num":6}
         that = this;
         sendResourceGetReq(this.get_url, this.qrc, this.context, function(data){
             if(data.resp_qrc.rcd_num == 0){
                 that.resLoadFailedCnt += 1;
             }else{
                 that.lastHelpPt = data.resp_qrc['last_help_pt']; 
             }
             callback && callback(data);          
             that.resLoading = false;
         });
     }

}

doneHelpResource = {
    'get_url':'/resource/DoneHelpResource/get/',
    'resLoadFailedCnt':0,
    'lastHelpPt':0.0,
    'resLoading':false,
    'qrc':'',
    'context':'',
    'getResource':function(callback){
        if(this.resLoading) return;
        if(this.resLoadFailedCnt >= 3) return;
        this.resLoading = true;
        this.context = {'last_help_pt':this.lastHelpPt};
        this.qrc = {"rcd_num":6};
        that = this;
        sendResourceGetReq(this.get_url, this.qrc, this.context, function(data){
            if(data.resp_qrc.rcd_num == 0){
                that.resLoadFailedCnt +=1;
            }else{
                that.lastHelpPt = data.resp_qrc['last_help_pt'];
            }
            callback && callback(data);
            that.resLoading = false;
        });
    }

}
helpResource = {
    'del_url':"/resource/HelpResource/delete/",
    'resLoading':false,
    'qrc':'',
    'context':'',
    'delResource':function(helpid, success_callback, failed_callback){
        if(this.resLoading) return ;
        this.resLoading = true;
        this.context = {'helpid':helpid};
        that = this
        sendResourceDeleteReq(this.del_url, this.qrc, this.context, function(data){ 
             if(data.resp_qrc['result'] == "OK"){
                 success_callback && success_callback(that.context['helpid'])
             }else{
                 failed_callback && failed_callback(that.context['helpid']);
             }
             that.resLoading = false;
        });
    },
}

updatesHelpResource = {
    'get_url':"/resource/UpdatesHelpResource/get/",
    'resLoadFailedCnt':0,
    'lastHelpPt':0.0,
    'location':[],
    'resLoading':false,
    'qrc':"",
    'context':"",
    'getResource':function(callback){
         if(this.resLoading) return ;
         if(this.resLoadFailedCnt >= 3) return ;
         this.resLoading = true;
         this.context = {"last_help_pt":this.lastHelpPt,'location':this.location};
         this.qrc = {"rcd_num":6}
         that = this;
         sendResourceGetReq(this.get_url, this.qrc, this.context, function(data){
             if(data.resp_qrc.rcd_num == 0){
                 that.resLoadFailedCnt += 1;
             }else{
                 that.lastHelpPt = data.resp_qrc['last_help_pt']; 
             }
             callback && callback(data);         
             that.resLoading = false;
         });
     }

}

wxJSAPIResource = {
    'get_url':'/resource/WXJSApiResource/get/',
    'qrc':'',
    'context':'',
    'getResource':function(callback){
         this.context = {"req_url":location.href+location.search};
         this.qrc = {};
         sendResourceGetReq(this.get_url, this.qrc, this.context, function(data){
             callback && callback(data); 
         });
     }
}