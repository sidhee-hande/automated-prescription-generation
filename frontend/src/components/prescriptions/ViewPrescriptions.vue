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
                class="text-left text-black font-weight-bold"
                style="margin-bottom: -25px"
              >
                Prescriptions Table
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
                      <button v-on:click="searchprescription(searchTerm)"> Search</button>
                 
                </div>
              </div>

              <div class="table-responsive">
                <table
                  id="prescriptionTable"
                  class="table align-items-center table-condensed"
                >
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Patient ID</th>
                      <th>Name</th>
                      <th>Email</th>
                     <th>Age</th>
                     <th>Date</th>
                      <th>Symptoms</th>
                     <th>Diagnosis</th>
                     <th>Medicines</th>
                     <th>Dosage</th>
                    </tr>
                  </thead>
                    <tbody>

                  <tr v-for="prescription in prescriptions" :key="prescription.id">
                      <td>{{ prescription.id }}</td>
                       <td>{{ prescription.patient_id }}</td>
                      <td>
                        {{ prescription.name }} 
                      </td>
                     
                      <td>{{ prescription.email }}</td>
                      
                      <td>{{ prescription.age}}</td>
                      <td>{{ prescription.date}}</td>
                      <td>{{ prescription.symptoms}}</td>
                      <td>{{ prescription.diagnosis}}</td>
                      <td>{{ prescription.medicines}}</td>
                      <td>{{ prescription.dosageofmedication}}</td>
                      
                     

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
                  :items="prescriptions"
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

  data() {
    const customStyles = {
  ul: {
    border: "2px solid rgba(101, 103, 119, 0.21)",
    background: "black",
  },
};
    return {
      prescriptions: [],
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
    
    allprescription() {
      axios
        .get("https://prescriptiongeneratorserver.azurewebsites.net/api/getprescriptiondata")
        .then(({ data }) => (this.prescriptions = data))
        .catch();
    },
     searchprescription(search_email) {
        if(search_email.length>0)
        {
      axios
        .post("https://prescriptiongeneratorserver.azurewebsites.net/api/searchprescriptiondata", {"email": search_email})
        .then(({ data }) => (this.prescriptions = data))
        .catch();
        }
    },

  },
  mounted() {
    // if i use created() method here, then '/prescription' route will open it w/o even login
    this.allprescription();
  },
};
</script>