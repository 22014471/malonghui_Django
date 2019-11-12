/**
 * Created by python on 19-8-24.
 */
var sb = new Vue({
    el:'.mycollect-list',
    data:{
        host,
        numb:0,
        collect_news:[],
        collect_talks: [],
        user_id : sessionStorage.user_id || localStorage.user_id,
        username : sessionStorage.username || localStorage.username,
        token: sessionStorage.token || localStorage.token,
    },
    mounted:function () {
        this.get_collect_news(),
        this.get_collect_talks()
    },
    methods:{

        get_collect_news: function(){
            axios.get(this.host+'/collections/news/', {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    // params: {
                    //     page: this.page,
                    //     page_size: this.page_size
                    // },
                    responseType: 'json'
                })
                .then(response => {
                    // this.count = response.data.count;
                    this.collect_news = response.data.results;
                    // for(var i=0; i<this.answers.length; i++){
                    //     this.answers[i].url = '/goods/' + this.skus[i].id + ".html";
                    // }
                })
                .catch(error => {
                    console.log(error.response.data);
                })
        },
        get_collect_talks: function(){
            axios.get(this.host+'/collections/talks/', {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    // params: {
                    //     page: this.page,
                    //     page_size: this.page_size
                    // },
                    responseType: 'json'
                })
                .then(response => {
                    // this.count = response.data.count;
                    this.collect_talks = response.data.results;
                    // for(var i=0; i<this.answers.length; i++){
                    //     this.answers[i].url = '/goods/' + this.skus[i].id + ".html";
                    // }
                })
                .catch(error => {
                    console.log(error.response.data);
                })
        },
        // 退出
        logout: function(){
            sessionStorage.clear();
            localStorage.clear();
            location.href = '/headline-login.html';
        },
    }

})
