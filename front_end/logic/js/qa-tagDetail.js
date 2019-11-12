/**
 * Created by python on 19-8-28.
 */

var vm = new Vue({
    el:"#app",
    data:{
        host,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        avatar:sessionStorage.avatar || localStorage.avatar,
        username:sessionStorage.username || localStorage.username,
        tag:null,
        tag_id:null,
        hottags:[],
        category_list:[],
        question_list:[],
        page: 1, // 当前页数
        page_size:6, // 每页数量
        count: 0,  // 总数量
        time_class_name:"sui-btn class",
        like_class_name:"sui-btn",
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
    mounted:function () {
        this.tag_id = get_query_string("tag_id");
        this.get_tag();
        this.get_hottags();
        this.get_questions("-create_time");
    },
    methods:{
        change_time_class:function () {
            this.time_class_name = 'sui-btn active';
            this.like_class_name = 'sui-btn';
            this.get_questions('-create_time')
        },
        change_like_class:function () {
            this.like_class_name = 'sui-btn active';
            this.time_class_name = 'sui-btn';
            this.get_questions('-like_count')
        },
        get_questions: function (ordering) {
            axios.get(this.host+'/tag/questions/',{
                params: {
                            page: this.page,
                            page_size: this.page_size,
                            ordering: ordering,
                        },
                responseType: 'json',
            })
            .then(response => {
                this.question_list = response.data.results;
                this.count = response.data.count;
            })
            .catch(error => {
                console.log(error.response.data);
            });
        },
        is_login:function () {
            if(this.user_id&&this.token){
                return false
            }else {
                return true
            }
        },
        get_tag:function () {
            axios.get(this.host+'/tag/'+this.tag_id+'/',{
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
                withCredentials: true
            })
            .then(response => {
                this.tag = response.data;
            })
            .catch(error => {
                console.log(error.response.data);
            })
        },
        // 获取问题分类
        get_categories: function(){
            axios.get(this.host+'/question/categories/', {
                    responseType: 'json'
                })
                .then(response => {
                    this.category_list = response.data;
                    // 拼接问题url
                })
                .catch(error => {
                    console.log(error.response.data);
                })
        },
        get_hottags:function(){
            axios.get(this.host+'/hottags/', {
                    responseType: 'json'
                })
                .then(response => {
                    this.hottags = response.data;
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
        like_tag:function (tag_id) {
            if (!(this.user_id && this.token)){
                alert("请先登录");
                location.href="/person-loginsign.html?next=/qa-tagDetail?tag_id="+question_id
            }
            axios.post(this.host+'/tag/like/', {
                        tag_id:tag_id,
                    },{
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
                withCredentials: true
            })
            .then(response => {
                console.log(response.data);
                alert("关注成功");
                location.reload()
            })
            .catch(error => {
                console.log(error.response.data);
            })
        },
        dislike_tag:function (tag_id) {
            if (!(this.user_id && this.token)){
                alert("请先登录");
                location.href="/person-loginsign.html?next=/qa-allTag.html?tag_id="+tag_id
            }
            axios.delete(this.host+'/tag/like/', {
                params:{
                    tag_id:tag_id
                },
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
                withCredentials: true
            })
            .then(response => {
                console.log(response.data);
                alert("已取消关注");
                location.reload()
            })
            .catch(error => {
                console.log(error.response.data);
            })
        }
    }

})
