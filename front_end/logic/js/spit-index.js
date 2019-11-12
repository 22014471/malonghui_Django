var app = new Vue({
    el: "#app",
    // delimiters: ['[[', ']]'], // 修改vue模板符号，防止与django冲突
    data: {
        // 页面中需要使用到的数据，键值对
        host: host,
        talks: [],
        page: 1, // 当前页数
        page_size: 10, // 每页数量
        ordering: '-create_time', // 排序
        count: 0,  // 总数量
        username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,

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
            if (this.total_page <= 10) {
                for (var i = 1; i <= this.total_page; i++) {
                    nums.push(i);
                }
            } else if (this.page <= 3) {
                nums = [1, 2, 3, 4, 5];
            } else if (this.total_page - this.page <= 2) {
                for (var i = this.total_page; i > this.total_page - 5; i--) {
                    nums.push(i);
                }
            } else {
                for (var i = this.page - 2; i < this.page + 3; i++) {
                    nums.push(i);
                }
            }
            return nums;
        }
    },
    mounted: function () {
        // 一加载就需要做的，直接是代码
        this.get_talks();
    },
    methods: {
        checkToken () {
            // 用户没有登陆
            if (!this.token) {
                location.href = 'headline-login.html?next=/spit-index.html'
                return
            }
        },
        // 需要用到的函数，键值对 ，键是名称，值是匿名函数
        //吐槽的点赞
        talk_like: function (talk) {
            // 用户没有登陆
            this.checkToken()
            axios.post(this.host + '/talk/likes',
                {
                    talk_id: talk.id
                }, {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    responseType: 'json',
                    withCredentials: true,
                })

                .then(response => {
                    talk.is_like = 1
                    talk.like_count += 1
                })
                .catch(error => {

                })


        },
        //吐槽取消点赞
        remove_talk_like: function (talk) {
            // 用户没有登陆
            this.checkToken()
            axios.delete(this.host + '/talk/likes/' + talk.id,

                {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    params: {
                        talk_id: talk.id,
                    },
                    responseType: 'json',
                    withCredentials: true,
                }
            )
                .then(response => {
                    talk.is_like = 0
                    talk.like_count -= 1
                })
                .catch(error => {

                })


        },
        // 收藏
        talk_collect: function (talk_id) {
            // 用户没有登陆

            if (!this.token) {
                location.href = 'person-loginsign.html?next=/spit-index.html'
                return
            }
            axios.post(this.host + '/talk/collect',
                {
                    talk_id: talk_id
                }, {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    responseType: 'json',
                    withCredentials: true,
                })

                .then(response => {
                    talk.is_collect = 1

                })
                .catch(error => {

                })


        },
        // 取消收藏
        remove_talk_collect: function (talk) {
            // 用户没有登陆
            if (!this.token) {
                location.href = 'headline-login.html?next=/spit-index.html'
                return
            }
            axios.delete(this.host + '/talk/collect',

                {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    params: {
                        talk_id: talk.id,
                    },
                    responseType: 'json',
                    withCredentials: true,
                })

                .then(response => {
                    talk.is_collect = 0

                })
                .catch(error => {

                })


        },

        get_talks: function () {
            axios.get(this.host + "/talks/", {
                params: {
                    page: this.page,
                    page_size: this.page_size,
                    ordering: this.ordering
                },
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
                withCredentials: true,
            })
                .then(response => {
                    this.count = response.data.count;
                    this.talks = response.data.results;
                    for (var i = 0; i < this.talks.length; i++) {
                        this.talks[i].url = '/talks/' + this.talks[i].id + ".html";
                    }
                })
                .catch(error => {
                    console.log(error.response.data);
                })
        },
        // 点击页数
        on_page: function (num) {
            if (num != this.page) {
                this.page = num;
                this.get_talks();
            }
        },

    },
    filters: {
        filterA(value){
            data = new Date(value)
            var year = data.getFullYear()
            var day = data.getDate()
            var mouth = data.getMonth() + 1
            var hours = data.getHours()
            var minutes = data.getMinutes()
            return year + '-' + mouth + '-' + day + ' ' + hours + ':' + minutes
        },

    },

})