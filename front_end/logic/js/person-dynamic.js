/**
 * Created by python on 19-8-29.
 */

Vue.filter('str2date', function (value) {
  return new Date(value)
})

Vue.filter('date2delta', function (value) {
    // 获取当前时间和value的时间差
    if (!value) return ''
    date = new Date(value)
    now = new Date()
    ms = now.getTime() - date.getTime()
    day = Math.floor(ms / 1000 / 60 / 60 / 24)
    hour = Math.floor((ms / 1000 / 60 / 60) - 24 * day)
    minute = Math.ceil(ms / 1000 / 60 - (hour + 24 * day) * 60)
    if (day > 0) return day + '天' + hour + '小时' + minute + '分钟'
    else if (hour > 0) return hour + '小时' + minute + '分钟'
    else return minute + '分钟'
})


var sb = new Vue({
    el:".activities",
    delimiters: ['[[', ']]'],
    data:{
        // 页面中需要使用到的数据，键值对
        host,
        page: 1, // 当前页数
        page_size: 5, // 每页数量
        count: 0,  // 总数量
        activities: [],
        user_id: localStorage.user_id || sessionStorage.user_id,
        avatar: localStorage.username || sessionStorage.username,
        username: localStorage.username || sessionStorage.username,
        token: sessionStorage.token || localStorage.token,

    },

    computed: {
        total_page: function(){  // 总页数
            return Math.ceil(this.count/this.page_size);
        },
        next: function(){  // 下一页
            if (this.page >= this.total_page) {
                return 0;
            } else {
                return this.page + 1;
            }
        },
        previous: function(){  // 上一页
            if (this.page <= 0 ) {
                return 0;
            } else {
                return this.page - 1;
            }
        },
        page_nums: function(){  // 页码
            // 分页页数显示计算
            // 1.如果总页数<=5
            // 2.如果当前页是前3页
            // 3.如果当前页是后3页,
            // 4.既不是前3页，也不是后3页
            var nums = [];
            if (this.total_page <= 5) {
                for (var i=1; i<=this.total_page; i++){
                    nums.push(i);
                }
            } else if (this.page <= 3) {
                nums = [1, 2, 3, 4, 5];
            } else if (this.total_page - this.page <= 2) {
                for (var i=this.total_page; i>this.total_page-5; i--) {
                    nums.push(i);
                }
            } else {
                for (var i=this.page-2; i<this.page+3; i++){
                    nums.push(i);
                }
            }
            return nums;
        }
    },

    mounted:function () {
         this.get_activities()
    },
    methods:{
        // 需要用到的函数，键值对 ，键是名称，值是匿名函数
         get_activities: function(){
            axios.get(this.host+'/dynamics/', {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    params: {
                        page: this.page,
                        page_size: this.page_size
                    },
                    responseType: 'json'
                })
                .then(response => {
                    this.count = response.data.count;
                    this.activities = response.data.results;
                })
                .catch(error => {
                    console.log(error.response.data);
                })
        },

        // 点击页数
        on_page: function(num){
            if (num != this.page){
                this.page = num;
                this.get_answers();
            }
        },
    },
})

