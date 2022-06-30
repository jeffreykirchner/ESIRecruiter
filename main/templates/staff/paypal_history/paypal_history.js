axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";

var app = new Vue({
    delimiters: ['[[', ']]'],
    el: '#root',        
    data:{
        baseURL:'{{request.get_full_path}}',                                                                                                                 
              
        searchButtonText:'Search <i class="fas fa-search"></i>',

        //api
        errorMessage:"",
        history:[],
        startDate:"{{d_one_year}}",
        endDate:"{{d_today}}",

        //recruiter
        errorMessageRecruiter:"",
        historyRecruiter:[],
        startDateRecruiter:"{{d_one_year}}",
        endDateRecruiter:"{{d_today}}",
    },

    methods:{
        //get list of users based on search
        getHistory: function(){

            axios.post('{{request.get_full_path}}', {                            
                action: "getHistory",
                startDate: app.$data.startDate,
                endDate: app.$data.endDate,
                            
            })
            .then(function (response) {                         
                app.$data.history = response.data.history;
                app.$data.errorMessage = response.data.errorMessage;
                app.$data.searchButtonText = 'Search <i class="fas fa-search"></i>';
            })
            .catch(function (error) {
                console.log(error);                               
            }); 
        }, 

        getHistoryButton : function(){
            app.$data.searchButtonText = '<i class="fas fa-spinner fa-spin"></i>';
            this.getHistory();
        },

        //get list of users based on search
        getHistoryRecruiter: function(){
            app.$data.searchButtonText = '<i class="fas fa-spinner fa-spin"></i>';

            axios.post('{{request.get_full_path}}', {                            
                action: "getHistoryRecruiter",
                startDate: app.$data.startDateRecruiter,
                endDate: app.$data.endDateRecruiter,
                            
            })
            .then(function (response) {                         
                app.$data.historyRecruiter = response.data.history;
                app.$data.errorMessageRecruiter = response.data.errorMessage;
                app.$data.searchButtonText = 'Search <i class="fas fa-search"></i>';
            })
            .catch(function (error) {
                console.log(error);                               
            }); 
        },
      
    },
    
    mounted: function(){
        //this.getHistory();
    },
});