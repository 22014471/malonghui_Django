/**
 * Created by python on 19-8-24.
 */


var vm = new Vue({
    el: "#app",
    data:{
        host,
        active:'active',
        category_id:null,
        category_list: [],
        question_list: [],
        ordering:'-create_time',
        page: 1, // 当前页数
        page_size:6, // 每页数量
        count: 0,  // 总数量
        cid:0,
        new_class:"active",
        hot_class:" ",
        wait_class:" ",
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
    mounted: function(){
        // 获取问题分类
        this.ordering = get_query_string('ordering');
        this.get_categories();
        this.get_questions(this.category_id);
    },
    methods: {
        change_new_class:function () {
            this.new_class = "active";
            this.hot_class = " ";
            this.wait_class = " ";
            this.get_questions(3,'create_time')
        },
        change_hot_class:function () {
            this.hot_class = "active";
            this.new_class = " ";
            this.wait_class = " ";
            this.get_questions(3,'hot')
        },
        change_wait_class:function () {
            this.wait_class = "active";
            this.hot_class = " ";
            this.new_class = " ";
            this.get_questions(3,'wait')
        },
        // 获取首页问题
        get_questions: function (category_id,ordering) {
            axios.get(this.host+'/questions/',{
                params: {
                            page: this.page,
                            page_size: this.page_size,
                            ordering: ordering,
                            category_id:category_id,
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
        // 点击页数
        on_page: function(num){
            if (num != this.page){
                this.page = num;
                this.get_questions();
            }
        },
    }
})