/**
 * Created by python on 19-8-25.
 */

var vm = new Vue({
    el:"#app",
    data:{
        host,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        avatar:sessionStorage.avatar || localStorage.avatar,
        username:sessionStorage.username || localStorage.username,
        oauth_access_token:sessionStorage.oauth_access_token || localStorage.oauth_access_token,
        category_list: [],
        answer_list:[],
        question_id:null,
        question:null,
        content:null,
        q_show:false,
        a_show_comment:null,
        a_show_edit:null,
        a_active:'',
        a_dislike_active:'',
        a_like_active:'',
        q_active:'',
        q_dislike_active:'',
        q_like_active:'',
        is_like:false,
    },
    mounted:function () {
        this.question_id = get_query_string('question_id');
        if (!this.question_id){
            location.href='/qa-login.html'
        }
        this.get_categories();
        this.get_question_answer();
        this.get_question();
    },
    methods:{
        go_to_share:function (title,question_id) {
            location.href='/qa-share.html?question_id='+question_id+'&title='+title
        },
        is_login:function () {
            if(this.user_id&&this.token){
                return false
            }else {
                return true
            }
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
        get_question_answer:function () {
            axios.get(this.host+'/question/answers/', {
                params:{
                    question_id:this.question_id,
                    ordering:'-like_count'
                },
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
                withCredentials: true
                })
                .then(response => {
                    this.answer_list = response.data;
                })
                .catch(error => {
                    console.log(error.response.data);
                })
        },
        get_question:function () {
            axios.get(this.host+'/question/', {
                params:{
                    question_id:this.question_id
                },
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
                withCredentials: true
            })
            .then(response => {
                this.question = response.data;
                // 拼接问题url
            })
            .catch(error => {
                console.log(error.response.data);
            })
        },
        get_submit_answer:function (parent_id) {
            if (!this.content){
                alert("评论为空");
            }
            else if (!(this.user_id && this.token)){
                alert("请先登录");
                location.href="/person-loginsign.html?next=/qa-detail.html?question_id="+this.question_id
            }
            else {
                axios.post(this.host+'/question/answer/',
                    {
                        content:this.content,
                        question:this.question_id,
                        parent:parent_id,
                    }, {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                },
                    responseType: 'json',
                    withCredentials: true
                })
                .then(response => {
                    console.log(response.data);
                    alert("解答成功");
                    location.href="/qa-detail.html?question_id="+this.question_id
                })
                .catch(error => {
                    if (error.response.status == 400){
                    console.log(error.response.data);
                    alert('评论不能为空');
                    location.href="/qa-detail.html?question_id="+this.question_id
                }
                else if(error.response.status == 401) {
                    console.log(error.response.data);
                    alert("请先登录");
                    location.href="/person-loginsign.html?next=/qa-detail?question_id="+this.question_id
                }else {
                    console.log(error.response.data);
                }
                })
            }
        },
        edit_answer:function (answer_id) {
            if (!this.content){
                alert("评论为空");
            }
            else if (!(this.user_id && this.token)){
                alert("请先登录");
                location.href="/person-loginsign.html?next=/qa-detail.html?question_id="+this.question_id
            }
            else {
                axios.put(this.host+'/question/answer/',
                    {
                        content:this.content,
                        question_id:this.question_id,
                        id:answer_id
                    }, {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                },
                    responseType: 'json',
                    withCredentials: true
                })
                .then(response => {
                    console.log(response.data);
                    alert("编辑成功");
                    location.href="/qa-detail.html?question_id="+this.question_id
                })
                .catch(error => {
                    if (error.response.status == 400){
                    console.log(error.response.data);
                    alert('评论不能为空');
                    location.href="/qa-detail.html?question_id="+this.question_id
                }
                else if(error.response.status == 401) {
                    console.log(error.response.data);
                    alert("请先登录");
                    location.href="/person-loginsign.html?next=/qa-detail?question_id="+this.question_id
                }else {
                    console.log(error.response.data);
                }
                })
            }
        },
        like_question:function (action) {
            if (!(this.user_id && this.token)){
                alert("请先登录");
                location.href="/person-loginsign.html?next=/qa-detail?question_id="+this.question_id
            }
            axios.post(this.host+'/question/like/',
                {
                    question_id:this.question_id,
                    action:action
                },{
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
                withCredentials: true
            })
            .then(response => {
                console.log(response.data);
                this.get_question();
            })
            .catch(error => {
                if (error.response.status == 400){
                    console.log(error.response.data);
                    alert('一个问题您只能点赞或踩一次')
                }
                else if(error.response.status == 401) {
                    console.log(error.response.data);
                    alert("请先登录");
                    location.href="/person-loginsign.html?next=/qa-detail?question_id="+this.question_id
                }else {
                    console.log(error.response.data);
                }
            })
        },
        like_answer:function (answer_id,action) {
            if (!(this.user_id && this.token)){
                alert("请先登录");
                location.href="/person-loginsign.html?next=/qa-detail?question_id="+this.question_id
            }
            axios.post(this.host+'/answer/like/', {
                    answer_id:answer_id,
                    action:action
                },{
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
                withCredentials: true
            })
            .then(response => {
                console.log(response.data);
                this.get_question_answer();
            })
            .catch(error => {
                if (error.response.status == 400){
                    console.log(error.response.data);
                    alert('一个解答您只能点赞或踩一次')
                }
                else if(error.response.status == 401) {
                    console.log(error.response.data);
                    alert("请先登录");
                    location.href="/person-loginsign.html"
                }else {
                    console.log(error.response.data);
                }
            })
        },
        // 展示评论框
        q_is_show:function () {
            this.q_show=!this.q_show
        },
        a_is_show_comment:function (index) {
            this.a_show_comment = index;
        },
         a_is_show_edit:function (index,content) {
            this.a_show_edit = index;
            if (content){
                this.content = content
            }
        },
        q_is_hover:function () {
           this.q_active='color: #E64620';
        },
        q_is_leave:function () {
            this.q_active='color: #000';
        },
        q_like_is_hover:function () {
           this.q_like_active='color: #E64620';
        },
        q_like_is_leave:function () {
            this.q_like_active='color: #000';
        },
        q_dislike_is_hover:function () {
           this.q_dislike_active='color: #E64620';
        },
        q_dislike_is_leave:function () {
            this.q_dislike_active='color: #000';
        },
        a_is_hover:function () {
           this.a_active='color: #E64620';
        },
        a_is_leave:function () {
            this.a_active='color: #000';
        },
        a_like_is_hover:function () {
           this.a_like_active='color: #E64620';
        },
        a_like_is_leave:function () {
            this.a_like_active='color: #000';
        },
        a_dislike_is_hover:function () {
           this.a_dislike_active='color: #E64620';
        },
        a_dislike_is_leave:function () {
            this.a_dislike_active='color: #000';
        },
    },
})
