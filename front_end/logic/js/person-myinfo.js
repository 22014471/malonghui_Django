/**
 * Created by python on 19-8-30.
 */
var vcc = new Vue({
    el: '#myinfo',
    data: {
        host,
        user_id : sessionStorage.user_id || localStorage.user_id,
        username : sessionStorage.username || localStorage.username,
        token: sessionStorage.token || localStorage.token,
        personal_url: "",
        email: "",
        mobile: "",
        live_city: '',
        graduation: "",
        gender:'',
        address: '',
        birthday: ''
    },
    mounted: function() {
            axios.get(this.host + '/myfile/', {
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
                })
                .then(response => {
                    // 加载用户数据
                    // this.user_id = response.data.id;
                    this.username = response.data.username;
                    this.mobile = response.data.mobile;
                    this.email = response.data.email;
                    this.personal_url = response.data.personal_url;
                    this.live_city = response.data.live_city;
                    this.graduation = response.data.graduation;
                    this.gender = response.data.gender;
                    this.address = response.data.address;
                    this.birthday = response.data.birthday;
                    if (this.gender == 0){
                        this.gender = '男'
                    }else{
                        this.gender ='女'
                    }
                })
                .catch(error => {
                    if (error.response.status == 401 || error.response.status == 403) {
                        location.href = '/person-loginsign.html';
                    }
                });

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

