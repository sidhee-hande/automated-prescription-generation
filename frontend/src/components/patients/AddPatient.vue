<script src="https://unpkg.com/axios/dist/axios.min.js"></script>
<template>
  <div>
    <form @submit.prevent="submitForm">
      <span>Patient Name:</span><br>
      <input v-model="details.name" type="text" placeholder="Enter patient's name" /><br>
      <span>Patient Email:</span><br>
      <input v-model="details.email" type="email" placeholder="Enter patient's email" /><br>
     
      <span>Patient Age:</span><br>
      <input v-model="details.age" type="text" placeholder="Enter patient's age" /><br>
      <input class="submit" type="submit" value="Submit">
    
    </form>
   <p> {{ message}} </p>
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
        .post('http://localhost:5000/api/addpatient',  { "patient": this.details} ).then( 
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
  font-size: 15px;
  color: #fff;
  background: #222;
  padding: 6px 12px;
  border: none;
  margin-top: 8px;
  cursor: pointer;
  border-radius: 5px;
}
</style>

