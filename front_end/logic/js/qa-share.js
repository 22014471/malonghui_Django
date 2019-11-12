/**
 * Created by python on 19-8-31.
 */
var vm = new Vue({
    el:"#app",
    data:{
        content_wb:'',
        question_id:'',
        host,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        avatar:sessionStorage.avatar || localStorage.avatar,
        username:sessionStorage.username || localStorage.username,
        oauth_access_token:sessionStorage.oauth_access_token || localStorage.oauth_access_token,
    },
    mounted:function () {
        this.question_id = get_query_string('question_id');
        title = get_query_string('title');
        this.content_wb = '欢迎到http://193.112.250.74/qa-detail.html?question_id='+this.question_id+'来访问问题('+title+')';

    },
    methods:{
        share_to_weibo:function () {
            if(!this.oauth_access_token){
                alert('请先进行微博登录');
                location.href='/person-loginsign.html?next=/qa-logined.html'
            }else {
                axios.post(this.host+'/oauth/share_to_weibo/',{
                oauth_access_token:this.oauth_access_token,
                question_id:this.question_id,
                content:this.content_wb,
            },{
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
            })
            .then(response => {
                alert('分享成功,请访问您的微博主页查看分享');
                location.href='/qa-detail.html?question_id='+this.question_id
            })
            .catch(error => {
                if (error.response.status == 400){
                    alert("该问题您已经分享过，请分享其他问题");
                    location.href='/qa-logined.html'
                }
                console.log(error.response.data);
            })
            }
        },
    }
})
