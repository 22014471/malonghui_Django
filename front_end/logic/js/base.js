/**
 * Created by python on 19-8-24.
 */
const host = 'http://193.112.250.74:8000';

// 获取url路径参数
function get_query_string(name) {
    var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
    var r = window.location.search.substr(1).match(reg);
    if (r != null) {
        return decodeURI(r[2]);
    }
    return null;
}


Vue.filter('str2day', function(value){
    return new Date(value)
});

Vue.filter('date2ymd', function (value) {
    return value.getFullYear() + '-' + (value.getMonth() + 1) + '-' + value.getDate();
});

