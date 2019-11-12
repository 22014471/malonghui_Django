/**
 * Created by python on 19-8-28.
 */
var vm = new Vue({
    el: '#update',
    data: {
        host,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        username: sessionStorage.username || localStorage.username,
        live_city: "",
        graduation: "",
        commany: "",
        personal_url: "",
        avatar: ""
    },
    mounted: function(){
        // 判断用户的登录状态
        if (this.user_id && this.token) {
            axios.get(this.host + '/user/detail/', {
                    // 向后端传递JWT token的方法
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    responseType: 'json',
                })
                .then(response => {
                    // 加载用户数据
                    this.personal_url = response.data.personal_url;
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