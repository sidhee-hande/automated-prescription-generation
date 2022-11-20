<template>
  <div>
    <form @submit.prevent="submitForm" v-if="!formSubmitted">
      <span>Patient Name:</span><br>
      <input v-model="name" type="text" placeholder="Enter your name" /><br>
      <span>Patient Date of Birth</span><br>
      <input v-model="email" type="email" placeholder="Enter your email" /><br>
      <span>Gender</span><br>
      <input type="radio" v-model="gender" value="Male" />
      <label>Male</label>
      <input type="radio" v-model="gender" value="Female" />
      <label>Female</label><br>

      <span>Symptoms</span><br>
      <input v-model="symptoms" type="text" placeholder="Symptoms" /><br>
      <span>Diagnosis:</span><br>
      <input v-model="Diagnosis" type="text" placeholder="Diagnosis" /><br>
      <span>Medicines:</span><br>
      <input v-model="Medicines" type="text" placeholder="Medicines" /><br>
      <input class="submit" type="submit" value="Submit">
    </form>
    <div v-if="formSubmitted">
      <h3>Form Submitted</h3>
      <p>Name: {{ name }}</p>
      <p>Email: {{ email }}</p>
      <p>Gender: {{ gender }}</p>
      <p>Symptoms: {{ symptoms }}</p>
      <p>Diagnosis: {{ Diagnosis }}</p>
      <p>Medicines: {{ Medicines }}</p>

    </div>
  </div>
</template>

<script>
import jsPDF from 'jspdf'
export default {
  data() {
    return {
      name: "",
      email: "",
      gender: "",
      symptoms: "",
      Diagnosis: "",
      Medicines: "",
      formSubmitted: false
    };
  },
  methods: {
    submitForm: function () {
      this.createPDF()
      this.formSubmitted = true
    },

    createPDF() {
      let pdfName = 'test';
      var doc = new jsPDF();
      doc.text("Name: " + this.name, 10, 10);
      doc.text("Email: " + this.email, 10, 20);
      doc.text("Gender: " + this.gender, 10, 30);
      doc.text("Symptoms: " + this.symptoms, 10, 40);
      doc.text("Diagnosis: " + this.Diagnosis, 10, 50);
      doc.text("Medicines: " + this.Medicines, 10, 60);
      doc.save(pdfName + '.pdf');
    }


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


<!-- <b-table :items="items" :fields="fields">
  <div id="app" class="container">
    <h1> PRESCRIPTION </h1>
    <form @submit="onSubmit" class="add-form">

      <div class="card">
        <div class="row">

          <div class="col-md-3">
            <label>Patient Name: </label>
            <b-form-input type="text" name="name" v-if="items[0].edit" v-model="items[0].name"
              class="mb-2 mr-sm-2 mb-sm-0">
            </b-form-input>
          </div>
        </div>
        <div class="row">
          <div class="col-md-3">
            <label>Patient Age: </label>
            <b-form-input type="text" name="age" v-if="items[0].edit" v-model="items[0].age"></b-form-input>
          </div>
        </div>
        <div class="row">
          <div class="col-md-3">
            <label>Date: </label>
            <b-form-input type="text" v-if="items[0].edit" v-model="items[0].date"></b-form-input>
          </div>

        </div>
        <br>
        <br>
        <div class="row">
          <div class="col">
            <label>Symptoms:</label>
            <b-form-input type="text" v-if="items[0].edit" v-model="items[0].symptoms"></b-form-input>
          </div>
        </div>
        <div class="row">
          <div class="col">
            <label> Diagnosis: </label>
            <b-form-input type="text" v-if="items[0].edit" v-model="items[0].diagnosis"> </b-form-input>

          </div>
        </div>

        <div class="row">
          <div class="col">
            <label> Medicines:</label>
            <b-form-input type="text" v-if="items[0].edit" v-model="items[0].medicines"></b-form-input>
          </div>
        </div>
        <div class="row">
          <div class="col">
            <label>Recommendation: </label>
            <b-form-input type="text" v-if="items[0].edit" v-model="items[0].dosageofmedication"></b-form-input>

            <b-form-input type="text" v-if="items[0].edit" v-model="items[0].frequencyofmedication"></b-form-input>
          </div>
        </div>
        <div class="row">
          <div class="col-md-8">

            <b-form-input type="text" v-model="items[0].signature"></b-form-input>

          </div>
        </div>
        <br>
      </div>
      <button @click="submit">Submit</button>
    </form>


    
      <template #cell(name)="data">
          <b-form-input v-if="items[data.index].isEdit" type="text" v-model="items[data.index].name"></b-form-input>
          <span v-else>{{data.value}}</span>
      </template>
      <template #cell(department)="data">
        <b-form-select v-if="items[data.index].isEdit" v-model="items[data.index].department" :options="['Development', 'Marketing', 'HR', 'Accounting']"></b-form-select>
        <span v-else>{{data.value}}</span>
      </template>
      <template #cell(age)="data">
          <b-form-input v-if="items[data.index].isEdit" type="number" v-model="items[data.index].age"></b-form-input>
          <span v-else>{{data.value}}</span>
      </template>
      <template #cell(dateOfBirth)="data">
        <b-form-datepicker v-if="items[data.index].isEdit" v-model="items[data.index].dateOfBirth"></b-form-datepicker>
        <span v-else>{{data.value}}</span>
      </template>
      <template #cell(edit)="data">
        <b-button @click="editRowHandler(data)">
          <span v-if="!items[data.index].isEdit">Edit</span>
          <span v-else>Done</span>
        </b-button>
      </template>



  </div>


<script>
export default {
  name: "HelloWorld",
  components: {},
  //{"1":{"age":"45 years old","date":"Mon, 07 Nov 2022 00:00:00 GMT","diagnosis":["Covid-19"],
  //"dosageofmedication":["100mg ibuprofen "],"frequencyofmedication":["ibuprofen twice daily "],
  //"medicines":["ibuprofen"],"name":"Jeff Bezos","symptoms":["chest pain","cough","fever"]}}
  data() {
    return {
      fields: [
        { key: "name", label: "Name" },
        { key: "date", label: "Date" },
        { key: "age", label: "Age" },
        { key: "symptoms", label: "Symptoms" },
        { key: "diagnosis", label: "Diagnosis" },
        { key: "medicines", label: "Medicines" },
        { key: "dosageofmedication ", label: "Dosage of Medication" },
        { key: "frequencyofmedication", label: "Frequency of Medication" },
        { key: 'edit', label: '' }
      ],
      items: [
        {
          "age": "45 years old", "date": "Mon, 07 Nov 2022", "diagnosis": "Covid-19",
          "dosageofmedication": "100mg ibuprofen ", "frequencyofmedication": "ibuprofen twice daily ",
          "medicines": "ibuprofen", "name": "Jeff Bezos", "symptoms": "chest pain,cough,fever", "edit": true, "signature": ""
        }

      ],
    };
  },
  mounted() {
    this.items = this.items.map(item => ({ ...item, isEdit: false }));
  },
  methods: {
    editRowHandler(data) {
      this.items[data.index].isEdit = !this.items[data.index].isEdit;
    },

  }
}
</script>

<style>
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
  background-color: #19191C;
  padding: 20px;
  display: relative;
  overflow: auto;
  color: white !important;
}
</style>

    </b-table> -->