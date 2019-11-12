/**
 * Created by python on 19-8-29.
 */
var vm = new Vue({
    el:"#app",
    data:{
        host:host,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        avatar:sessionStorage.avatar || localStorage.avatar,
        username:sessionStorage.username || localStorage.username,
        category_list: [],
        title: '',
        category_id: '',
        label: '',
        content: '',

    },
    mounted:function () {
        CKEDITOR.replace('editor1', {"filebrowerUploadUrl": this.host + "/ckeditor/upload/"});
        this.get_category()
    },
    methods:{
        add_news:function () {
          this.content = CKEDITOR.instances.content_text.getData();
          if (this.content == '') {
             alert("内容不能为空")
          }
          else if (this.title == ''){
              alert("标题不能为空")
          }
          else if (this.category_id == ''){
              alert("分类不能为空")
          }
          else if (this.label == ''){
              alert("标签不能为空")
          }

          else {

               axios({
                  url: this.host + '/headlines_add',
                  method: 'post',
                  data:{
                      "title": this.title,
                      "category": this.category_id,
                      "label": this.label,
                      "content": this.content,
                  },
                  headers: {
                      'Authorization': 'JWT ' + this.token
                  },
                  responseType: 'json',

        })
        .then(function(dat){
                alert('添加头条成功')
                location.href="./headline-login.html"
        })
        // .catch(function(){
        //     alert('请求失败')
        // })
          }

        },
         // 获取分类
        get_category:function(){
         axios({
            url:this.host + '/headlines_category',
            method:'get',
        })
        .then(function(dat){
            console.log(dat.data)
            vm.category_list = dat.data

        })
        .catch(function(){
            alert('请求失败')
        })
        },

    }
});