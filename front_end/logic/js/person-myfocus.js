/**
 * Created by python on 19-8-29.
 */


var vm = new Vue({
    el:'#fuck',
    data:{
        host,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        avatar:sessionStorage.avatar || localStorage.avatar,
        username:sessionStorage.username || localStorage.username,
        tags:[],
        page: 1, // 当前页数
        page_size:6, // 每页数量
        count: 0,  // 总数量
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
    mounted: function () {
        this.get_tags();
    },
    methods:{

        get_tags:function () {
            axios.get(this.host+"/myfocus/",{
                params: {
                    page: this.page,
                    page_size: this.page_size,
                },
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                withCredentials: true,
                responseType: 'json'
            })
            .then(response => {
                this.tags = response.data.results;
                this.count = response.data.count;
                console(this.tags)
                // 标签url
            })
            .catch(error => {
                console.log(error.response.data);
            })
        },

        is_concern:function(is_concern){
            if (is_concern == 0){
                return true
            }else {
                return false
            }
        },

        dislike_tag:function (tag_id) {
            axios.delete(this.host+'/tag/like/', {
                params:{
                        tag_id:tag_id,
                    },
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
                withCredentials: true
            })
            .then(response => {
                console.log(response.data);
                alert("已取消关注")
                this.get_tags()
            })
            .catch(error => {
                console.log(error.response.data);
            })
        }
    }
})