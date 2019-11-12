/**
 * Created by python on 19-8-29.
 */

// Vue.filter('str2date', function (value) {
//   return new Date(value)
// })

Vue.filter('date2md', function (value) {
    return (value.getMonth() + 1) + "月" + value.getDate() + '日'
})

var sb = new Vue({
    el:"#fuck",
    delimiters: ['[[', ']]'],
    data:{
        // 页面中需要使用到的数据，键值对
        host,
        numb:0,
        questions: [],
        activities: [],
        answers: [],
        user_id: localStorage.user_id || sessionStorage.user_id,
        avatar: localStorage.username || sessionStorage.username,
        username: localStorage.username || sessionStorage.username,
        token: sessionStorage.token || localStorage.token,

    },

    mounted:function () {
         this.get_questions(),
         this.get_answers(),
         this.get_activities()
    },
    methods:{
        // 需要用到的函数，键值对 ，键是名称，值是匿名函数
        get_questions: function(){
            axios.get(this.host+'/myquestions/', {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    responseType: 'json'
                })
                .then(response => {
                    this.questions = response.data.results;
                })
                .catch(error => {
                    console.log(error.response.data);
                })
        },

         get_activities: function(){
            axios.get(this.host+'/dynamics/', {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    responseType: 'json'
                })
                .then(response => {
                    this.activities = response.data.results;
                })
                .catch(error => {
                    console.log(error.response.data);
                })
        },

        get_answers: function(){
            axios.get(this.host+'/myanswers/', {
                    headers: {
                        'Authorization': 'JWT ' + this.token
                    },
                    responseType: 'json'
                })
                .then(response => {
                    this.answers = response.data.results;
                })
                .catch(error => {
                    console.log(error.response.data);
                })
        },

    },
})