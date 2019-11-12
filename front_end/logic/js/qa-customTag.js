/**
 * Created by python on 19-8-28.
 */

var vm = new Vue({
    el:"#app",
    data:{
        host:host,
        user_id: sessionStorage.user_id || localStorage.user_id,
        token: sessionStorage.token || localStorage.token,
        avatar:sessionStorage.avatar || localStorage.avatar,
        username:sessionStorage.username || localStorage.username,
        category_list:[],
    },
    mounted:function () {
        this.get_tag_category()
    },
    methods:{
        is_login:function () {
            if(this.user_id && this.token){
                return false
            }else {
                return true
            }
        },
        get_tag_category:function () {
            axios.get(this.host+'/tag_category/', {
                responseType: 'json',
            })
            .then(response => {
                console.log(response.data);
                this.category_list = response.data
            })
            .catch(error => {
                console.log(error.response.data);
            })
        }
    }
})