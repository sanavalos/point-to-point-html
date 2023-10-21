
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
            .then(data => {console.log(data)
            
            
            this.datos= data;
           

            }
            )
            
           
        }

    },

    created() {
        this.fetchData(this.url)
    },




}).mount('#app')
