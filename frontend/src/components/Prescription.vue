<template>
  <div>
    <div>
      <button v-if="enable" class="ui button toggle" @click="toggle"> {{ this.msg }}</button>
    </div>
    <br>
    <div class="container">

      <p v-if="isActive"> Recording
        <vue-speech @onTranscriptionEnd="onEnd" />
      </p>
    </div>
    <div class="container">
      <label v-if="!enable">
        Transcript:
        {{ this.transcription }}
      </label>
    </div>
{{this.items}}
    <div id="pdf" class="container">
      <h1> PRESCRIPTION </h1>
      <div class="card">
        <div class="row">

          <div class="col-md-3">
            <div class="row">
              <div class="col">
                <label>Patient Name: </label>
              </div>
              <div class="col">
                <!-- <b-form-input type="text" v-if="items.edit" v-model="items.name" class="mb-2 mr-sm-2 mb-sm-0">
                </b-form-input> -->
                <p> {{ this.patientname}}</p>
              </div>
            </div>
          </div>
               <div class="col">
            <div class="row">
              <div class="col">
                <label>Patient ID: </label>
              </div>
              <div class="col">
                <!-- <b-form-input type="text" v-if="items.edit" v-model="items.name" class="mb-2 mr-sm-2 mb-sm-0">
                </b-form-input> -->
                <p> {{ this.patientid }}</p>
              </div>
            </div>
          </div>
          </div>
          <div class="row">
           <div class="col-md-3">
            <div class="row">
              <div class="col">
                <label>Patient Email: </label>
              </div>
              <div class="col">
                <!-- <b-form-input type="text" v-if="items.edit" v-model="items.name" class="mb-2 mr-sm-2 mb-sm-0">
                </b-form-input> -->
                <p> {{ this.patientemail}}</p>
              </div>
            </div>
          </div>
          </div>
        
          
        <div class="row">
          <div class="col-md-3">
            <div class="row">
              <div class="col">
                <label>Patient Age: </label>
              </div>
              <div class="col">
               <p> {{ this.patientage}}</p>
                <!-- <b-form-input type="text" v-if="items.edit" v-model="items.age"></b-form-input> -->
              </div>
            </div>

          </div>
        </div>
        <div class="row">
          <div class="col-md-3">
            <div class="row">
              <div class="col">
                <label>Date: </label>
              </div>
              <div class="col">
                <b-form-datepicker v-if="items.edit" v-model="items.date" :placeholder="items.date"></b-form-datepicker>
              </div>
            </div>
          </div>

        </div>
        <br>
        <br>
        <div class="row">
          <div class="col">
            <div class="row">
              <div class="col">
                <label>Symptoms:</label>
              </div>
              <div class="col">
                <b-form-input type="text" v-if="items.edit" v-model="items.symptoms"></b-form-input>
              </div>
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col">
            <div class="row">
              <div class="col">
                <label> Diagnosis: </label>
              </div>
              <div class="col">
                <b-form-input type="text" v-if="items.edit" v-model="items.diagnosis"> </b-form-input>
              </div>
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col">
            <div class="row">
              <div class="col">
                <label> Medicines:</label>
              </div>
              <div class="col">
                <b-form-input type="text" v-if="items.edit" v-model="items.medicines"></b-form-input>
              </div>
            </div>
          </div>
        </div>

        <div class="row">
          <div class="col">
            <div class="row">
              <div class="col">
                <label>Recommendation: </label>
              </div>
              <div class="col">
                <b-form-input type="text" v-if="items.edit" v-model="items.dosageofmedication"></b-form-input>

                <b-form-input type="text" v-if="items.edit" v-model="items.frequencyofmedication"></b-form-input>
              </div>
            </div>
          </div>
        </div>
        <!-- <div class="row">
    <div class="col-md-8">

    <b-form-input
    type="text"  v-model="items.signature"></b-form-input>

    </div>
     </div> -->
        <br>
      </div>
    </div>
    <h5>
      Once you are done editing the prescription, kindly click on the button below to sign and email it to the patient.
    </h5>
    <button class="submit" @click="saveprescription">
      Sign prescription
    </button>

  </div>
</template>

