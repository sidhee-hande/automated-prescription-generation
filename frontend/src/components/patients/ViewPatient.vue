<template>
  <div class="container management-margin all-entry">
    <div class="bg-vuepage management-compo">
      <div class="container">
        <div class="row">
          <div class="col-md-5 mt-4 ml-2">
            <div class="">
              <div class="large-ref-btn">
                
              </div>
            </div>
          </div>

          <div class="col-md-3"></div>

        </div>

        <!-- <br> -->
        <div class="row">
          <div class="col-lg-12 mb-4">
            <!-- Simple Tables -->

            <div class="card table-card action-col">
              <div class="card-header justify-content-between"></div>
              <h5
                class="text-left text-white font-weight-bold"
                style="margin-bottom: -25px"
              >
                Patients Table
              </h5>

              <div class="row">
                <div class="col-md-9"></div>
                <div class="col-md-3">
                    <ul>
                      <input
                        type="text"
                        v-model="searchTerm"
                        class="searchbar input-field"
                        placeholder="Search via Email"
                      />
                    </ul>
                      <button v-on:click="searchpatient(searchTerm)"> Search</button>
                 
                </div>
              </div>

              <div class="table-responsive">
                <table
                  id="patientTable"
                  class="table align-items-center table-condensed"
                >
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Name</th>
                      <th>Email</th>
                     <th>Age</th>
                    </tr>
                  </thead>
                    <tbody>

                  <tr v-for="patient in patients" :key="patient.id">
                      <td>{{ patient.id }}</td>
                      <td>
                        {{ patient.name }} 
                      </td>
                     
                      <td>{{ patient.email }}</td>
                      
                      <td>{{ patient.age}}</td>
                      <td>
                        <button v-on:click="generateprescription( patient.id, patient.name, patient.age, patient.email)" >
                          Generate prescription
                        </button>

                        <!-- <a v-on:click="deletepatient(patient.email)">
                          <i class="fas fa-trash text-warning"></i>
                        </a> -->
                      </td>

                  </tr>
                  </tbody>
                </table>
               
              </div>
            </div>
          </div>
        </div>

        <!--Row-->
        <div class="row">
          <div class="col-sm-12 col-md-5"></div>
          <div class="col-sm-12 col-md-7">
            <ul class="pagination">
              <li class="pagination-bg">
                <!-- <jw-pagination
                  :items="patients"
                  @changePage="onChangePage"
                  :styles="customStyles"
                ></jw-pagination> -->
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script type="text/javascript">

import axios from "axios";
export default {
//   created() {
//     if (!User.loggedIn()) {
//       this.$router.push({ name: "/" });
//     }
//   },
  data() {
    const customStyles = {
  ul: {
    border: "2px solid rgba(101, 103, 119, 0.21)",
    background: "black",
  },
};
    return {
      patients: [],
      searchTerm: "",
      pageOfItems: [],
      customStyles
    };
  },
  computed: {
 
  },

  methods: {
    onChangePage(pageOfItems) {
      // update page of items
      this.pageOfItems = pageOfItems;
    },
    generateprescription(id,name, age, email) {
        this.$router.push({ name: "Prescription", params: { id: id, name: name, age: age, email: email } });
    },
    allpatient() {
      axios
        .get("http://localhost:5000/api/getpatientdata")
        .then(({ data }) => (this.patients = data))
        .catch();
    },
     searchpatient(search_email) {
        if(search_email.length>0)
        {
      axios
        .post("http://localhost:5000/api/searchpatientdata", {"email": search_email})
        .then(({ data }) => (this.patients = data))
        .catch();
        }
    },
    editpatient(cust) {
      this.$router.push({ name: "edit-patient", params: { id: cust } });
    },
    deletepatient(email) {
      this.$router.push({ name: "delete-patient", params: { id: email } });
    },
  

    // generate() {
    //   window.open("/api/export/patients");
    // },
  },
  mounted() {
    // if i use created() method here, then '/patient' route will open it w/o even login
    this.allpatient();
  },
};
</script>