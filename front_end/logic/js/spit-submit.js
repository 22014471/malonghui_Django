/**
 * Created by python on 19-8-29.
 */
let vm = new Vue({
    el: '#app',
    data:{
        host,
        username: sessionStorage.username || localStorage.username,
        token: sessionStorage.token || localStorage.token,
        content: "",
        headers:{},

    },
    mounted:  function () {
        CKEDITOR.replace('editor2',{"filebrowserUploadUrl": "http://127.0.0.1:8000/ckeditor/upload/"})


        //  向后端发送请求，首先判断是否存在token
        if(this.token){
            this.headers = {
                'Authorization': 'JWT ' + this.token
            }
        }

    },
    methods : {
        log_out:function () {
            sessionStorage.clear();
            localStorage.clear();
        },
        submit_complaint:function () {
            this.content=CKEDITOR.instances.editor2.getData()
            if(!this.token){
                location.href = '/headline-login.html?next=/spit-submit.html'
                return
            }
            if(this.content==''){
                alert('内容不能为空')
                return
            }

            axios.post(this.host + "/creation/talk/",
                {
                    "content": CKEDITOR.instances.editor2.getData()
                },
                {
                    headers: this.headers,
                    responseType: 'json'
                })
                .then(response =>{
                    //页面跳转

                    location.href = '/spit-index.html'
            })
            .catch(error => {

            })
        }
    }
})
// var vm = new Vue({
//     el: '#app',
//     data: {
//         host,
//         username: sessionStorage.username || localStorage.username,
//         user_id: sessionStorage.user_id || localStorage.user_id,
//         token: sessionStorage.token || localStorage.token,
//     },
//     mounted:function () {
//
//     },
//     methods:{
//         log_out:function () {
//             sessionStorage.clear();
//             localStorage.clear();
//         },
//         // 提交吐槽文本
//         submit_complaint: function () {
//             alert(this.input_content);
//             axios.post(this.host + "/creation/talk/", {
//                 content: this.input_content,
//             },  {
//                 headers: {
//                     'Authorization': 'JWT ' + this.token
//                 },
//                 responseType: 'json',
//                 withCredentials: true
//             })
//
//                 .then(response => {
//                      location.href = '/spit-index.html'
//                 })
//                 .catch(error => {
//                     console.log(error.response.data)
//                 });
//
//         }
//     }
//
//     // methods: {
//     //     // 提交吐槽文本
//     //     content_submit: function () {
//     //         alert(this.input_content);
//     //         axios.post(this.host + "/creation_tsukkomi/", {
//     //             content: this.input_content,
//     //         }, {
//     //             responseType: 'json'
//     //         })
//     //             .then(response => {
//     //
//     //             })
//     //             .catch(error => {
//     //                 console.log(error.response.data)
//     //             });
//     //
//     //     }
//     // }
// });

//     $(function() {
//         $(".content").submit(function () {
//             // var content = CKEDITOR.instances['content'].document.getBody().getText(); // 获取所有文本内容不包括链接
//             var content = CKEDITOR.instances['content'].getData(); // 获取所有文本内容
//             var token =  sessionStorage.token || localStorage.token;
//             var params = {
//                 "content": content,
//             };
//             if(token){$.ajax({
//                 url:host+"/creation/talk/",
//                 method: "post",
//                 data: JSON.stringify(params),
//                  headers: {
//                 'Authorization': 'JWT ' + token
//                         },
//                 contentType: "application/json",
//                 success: function (resp) {
//                     if (resp) {
//                         // 刷新当前界面
//                         alert("OK");
//                         // location.reload();
//                     } else {
//                         alert(resp.errmsg);
//                         // location.reload();
//                     }
//                 }
//             })}else{window.open('person-loginsign.html')}
//
//         })
// });