<script>
import emailjs from '@emailjs/browser';
import axios from 'axios'
import jsPDF from 'jspdf'
export default {
  name: "Prescription-Page",
  components: {},
  //{"1":{"age":"45 years old","date":"Mon, 07 Nov 2022 00:00:00 GMT","diagnosis":["Covid-19"],
  //"dosageofmedication":["100mg ibuprofen "],"frequencyofmedication":["ibuprofen twice daily "],
  //"medicines":["ibuprofen"],"name":"Jeff Bezos","symptoms":["chest pain","cough","fever"]}}
  data() {
    return {
      isActive: false,
      enable: true,
      msg: 'Start Recording',
      transcription: '',
      patientname: " ",
      patientemail: " ",
      patientid: " ",
      patientage: " ",
  
      //      items: [
      //       {"age":"45 years old","date":"Mon, 07 Nov 2022","diagnosis":"Covid-19",
      // "dosageofmedication":"100mg ibuprofen ","frequencyofmedication":"ibuprofen twice daily ",
      // "medicines":"ibuprofen","name":"Jeff Bezos","symptoms":"chest pain,cough,fever", "edit": true, "signature": ""}

      //       ],
      items: 
        {
          "patient_id": " ", "age": "", "email": " ",
           "date": " ", "diagnosis": " ",
          "dosageofmedication": " ", "frequencyofmedication": " ",
          "medicines": " ", "name": " ", "symptoms": " ", "edit": true, "signature": ""
        }

      ,
    }
  },
  mounted() {
   // this.items = this.items.map(item => ({ ...item, isEdit: false }));
    this.patientid = this.$route.params.id;
    this.patientname = this.$route.params.name;
    this.patientage = this.$route.params.age;
    this.patientemail = this.$route.params.email;
    this.items.patient_id= this.$route.params.id;
    this.items.name = this.$route.params.name;
    this.items.age= this.$route.params.age;
    this.items.email = this.$route.params.email;
  
  },
  methods:
  {
    sendEmail() {
      var contactParams = {
        patient_name: this.items.name,
        from_email: "automatedprescriptions@gmail.com",
        to_email: "skc86@cornell.edu"
      }
      emailjs.send('service_prgws4h', 'template_1xran0s', contactParams, 'wXlM_KPvNXTs0G7Kz')
        .then((result) => {
          console.log('SUCCESS!', result.text);
        }, (error) => {
          console.log('FAILED...', error.text);
        });
    },
    saveprescription() {
      this.sendEmail()
      this.createPDF()
       this.items.patient_id= this.patientid;
    this.items.name = this.patientname;
    this.items.age= this.patientage;
    this.items.email = this.patientemail;

      axios.post('http://localhost:5000/api/saveprescription',  { "prescription": this.items, 
      "patientname": this.patientname,
      "patientage" :  this.patientage,
      "patientemail": this.patientemail,
      "patientid": this.patientid
      } )
    },

    createPDF() {

      let pdf = new jsPDF('p', 'pt', 'a4');
      let pWidth = pdf.internal.pageSize.width; // 595.28 is the width of a4
      let srcWidth = document.getElementById('pdf').scrollWidth;
      let margin = 30; // narrow margin - 1.27 cm (36);
      let scale = (pWidth - margin * 2) / srcWidth;

      pdf.html(document.getElementById('pdf'), {
        x: margin,
        y: margin,
        html2canvas: {
          scale: scale,
        },
        callback: function () {
          pdf.save('Prescription.pdf')
        }
      });
    },

    editRowHandler(data) {
      this.items[data.index].isEdit = !this.items[data.index].isEdit;
    },
    onEnd({ lastSentence, transcription }) {
      // `lastSentence` is the last sentence before the pause
      // `transcription` is the full array of sentences
      console.log(lastSentence)
      console.log(transcription)
      this.transcription = transcription.join(" ")
      //send data to backend


    },
    toggle() {
      this.isActive = !this.isActive

      if (this.msg == "Start Recording") {
        this.msg = "Stop Recording"
      }
      else {
        this.enable = false
        axios.post('http://localhost:5000/api/generateprescription', { "transcript": this.transcription })
          .then(response => this.items = response.data);
     
    this.items.patient_id= this.patientid;
    this.items.name = this.patientname;
    this.items.age= this.patientage;
    this.items.email = this.patientemail;
    console.log(this.items)
      }
    },
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

thead,
tbody,
tfoot,
tr,
td,
th {
  text-align: left;
  width: 100px;
  vertical-align: middle;
}

pre {
  text-align: left;
  color: black !important;
}


label {
  margin-bottom: 5px;
  color: white !important;
}

input[type="submit"] {
  width: 40%;
  margin: 0 auto;
  color: white !important;
  background-image: linear-gradient(to bottom right, #fd7d96, #f16857);
  border: 0;
}

.card {

  border: 0;
  padding: 5px;
  margin: auto;
 
  text-align: center;
}

.container {
  border-radius: 5px;
  border-color: black;
  background-color: #19191C;
  padding: 20px;
  display: relative;
  overflow: auto;
  color: white !important;
}

label {
  color: black !important;
  font-weight: bold;
  display: block;
  width: fit-content;
}

p {
  color: black !important;
  font-weight: bold;
  width: fit-content;


}
</style>