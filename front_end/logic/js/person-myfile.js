/**
 * Created by python on 19-8-30.
 */
var vm = new Vue({
    el: '#edit',
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
        error_mobile: false,
        error_email: false,
        // editing_address_index: '', // 正在编辑的地址在addresses中的下标，''表示新增地址
    },
    mounted: function(){
        axios.get(this.host + '/myfile/',{
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
                    this.gender =response.data.gender;
                    this.address =response.data.address;
            })
            .catch(error => {
                if (error.response.status==401 || error.response.status==403) {
                        location.href = '/person-loginsign.html';
                    }
            });
        //  //补充获取地址数据的请求
        // axios.get(this.host + '/edit/', {
        //         headers: {
        //             'Authorization': 'JWT ' + this.token
        //         },
        //         responseType: 'json'
        //     })
        //     .then(response => {
        //         this.addresses = response.data.addresses;
        //         this.limit = response.data.limit;
        //         this.default_address_id = response.data.default_address_id;
        //     })
        //     .catch(error => {
        //         if (error.response.status==401 || error.response.status==403) {
        //                 location.href = '/person-loginsign.html';
        //             }
        //     });
    },
   // 用户详情编辑
    show_add: function () {
        this.change = true
    },
    // 取消编辑
    cancel: function () {
        this.change = false
    },
    // 保存编辑
    change_user_info: function () {
        alert('开始发送请求')
        axios.patch(this.host + '/myfile/', {
            user: this.user_id,
            mobile: this.mobile,
            email: this.email,
            live_city: this.live_city,
            birthday: this.birthday,
            gender: this.gender,
            username: this.username,
            graduation: this.graduation,
            address: this.address,

        }, {
            headers: {
                'Authorization': 'JWT ' + this.token
            },
            responseType: 'json',
            withCredentials: true
        }).then(response => {
            // 修改成功
            alert("保存成功")
            this.change = false
            // this.show_user_detail()
        })
            .catch(error => {
                    // 修改失败
                    alert("请求失败")
                }
            )
    },
    methods: {
        // 退出
        logout: function(){
            sessionStorage.clear();
            localStorage.clear();
            location.href = '/headline-logined.html';
        },
        clear_all_errors: function(){
            // this.error_receiver = false;
            // this.error_mobile = false;
            this.error_place = false;
            this.error_email = false;
        },
        // 展示编辑地址界面
        show_edit: function(index){
            this.clear_all_errors();
            this.editing_address_index = index;
            // 只获取数据，防止修改form_address影响到addresses数据
            this.form_address = JSON.parse(JSON.stringify(this.addresses[index]));
            this.is_show_edit = true;
        },
        check_mobile: function(){
            var re = /^1[345789]\d{9}$/;
            if(re.test(this.form_address.mobile)) {
                this.error_mobile = false;
            } else {
                this.error_mobile = true;
            }
        },
        check_email: function(){
            if (this.form_address.email) {
                var re = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/;
                if(re.test(this.form_address.email)) {
                    this.error_email = false;
                } else {
                    this.error_email = true;
                }
            }
        },
        // 保存地址
        save_address: function(){
            if (this.error_mobile || this.error_email ) {
                alert('信息填写有误！');
            } else {
                this.form_address.title = this.form_address.receiver;
                if (this.editing_address_index === '') {
                    // 新增地址
                    axios.post(this.host + '/edit/', this.form_address, {
                        headers: {
                            'Authorization': 'JWT ' + this.token
                        },
                        responseType: 'json'
                    })
                    // .then(response => {
                    //     // 将新地址添加大数组头部
                    //     this.addresses.splice(0, 0, response.data);
                    //     this.is_show_edit = false;
                    // })
                    // .catch(error => {
                    //     console.log(error.response.data);
                    // })
                } else {

                    // 修改地址
                    axios.put(this.host + '/addresses/' + this.addresses[this.editing_address_index].id + '/', this.form_address, {
                        headers: {
                            'Authorization': 'JWT ' + this.token
                        },
                        responseType: 'json'
                    })
                    .then(response => {
                        this.addresses[this.editing_address_index] = response.data;
                        this.is_show_edit = false;
                    })
                    .catch(error => {
                        alert(error.response.data.detail || error.response.data.message);
                    })
                }
            }
        },


    }
})