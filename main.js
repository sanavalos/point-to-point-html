
const { createApp } = Vue
createApp({ 
    data(){
        return{
            error: false,
            url: "https://dolarapi.com/v1/dolares",
            datos:[]
        }
    }, 
    methods:{
        fetchData(url){
            fetch(url)
            .then(response => response.json())
            .then(data => {
            this.datos= data.filter(e => e.casa === "oficial" || e.casa === "blue" || e.casa === "mayorista");
            }
            )
        }
    },
    created() {
        this.fetchData(this.url)
    },
}).mount('#app')
