 <template>
 <div>
 landing page will have patients list as a dropdown to choose from. 
 then redirect to Prescription page with the patient name and id autofilled. 
 Send it as a props in the component

 Add patient portal
    

    </div>
</template>

<script>
// import axios from 'axios'
export default {
  name: "Dashboard-Page",
  components: {},
  data() {
    return {
     isActive: false,
     enable: true,
     msg: 'Start Recording',
    }
  },
  mounted() {
      
  },
  methods: 
    {

      

    
  }
}
</script>

<style>
col {
  text-align: left !important;  
  align: left !important;
  width: fit-content;
  
}
#app {
  text-align: center;
  margin: 60px;
}
thead, tbody, tfoot, tr, td, th {
  text-align: left;
  width: 100px;
  vertical-align: middle;
}
pre {
  text-align: left;
  color: #d63384;
}


label {
  margin-bottom: 5px;
}
input[type="submit"] {
  width: 40%;
  margin: 0 auto;
  color: white !important;
  background-image: linear-gradient(to bottom right, #fd7d96, #f16857);
    border: 0;
}

.card {
          background-image: linear-gradient(to bottom right, grey, black);
    border: 0;
  padding: 5px;
  margin: auto;
  color: white !important;
  text-align: center;
}

.container {
  border-radius: 5px;
  border-color: black;
   background-color:#19191C;
  padding: 20px;
  display: relative;
  overflow: auto;
   color: white !important;
}
label {
color: white;
font-weight: bold;
display: block;
width: fit-content;
}

p {
  color: white;
font-weight: bold;
width: fit-content;


}
</style>