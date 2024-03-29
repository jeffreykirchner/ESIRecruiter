axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.xsrfCookieName = "csrftoken";


var app = Vue.createApp({

    delimiters: ['[[', ']]'],
       
    data(){return{   
        experiment : null,
        recruitment_params:{                          //recruiment parameters
                gender:[],
                actual_participants:0,
                registration_cutoff:0,
                experience_min:0,
                experience_max:1000,
                experience_constraint:false,
                institutions_exclude_all:0,
                institutions_include_all:0,
                experiments_exclude_all:0,
                experiments_include_all:0,
                allow_multiple_participations:false,
                institutions_exclude:[],
                institutions_include:[],
                experiments_exclude:[],
                experiments_include:[],
                trait_constraints:[],
            },
        recruitment_parameters_form_ids: {{recruitment_parameters_form_ids|safe}},
        confirmedCount:0,
        session:{confirmedCount:0},             //recruitment form parameter
        loading:true,
        buttonText1:'Update <i class="fas fa-sign-in-alt"></i>',                 //recruitment parameters update button text                   
    }},

    methods:{     

        //remove all the form errors
        clearMainFormErrors:function(){

            s = app.$data.recruitment_parameters_form_ids;
            for(var i in s)
            {
                $("#id_" + s[i]).attr("class","form-control");
                $("#id_errors_" + s[i]).remove();
            }
        },

        //update recruitment parameters 
        updateRecruitmentParameters: function(){                       
            axios.post('{{ request.path }}', {
                    status :"updateRecruitmentParameters" ,                                
                    formData : $("#updateRecruitmentParametersForm").serializeArray(),                                                              
                })
                .then(function (response) {     
                                                                           
                    status=response.data.status; 
                    app.clearMainFormErrors();

                    if(status=="success")
                    {                                 
                        window.open("{%url 'experimentView' experiment.id %}","_self");
                    }
                    else
                    {                                
                        app.displayErrors(response.data.errors);
                    }          

                    app.$data.buttonText1='Update <i class="fas fa-sign-in-alt"></i>';                      
                })
                .catch(function (error) {
                    console.log(error);
                    app.$data.searching=false;
                });                        
            },

        
        //gets experiment info from the server
        getExperiment: function(){
            axios.post('{{ request.path }}', {
                    status:"get",                                                              
                })
                .then(function (response) {                                                                   
                   
                    app.$data.recruitment_params = response.data.recruitment_params;    
                    app.$data.experiment = response.data.experiment;                            
                    app.$data.loading = false;
                })
                .catch(function (error) {
                    console.log(error);
                    //app.$data.searching=false;                                                              
                });                        
        },

        //if form is changed add * to button
        recruitmentFormChange:function(){
            app.$data.buttonText1='Update <i class="fas fa-sign-in-alt"></i> *';
        },

        //displays to the form errors
        displayErrors:function(errors){
            for(var e in errors)
            {
                $("#id_" + e).attr("class","form-control is-invalid")
                var str='<span id=id_errors_'+ e +' class="text-danger">';
                
                for(var i in errors[e])
                {
                    str +=errors[e][i] + '<br>';
                }

                str+='</span>';
                $("#div_id_" + e).append(str);  

                var elmnt = document.getElementById("div_id_" + e);
                elmnt.scrollIntoView();   
            }
        },
        
    },

    //run when vue is mounted
    mounted(){
        this.getExperiment();
    },                 

}).mount('#app');


