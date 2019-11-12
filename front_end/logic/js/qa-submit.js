var vm = new Vue({
    el:"#app",
    data:{
        host,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        avatar:sessionStorage.avatar || localStorage.avatar,
        username:sessionStorage.username || localStorage.username,
        tags:'',
        content:null,
        title:null,
        question_id:null,
        show:true
    },
    mounted:function () {
        CKEDITOR.replace('editor1', {"filebrowerUploadUrl": this.host+"/ckeidtor/upload"});
        this.question_id = get_query_string('question_id');
        if (this.question_id){
            this.get_question();
            this.show=false;
        }
    },
    methods:{
        select_submit_type:function (show) {
            if(show){
                this.submit_question()
            }else {
                this.eidt_question()
            }
        },
        get_question:function () {
            if (this.question_id) {
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
                CKEDITOR.instances.content_text.setData(response.data.content);
                this.title = response.data.title;
                var question_tags = response.data.question_tags;
                let index;
                for (index in question_tags){
                    this.tags += question_tags[index].name
                }
            })
            .catch(error => {
                console.log(error.response.data);
            })
            }
        },
        submit_question:function () {
            this.content = CKEDITOR.instances.content_text.getData();
            if(!this.content){
                alert("内容不能为空");
                location.reload()
            }
            else if (!this.title) {
                alert("标题不能为空");
                location.reload()
            }
            else if (!this.tags) {
                alert("标签不能为空");
                location.reload()
            }
            else {
                axios.post(this.host + "/question/", {
                    content: this.content,
                    tags: this.tags,
                    title: this.title,
                    category: 1,
                }, {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    responseType: 'json',
                    withCredentials: true
                })
                    .then(response => {
                        location.href = "/qa-logined.html"
                    })
                    .catch(error => {
                        console.log(error.response.data);
                        alert(error.response.data)
                    })
            }

        },
        eidt_question:function () {
            this.content = CKEDITOR.instances.content_text.getData();
            if(!this.content){
                alert("内容不能为空");
            }
            else if (!this.title) {
                alert("标题不能为空");
            }
            else if (!this.tags) {
                alert("标签不能为空");
            }
            else {
                axios.put(this.host+"/question/",{
                content:this.content,
                tags:this.tags,
                title:this.title,
                question_id:this.question_id,
            },{
                headers: {
                    'Authorization': 'JWT ' + this.token
                },
                responseType: 'json',
                withCredentials: true
            })
            .then(response => {
                console.log(response.data);
                alert(response.data.id)
                var question_id=response.data.id;
                location.href="/qa-detail.html?question_id="+question_id
            })
            .catch(error => {
                console.log(error.response.data);
                alert(error.response.data)
            })
            }

        }
    }
});