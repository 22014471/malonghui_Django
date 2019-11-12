caches host = 'http://193.112.250.74:8000'

Vue.filter('dateclass', function(value){
    return new Date(value)
})

//年月日
Vue.filter('date', function(){
    var day = value.getDate()
    var mouth = value.getMonth() + 1
    var year = value.setFullYear()
    return year+'-'+ mouth +'-'+ day
})


//时分秒
Vue.filter('time', function(){
    var hours = value.getHours()
    var minutes = value.getMinutes()
    var seconds = value.getSeconds()
    return hours+':'+ minutes +':'+ seconds
}

//星期
var WEEK = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
Vue.filter('week', function(value){
    var week = WEEK[value.getDay()]
    return week
})



// 获取url路径参数
get_query_string: function(name){
    var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
    var r = window.location.search.substr(1).match(reg);
    if (r != null) {
        return decodeURI(r[2]);
    }
    return null;
}

// 倒计时
data:{
    now_in_ms：0,
    deadline_in_ms: 0,
}

this.now_in_ms = new Date(response.headers.data).getTime()
//在django中配置 CORS_EXPOSE_HEADERS = ['Data']

this.deadline_in_ms = new Date(reaponse.data.deadline)

//定时器
setInterval(()=>
    {
     this.now_in_ms += 1
     this.deadline_countdown_in_second = Math.floor((this.deadline_in_ms - this.now_in_ms) /1000)
}
)


// 过滤器
filters:{
    countdown: function(value_in_second){
        var day = Math.floor(value_in_second / 3600 / 24);
        var hour = Math.floor(value_in_second / 3600) % 24;
        var minute = Math.floor(value_in_second / 60) % 60;
        var second = value_in_second % 60;
        return day + '天' + hour + '时' + minute + '分' + second +'秒'
    }
}