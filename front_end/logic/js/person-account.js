/**
 * Created by python on 19-8-29.
 */
var sb = new Vue({
    el:'.account-main',
    data:{
        host,
        user_id : sessionStorage.user_id || localStorage.user_id,
        username : sessionStorage.username || localStorage.username,
        token: sessionStorage.token || localStorage.token,
        personal_url: "",
        email: "",
        mobile: "",
        live_city: '',
        graduation: "",
        commany: ""
    },
    mounted: function(){
        // 判断用户的登录状态
        if (this.user_id && this.token) {
            axios.get(this.host + '/account/', {
                    // 向后端传递JWT token的方法
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    responseType: 'json',
                })
                .then(response => {
                    // 加载用户数据
                    this.personal_url = response.data.personal_url;
                    this.email = response.data.email;
                    this.mobile = response.data.mobile;
                    this.live_city = response.data.live_city;
                    this.graduation = response.data.graduation;
                    this.commany =response.data.commany;
                })
                .catch(error => {
                    if (error.response.status==401 || error.response.status==403) {
                        location.href = '/person-loginsign.html';
                    }
                });
        } else {
            location.href = '/person-loginsign.html';
        }
    },
    methods: {
        // 退出
        logout: function(){
            sessionStorage.clear();
            localStorage.clear();
            location.href = '/headline-login.html';
        },
        // 保存email
        save_email: function(){

        }
    }
});
