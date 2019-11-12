var host = 'http://193.112.250.74:8000';


Vue.filter('str2date', function (value) {
    return new Date(value)
});

Vue.filter('date2ymd', function (value) {
    return value.getFullYear() + '-' + (value.getMonth() - 1) + '-' + value.getDate();
});

Vue.filter('data2hm', function (value) {
    return value.getHours() + ':' + value.getMinutes();
});

var week = ["周日","周一","周二","周三","周四","周五","周六"]
Vue.filter('str2w', function (value) {
    return week[value.getDay()]
});

Vue.filter('date2year', function(value){
    return value.getFullYear() + '年创建'
})

/**
 * 获取当前时间
 * 格式YYYY-MM-DD
 */
Vue.prototype.getNowFormatDate = function() {
  var date = new Date();
  var seperator1 = "-";
  var year = date.getFullYear();
  var month = date.getMonth() + 1;
  var strDate = date.getDate();
  if (month >= 1 && month <= 9) {
    month = "0" + month;
  }
  if (strDate >= 0 && strDate <= 9) {
    strDate = "0" + strDate;
  }
  var currentdate = year + seperator1 + month + seperator1 + strDate;
  return currentdate;
};



Vue.filter('str_split', function(data) {
    return data.split('-')[0]
});

// 获取url路径参数
function get_query_string(name,defValue){
    var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
    var r = window.location.search.substr(1).match(reg);
    if (r != null) {
        return decodeURI(r[2]);
    }
    return defValue;
};




// Vue.filter('dateclass', function(value){
//     return new Date(value)
//     alert(value)
// })
//
// //年月日
// Vue.filter('date', function(value){
//
//     var day = value.getDate()
//     var mouth = value.getMonth() + 1
//     var hours = value.getHours()
//     var minutes = value.getMinutes()
//     return  mouth +'月'+ day + '日'+ ' ' + hours + ':' + minutes
// })





