/**
 * Created by python on 19-8-25.
 */

// 详情页
var vm = new Vue({
    el: '#app',
    data: {
        news: {}, //头条
        news_comments: [], //评论及子评论表
        // children_list: [],
        // children_count: '',
        host: host,
        news_id: '', //新闻id
        show_comments_index :-1,
        detail_hots: [],
        detail_talks: [],
        user_id: sessionStorage.user_id || localStorage.user_id || 0,
        username: sessionStorage.username || localStorage.username,
        avatar: sessionStorage.avatar || localStorage.avatar,
        token: sessionStorage.token || localStorage.token,
        att: false, //关注控制
        col: false, //收藏控制
        content: '',
        child_content: "",


    },
    mounted: function () {
        this.news_id = this.get_query_string("news_id");
        this.detail();
        this.comments();
        this.hots();
        this.talks();
    },
    methods: {
        // 分类功能
        detail: function () {
            axios({
                url: this.host + '/headlines_detail/' + this.news_id,
                method: 'get',
            })
                .then(function (dat) {
                    vm.news = dat.data;
                    var author_fans = vm.news.author.attention;
                    var news_collected = vm.news.collected;
                    for(var i=0;i<author_fans.length;i++){
                        if(vm.user_id == author_fans[i].user.id){
                            vm.att = true
                        }
                    }
                    for(var i=0;i<news_collected.length;i++){
                        if(vm.user_id == news_collected[i].user.id){
                            vm.col = true
                        }
                    }

                })
                .catch(function () {
                    alert('请求失败')
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

        // 评论
        comments: function () {
            axios({
                url: this.host + '/headlines_comments/' + this.news_id,
                method: 'get',
            })
                .then(function (dat) {
                    vm.news_comments = dat.data;

                })
                .catch(function () {
                    alert('请求失败')
                })
        },

        //控制回复框显示隐藏
        callback: function (i) {
            if (vm.show_comments_index==i){
                vm.show_comments_index = -1
                return
            }
            vm.show_comments_index = i
        },

        // 热门头条排行
        hots: function () {
            axios({
                url: this.host + '/headlines_hots',
                method: 'get',
            })
                .then(function (dat) {
                    vm.detail_hots = dat.data;

                })
                .catch(function () {
                    alert('请求失败')
                })
        },

        // 热门头条排行
        talks: function () {
            axios({
                url: this.host + '/headlines_talks',
                method: 'get',
            })
                .then(function (dat) {
                    vm.detail_talks = dat.data;

                })
                .catch(function () {
                    alert('请求失败')
                })
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
                    vm.att = true

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
                    vm.att = false

                })
                .catch(function (dat) {
                    alert('已取消关注请勿重复操作')

                })

            }
        },

        // 点击收藏
        collection_add: function (news_id) {
              axios({
                  url:this.host + '/headlines_collection',
                  method:'post',
                  headers: {
                    'Authorization': 'JWT ' + this.token
                },
                  data:{
                      "news": news_id
                  }
        })
            .then(function (dat) {
                    alert('取消收藏成功')
                    vm.col = true

                })
                .catch(function (dat) {
                    alert('已取消收藏请勿重复操作')

                })


        },

        // 点击收藏
        collection_delete: function (news_id) {
              axios({
                  url:this.host + '/headlines_collection',
                  method:'delete',
                  headers: {
                    'Authorization': 'JWT ' + this.token
                },
                  data:{
                      "news": news_id
                  }
        })
            .then(function (dat) {
                    alert('收藏成功')
                    vm.col = false

                })
                .catch(function (dat) {
                    alert('已取消收藏请勿重复操作')

                })


        },


        // 发表评论
        on_submit: function (news_id) {
            if (news_id && vm.content){
                 axios({
                  url:this.host + '/headlines_comment',
                  method:'post',
                  headers: {
                    'Authorization': 'JWT ' + this.token
                },
                  data:{
                      "news": news_id,
                      "content":vm.content,
                  }
        })
            .then(function (dat) {
                alert('评论成功')
                location.reload()
                })
                .catch(function (dat) {
                status = dat.response.status;
                    if (status == 507){
                         alert('评论失败')
                    }
                })
            }

        },
        // 发表子评论
        child_submit: function (news_id,parent) {
            if (news_id && vm.child_content){
                 axios({
                  url:this.host + '/headlines_comment',
                  method:'post',
                  headers: {
                    'Authorization': 'JWT ' + this.token
                },
                  data:{
                      "news": news_id,
                      "content":vm.child_content,
                      "parent": parent,

                  }
        })
            .then(function (dat) {
                alert('评论成功')
                location.reload()
                })
                .catch(function (dat) {
                status = dat.response.status;
                    if (status == 507){
                         alert('评论失败')
                    }
                })
            }

        },
    },
    filters: {
        filterA(value){
            var data = new Date(value)
            var day = data.getDate()
            var mouth = data.getMonth() + 1
            return mouth + '月' + day + '日'
        },
        filterB(value){
            var len = value.length
            if (len == 0){
                return
            }

            return len + '条回复'
        }
    }

})

