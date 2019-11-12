// 主页
var vm = new Vue({
    el:'#app',
    data:{
        category_list:[],
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
        keyword: ''
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
        this.categories()
        this.cat(this.category)
        this.questions()
        this.activities()
        },
    methods:{
        // 分类功能
        categories:function(){
         axios({
            url:this.host + '/headlines_category',
            method:'get',
        })
        .then(function(dat){
            console.log(dat.data)
            vm.category_list = dat.data

        })
        .catch(function(){
            alert('请求失败')
        })
        },

        // 分类点击
        cat:function(category_id){

            // 全局cate变量存储category
            this.cate = this.category;

            //存储当前分类id
            this.category = category_id

            // 判断如果分类改变重置当前页数
            if (this.cate != this.category){
                this.page = 1
            }

            axios({
                url:this.host + '/headlines_news/'+ category_id,
                method:'get',
                params: {
                    page: this.page,
                    page_size: this.page_size,
                },
        })
            .then(function (dat) {
                vm.count = dat.data.count + 1;
                console.log(dat.data);
                vm.news_list = dat.data.results;
                if (localStorage.unlike_by_id) {
                    vm.unlike_by_id = localStorage.unlike_by_id.split(',').filter(function (element, index, self) {
                        return self.indexOf(element) === index;
                    })
                    vm.count -= vm.unlike_by_id.length
                }
                for (var i = 0; i < vm.news_list.length; i++) {
                    for (var n = 0; n < vm.unlike_by_id.length; n++) {
                        if (vm.unlike_by_id[n] == vm.news_list[i].id) {
                            vm.news_list.splice(i, 1)
                        }
                    }
                    var author_id = vm.news_list[i].author.id
                    var att_list = vm.news_list[i].author.attention;
                    vm.att_dict[String(author_id)] = att_list;

                    if (vm.att_dict[author_id].length > 0) {
                        for (var j = 0; j < vm.att_dict[author_id].length; j++) {
                            if (vm.user_id == vm.att_dict[author_id][j].user.id) {
                                vm.news_list[i]["att"] = true
                            }

                        }
                    }
                }

            })

        },

        //问答排行
        questions:function(){
            axios({
                url:this.host + '/headlines_questions',
                method:'get',
        })
            .then(function (dat) {
                    vm.question_list = dat.data
                })
                .catch(function () {
                    alert('请求失败')
                })
        },

        // 热门活动
        activities:function(){
            axios({
                url:this.host + '/headlines_activities',
                method:'get',
        })
            .then(function (dat) {
                    vm.activity_list = dat.data
                })
                .catch(function () {
                    alert('请求失败')
                })
        },
       
        // 点击页数
        on_page: function (num) {
            if (num != this.page) {
                this.page = num;
                this.cat(this.category);
            }
        },
        // 点击关注
        attention_add: function (author_id) {
            if (author_id != this.user_id) {
              axios({
                  url:this.host + '/headlines_attention',
                  method:'post',
                  headers: {
                    'Authorization': 'JWT ' + this.token
                },
                  data:{
                      "author": author_id
                  }
        })
            .then(function (dat) {
                    alert('关注成功')
                    location.reload()

                })
                .catch(function (dat) {
                    status = dat.response.status;
                    if (status == 400){
                         alert('已关注请勿重复关注')
                    }
                })

            }
            else
            {alert("不能关注自己")}
        },

        // 点击取消关注
        attention_delete: function (author_id) {
            if (author_id != this.user_id) {
              axios({
                  url:this.host + '/headlines_attention',
                  method:'delete',
                  headers: {
                    'Authorization': 'JWT ' + this.token
                },
                  data:{
                      "author": author_id
                  }
        })
            .then(function (dat) {
                    alert('取消关注成功')
                     location.reload()

                })
                .catch(function (dat) {
                    alert('已取消关注请勿重复操作')

                })

            }

        },

        //添加不感兴趣
        unlike: function (news_id) {
            localStorage.unlike_by_id += ',' + news_id;
            vm.unlike_by_id = localStorage.unlike_by_id.split(',').filter(function(element,index,self){
                    return self.indexOf(element) === index;
                });
            if ((vm.unlike_by_id.length-1)>=vm.page_size)
            {
                vm.page +=1
                alert(vm.page)
            }
            alert('安排！已为你重新加载内容')
            location.reload()


        },
        //跳转查询
        elstic:function () {

            location.href = this.host + '/headline-elasticsearch.html?els=' + vm.keyword
        }
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

