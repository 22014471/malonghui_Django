var app = new Vue({
    el: "#app",
    data: {
        // 页面中需要使用到的数据，键值对
        host:host,
        talk: null,
        talk_comments: [],
        username: sessionStorage.username || localStorage.username,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
    },
    mounted: function () {
        // 一加载就需要做的，直接是代码
        var id = get_query_string('id', null)
        if (id == null) {
            location.href = '/spit-index.html'
        } else {
            axios.get(this.host + '/talks/' + id, {
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
                withCredentials: true
            })

            .then(response => {
                // console.log(response)
                this.talk = response.data
            })
        }
        ;
        axios.get(this.host + "/talks/" + id + "/comments")
            .then(response => {
                this.talk_comments = response.data
                console.log(response.data)
            });
    },
        methods: {
        // 需要用到的函数，键值对 ，键是名称，值是匿名函数
        // 评论提交
        create_comment: function (id) {
            if (!this.token) {
                location.href = 'person-loginsign.html?next=/spit-index.html'
                return
            }
            axios.post(this.host + '/talks/' + id + '/comments',
                {
                    talk_id: id,
                    user: this.user_id,
                    content: this.content
                }, {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    responseType: 'json',
                    withCredentials: true,
                })

                .then(response => {
                    location.reload()
                })
                .catch(error => {

                })

        }
        ,
        // 评论的点赞
        comment_like: function (comment) {
            if (comment.like_count==1) {
                this.remove_comment_like(comment)
                return
            }
            // 用户没有登陆
            if (!this.token) {
                location.href = 'person-loginsign.html?next=/spit-index.html'
                return
            }
            axios.post(this.host + '/talk/comment/likes',
                {
                    comment: comment.id,
                    user: this.user_id
                }, {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    responseType: 'json',
                    withCredentials: true,
                })

                .then(response => {
                     location.reload()
                })
                .catch(error => {

                })


        },
        // 取消评论点赞
        remove_comment_like: function (comment) {
            // 用户没有登陆
            if (!this.token) {
                location.href = 'person-loginsign.html?next=/spit-index.html'
                return
            }
            axios({
                  url:this.host + '/talk/comment/likes',
                  method:'delete',
                  headers: {
                    'Authorization': 'JWT ' + this.token
                },
                  data:{
                       comment: comment.id,
                       user: this.user_id
                  }
        })
            .then(function (dat) {
                    alert('取消关注成功')
                    vm.att = false
            // axios.delete(this.host + '/talk/comment/likes',
            //
            //      {
            //         headers: {
            //             'Authorization': 'JWT ' + this.token
            //         },
            //          params: {
            //             comment: comment,
            //             user: this.user_id
            //
            //              },
            //
            //         responseType: 'json',
            //         withCredentials: true,
            //     })
            //
            //     .then(response => {
            //
            //             location.reload()
            //     })
            //     .catch(error => {
            //
                 })


        },

        //吐槽的点赞
        talk_like: function (talk) {
            // 用户没有登陆
            if (!this.token) {
                location.href = 'person-loginsign.html?next=/spit-index.html'
                return
            }
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
                    talk.is_like = 1,
                        location.reload()
                })
                .catch(error => {

                })


        },
        //吐槽取消点赞
        remove_talk_like: function (talk) {
            // 用户没有登陆
            if (!this.token) {
                location.href = 'headline-login.html?next=/spit-index.html'
                return
            }
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
                    talk.is_like = 0,
                        location.reload()
                })
                .catch(error => {

                })


        },
    },

})


// axios.get(host +'talks/')

function get_query_string(name, defvalue) {
    var reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
    var r = window.location.search.substr(1).match(reg);
    if (r != null) {
        return decodeURI(r[2]);
    }
    return defvalue;
}