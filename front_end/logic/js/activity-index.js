/**
 * Created by python on 19-8-25.
 */

var app = new Vue({
    el: '#app',
    data:{
        host:host,
    //    页面需要使用的数据
        activities:[]
    },
    computed:{
    //    需要通过计算得到的数据
    },
    mounted:function () {
    //    一加载就需要做的

        axios.get(this.host + '/activities/').

        then(response => {
            // console.info(response.data)
            this.activities = response.data.results
            console.log(this.activities)
            // alert(this.activity)
        }).
        catch(error => {
            alert('error')
        })
    },
    methods:{
    //
    }
});
