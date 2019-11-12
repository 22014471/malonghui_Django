/**
 * Created by python on 19-8-30.
 */
// 主页
var vm = new Vue({
    el:'#app',
    data:{
        news_list: [],
        host: host,
        page: 1, // 当前页数
        page_size:12, // 每页数量
        count: 0,  // 总数量
        category: 1,
        cate: 1,
        activity_list: [],
        question_list: [],
        unlike_by_id: '',
        user_id: sessionStorage.user_id || localStorage.user_id || 0,
        username: sessionStorage.username || localStorage.username,
        avatar: sessionStorage.avatar || localStorage.avatar,
        token: sessionStorage.token || localStorage.token,
        att_dict: {},
        query: '',
    },
     computed: {
        total_page: function () {  // 总页数
            return Math.ceil(this.count / this.page_size);

        },
        next: function () {  // 下一页
            if (this.page >= this.total_page) {
                return 0;
            } else {
                return this.page + 1;
            }
        },
        previous: function () {  // 上一页
            if (this.page <= 0) {
                return 0;
            } else {
                return this.page - 1;
            }
        },
        page_nums: function () {  // 页码
            // 分页页数显示计算
            // 1.如果总页数<=5
            // 2.如果当前页是前3页
            // 3.如果当前页是后3页,
            // 4.既不是前3页，也不是后3页

            var nums = [];
            if (this.total_page <= 5) {
                for (var i = 1; i <= this.total_page; i++) {
                    nums.push(i);
                }
            } else if (this.page <= 3) {
                nums = [1, 2, 3, 4, 5];
            }

            else if (this.total_page - this.page <= 2) {
                for (var i = this.total_page; i > this.total_page - 5; i--) {
                    nums.push(i);
                }
            }
            else {
                for (var i = this.page - 2; i < this.page + 3; i++) {
                    nums.push(i);
                }
            }
            if (this.total_page == 1) {
                nums = []
            }
            return nums;
        }
    },
    mounted:function(){
        this.query = get_query_string('els')
        this.cat()
        },
    methods:{
        // 分类点击
        cat:function(){
            axios({
                url:this.host + '/headlines/serach/',
                method:'get',
                params: {
                    query: this.query,
                    page: this.page,
                    page_size: this.page_size,
                },
        })
            .then(function (dat) {
                vm.count = dat.data.count;
                console.log(dat.data);
                vm.news_list = dat.data.results;

            })

        },
        // 获取url路径参数
        get_query_string: function(name){
            var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
            var r = window.location.search.substr(1).match(reg);
            if (r != null) {
                return decodeURI(r[2]);
            }
            return null;

        },
        },
        filters:{
	      filterA(value){
	           data = new Date(value)
              var day = data.getDate()
              var mouth = data.getMonth() + 1
              var hours = data.getHours()
              var minutes = data.getMinutes()
              return mouth + '月' + day + '日' + ' ' + hours + ':' + minutes
	      },
	      filterB(value){

              return value.slice(0,100) + ' ......'
	      },
	      filterC(value){
            data = new Date(value)
            var year = data.getFullYear()
            var day = data.getDate()
            var mouth = data.getMonth() + 1

            return year + '/' + mouth + '/' + day + '/'
        },
	    },
})

