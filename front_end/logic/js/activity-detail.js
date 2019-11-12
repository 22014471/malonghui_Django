let app = new Vue({
    el: "#app",
    data: {
        activity: [],
        now: 0,
        deadline: 0,
        last_ms: 0
    },
    mounted: function () {
        let id = 1
        let reg = new RegExp("(^|&)" + "id" + "=([^&]*)(&|$)", "i");
        let r = window.location.search.substr(1).match(reg);
        if (r != null) {
            id = r[2];
        }
        axios.get(host + "/activities/" + id + "/")
            .then(response => {
                // console.log(response.data)
                this.activity = response.data;
                console.log('111111111111111111' + this.activity)
                // response.headers.date
                this.now = new Date(response.headers.date).getTime();
                console.log('111111111111111111' + this.now)
                this.deadline = new Date(this.activity.deadline).getTime();
                console.log('111111111111111111' + this.deadline)
                setInterval(
                    //     function () {
                    //     this.now +=1000;
                    //     this.last_ma = this.now - this.deadline
                    // }
                    () => {
                        this.now += 1000;
                        this.last_ms = this.deadline - this.now

                    }
                    , 1000)
            })
            .catch(error => {
            })
    },

    methods: {},
    filters: {
        countdown2dhms: function (value_ms) {
            let seconds = value_ms / 1000
            let day = Math.floor(seconds / (60 * 60 * 24))
            let hour = Math.floor(seconds /(60*60)) % 24
            let minute = Math.floor(seconds /60) % 60
            let second =seconds % 60

            return day + "天" + hour + "时" + minute + "分" + second + "秒"
        }
    }
})