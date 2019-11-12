var vm1 = new Vue({
	el: '#app1',
	data: {
		host,
        // 注册
		error_name: false,
		error_password: false,
		error_phone: false,
		error_allow: false,
		error_sms_code: false,

		username: '',
		password: '',
		mobile: '',
		sms_code: '',
		allow: false,

		sms_code_tip: '获取短信验证码',
        sending_flag: false, // 正在发送短信标志,
        error_name_message:"",
        error_phone_message:"",

        // 登陆
        login_name: '',
        login_password: '',
        error_login_name: false,
        error_pwd: false,
        error_pwd_message: '请填写密码',
        remember: false
	},
	methods: {
	    // 注册
		check_username: function (){
            var len = this.username.length;
            if(len<5||len>32) {
                this.error_name_message = '请输入5-32个字符的用户名';
                this.error_name = true;
            } else {
                this.error_name = false;
            }
            // 检查重名
            if (this.error_name == false) {
                axios.get(this.host + '/usernames/' + this.username + '/count/', {
                        responseType: 'json'
                    })
                    .then(response => {
                        if (response.data.count > 0) {
                            this.error_name_message = '用户名已存在';
                            this.error_name = true;
                        } else {
                            this.error_name = false;
                        }
                    })
                    .catch(error => {
                        console.log(error.response.data);
                    })
            }
        },
		check_pwd: function (){
			var len = this.password.length;
			if(len<8||len>20){
				this.error_password = true;
			} else {
				this.error_password = false;
			}
		},
		check_phone: function (){
            var re = /^1[345789]\d{9}$/;
            if(re.test(this.mobile)) {
                this.error_phone = false;
            } else {
                this.error_phone_message = '您输入的手机号格式不正确';
                this.error_phone = true;
            }
            if (this.error_phone == false) {
                axios.get(this.host + '/mobiles/'+ this.mobile + '/count/', {
                        responseType: 'json'
                    })
                    .then(response => {
                        if (response.data.count > 0) {
                            this.error_phone_message = '手机号已存在';
                            this.error_phone = true;
                        } else {
                            this.error_phone = false;
                        }
                    })
                    .catch(error => {
                        console.log(error.response.data);
                    })
            }
        },
		check_sms_code: function(){
			if(!this.sms_code){
				this.error_sms_code = true;
			} else {
				this.error_sms_code = false;
			}
		},
		check_allow: function(){
			if(!this.allow) {
				this.error_allow = true;
			} else {
				this.error_allow = false;
			}
		},
		// 注册
		on_submit: function(){
            this.check_username();
            this.check_pwd();
            this.check_phone();
            this.check_sms_code();
            this.check_allow();

            if(this.error_name == false && this.error_password == false && this.error_phone == false && this.error_sms_code == false && this.error_allow == false) {
                axios.post(this.host + '/users/', {
                        username: this.username,
                        password: this.password,
                        mobile: this.mobile,
                        sms_code: this.sms_code,
                        allow: this.allow.toString()
                    }, {
                        responseType: 'json',
                    })
                    .then(response => {
                        localStorage.clear();
                        sessionStorage.clear();
                        localStorage.user_id = response.data.id;
                        localStorage.username = response.data.username;
                        localStorage.avatar = response.data.avatar;
                        localStorage.token = response.data.token;
                        parent.location.href = '/headline-login.html';
                    })
                    .catch(error=> {
                        if (error.response.status == 400) {
                            if ('non_field_errors' in error.response.data) {
                                this.error_sms_code_message = error.response.data.non_field_errors[0];
                                alert(this.error_sms_code_message);
                            } else {
                                this.error_sms_code_message = '数据有误';
                                alert(this.error_sms_code_message);
                            }
                            this.error_sms_code = true;
                        } else {
                            console.log(error.response.data);
                        }
                    })
            }
        },
		send_sms_code: function(){
            if (this.sending_flag == true) {
                return;
            }
            this.sending_flag = true;

            // 校验参数，保证输入框有数据填写
            this.check_phone();

            if (this.error_phone == true) {
                this.sending_flag = false;
                return;
            }
            // 向后端接口发送请求，让后端发送短信验证码
            axios.get(this.host + '/sms_codes/' + this.mobile + '/', {
                    responseType: 'json'
                })
                .then(response => {
                    // 表示后端发送短信成功
                    // 倒计时60秒，60秒后允许用户再次点击发送短信验证码的按钮
                    var num = 60;
                    // 设置一个计时器
                    var t = setInterval(() => {
                        if (num == 1) {
                            // 如果计时器到最后, 清除计时器对象
                            clearInterval(t);
                            // 将点击获取验证码的按钮展示的文本回复成原始文本
                            this.sms_code_tip = '获取短信验证码';
                            // 将点击按钮的onclick事件函数恢复回去
                            this.sending_flag = false;
                        } else {
                            num -= 1;
                            // 展示倒计时信息
                            this.sms_code_tip = num + '秒';
                        }
                    }, 1000, 60)
                })
                .catch(error => {
                    if (error.response.status == 400) {
                        this.error_phone_message = '短信验证码有误';
                    } else {
                        console.log(error.response.data);
                    }
                    this.sending_flag = false;
                })
        },

        // 登陆
        // 获取url路径参数
        get_query_string: function(name){
            let reg = new RegExp('(^|&)' + name + '=([^&]*)(&|$)', 'i');
            let r = window.location.search.substr(1).match(reg);
            if (r != null) {
                return decodeURI(r[2]);
            }
            return null;
        },
        // 检查数据
        check_login_name: function(){
            if (!this.login_name) {
                this.error_login_name = true;
            } else {
                this.error_login_name = false;
            }
        },
        check_login_pwd: function(){
            if (!this.login_password) {
                this.error_pwd_message = '请填写密码';
                this.error_pwd = true;
            } else {
                this.error_pwd = false;
            }
        },
        // 表单提交
        login_on_submit: function(){
            this.check_login_name();
            this.check_login_pwd();

            if (this.error_login_name == false && this.error_pwd == false) {
                axios.post(this.host+'/authorizations/', {
                        username: this.login_name,
                        password: this.login_password
                    }, {
                        responseType: 'json',
                        withCredentials: true
                    })
                    .then(response => {
                        // 使用浏览器本地存储保存token
                        if (this.remember) {
                            // 记住登录
                            sessionStorage.clear();
                            localStorage.token = response.data.token;
                            localStorage.user_id = response.data.user_id;
                            localStorage.username = response.data.username;
                            localStorage.avatar = response.data.avatar;
                        } else {
                            // 未记住登录
                            localStorage.clear();
                            sessionStorage.token = response.data.token;
                            sessionStorage.user_id = response.data.user_id;
                            sessionStorage.username = response.data.username;
                            sessionStorage.avatar = response.data.avatar;
                        }

                        // 跳转页面
                        let return_url = this.get_query_string('next');
                        if (!return_url) {
                            return_url = '/headline-login.html';
                        }
                        location.href = return_url;
                    })
                    .catch(error => {
                        if (error.response.status == 400) {
                            this.error_pwd_message = '用户名或密码错误';
                        } else {
                            this.error_pwd_message = '服务器错误';
                        }
                        this.error_pwd = true;
                    })
            }
        },
        qq_login: function(){
        var next = this.get_query_string('next') || '/';
        axios.get(this.host + '/oauth/qq/authorization/?next=' + next, {
                responseType: 'json'
            })
            .then(response => {
                location.href = response.data.login_url;
            })
            .catch(error => {
                console.log(error.response.data);
            })
        },
        wb_login: function(){
        var next = this.get_query_string('next') || '/';
        axios.get(this.host + '/oauth/wb/authorization/?next=' + next, {
                responseType: 'json'
            })
            .then(response => {
                location.href = response.data.login_url;
            })
            .catch(error => {
                console.log(error.response.data);
            })
        },
	},

});

