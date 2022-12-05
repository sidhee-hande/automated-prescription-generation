<script src="https://unpkg.com/axios/dist/axios.min.js"></script>
<template>
  <div class="container">
    <form @submit.prevent="submitForm">
      <span>Patient Name:</span><br>
      <input v-model="details.name" type="text"  placeholder="Enter patient's name" required/><br>
     
      <span>Patient Email:</span><br>
      <input v-model="details.email" type="email" placeholder="Enter patient's email" required/><br>
     
      <span>Patient Age:</span><br>
      <input v-model="details.age" type="number" placeholder="Enter patient's age" required/><br>
      <br>
      <input class="submit" type="submit" value="Submit">
    
    </form>
   <p style="color:white"> {{ message}} </p>
  </div>
</template>
 
<script>

import axios from 'axios';

export default {
    name: "add-patient",
  components: {},
  data() {
    return {
      message : " ",
      
      details: 
        {
          "name": " ", "age": " ",
          "email": " "
        }

      ,
     
      formSubmitted: false
    };
  },
  methods: {

    submitForm: function () {
      
      this.formSubmitted = true
      axios
        .post('https://prescriptiongeneratorserver.azurewebsites.net/api/addpatient',  { "patient": this.details} ).then( 
          response => this.message = response.data);

    },



  },
};
</script>
<style>
form {
  padding: 10px;
  border: 2px solid black;
  border-radius: 5px;
}

input {
  padding: 4px 8px;
  margin: 4px;
}

span {
  font-size: 18px;
  margin: 4px;
  font-weight: 500;
}

.submit {
    width: 40%;
  margin: 0 auto;
  color: white !important;
  background-image: linear-gradient(to bottom right, #fd7d96, #f16857);
  border: 0;
}
</style>

