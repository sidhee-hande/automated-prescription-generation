<template>
  <div class="container management-margin all-entry">
    <div class="bg-vuepage management-compo">
      <div class="container">
        <div class="row">
          <div class="col-md-5 mt-4 ml-2">
            <div class="">
              <div class="large-ref-btn">
                <div>
                  <router-link to="/competitorstore" class="btn">
                    Competitor Stores
                  </router-link>
                  <span class="">
                    <router-link to="/nanboyastore" class="btn">
                      Nanboya Stores
                    </router-link>
                  </span>
                </div>
              </div>
            </div>
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
                patients Table
              </h5>

              <div class="row">
                <div class="col-md-9"></div>
                <div class="col-md-3">
                  <div class="input-icons">
                    <ul>
                      <i class="fas fa-search iconn"></i>
                      <input
                        type="text"
                        v-model="searchTerm"
                        class="searchbar input-field"
                        placeholder="Search via Email"
                      />
                    </ul>
                  </div>
                </div>
              </div>

              <div class="table-responsive">
                <table
                  id="PatientTable"
                  class="table align-items-center table-condensed"
                >
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Name</th>
                      <th>Prefecture</th>
                      <th>City</th>
                      <th>Postal Code</th>
                      <th>Phone Number</th>
                      <th>Email</th>
                      <!-- <th>Latitude</th>
                    <th>Longitude</th> -->
                      <th>Gender</th>
                      <th>D.O.B</th>
                      <th>Action</th>
                    </tr>
                  </thead>
                    <tbody>

                  <tr v-for="Patient in pageOfItems" :key="Patient.id">
                      <td>{{ Patient.id }}</td>
                      <td>
                        {{ Patient.first_name }} {{ Patient.last_name }}
                      </td>
                      <td>{{ Patient.prefecture }}</td>
                      <td>{{ Patient.city }}</td>
                      <td>{{ Patient.postal_code }}</td>
                      <td>{{ Patient.phone_number }}</td>
                      <td>{{ Patient.email }}</td>
                      <!-- <td>{{Patient.latitude}}</td>
                    <td>{{Patient.longitude}}</td> -->
                      <td>{{ Patient.gender }}</td>
                      <td>{{ Patient.date_of_birth }}</td>
                      <td>
                        <a v-on:click="editPatient(Patient)">
                          <i class="fas fa-edit text-info"></i>
                        </a>

                        <a v-on:click="deletePatient(Patient.email)">
                          <i class="fas fa-trash text-warning"></i>
                        </a>
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
                <jw-pagination
                  :items="patients"
                  @changePage="onChangePage"
                  :styles="customStyles"
                ></jw-pagination>
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
  created() {
    
  },
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
    allPatient() {
      axios
        .get("/api/patients")
        .then(({ data }) => (this.patients = data))
        .catch();
    },
    editPatient(cust) {
      this.$router.push({ name: "edit-Patient", params: { id: cust } });
    },
    deletePatient(email) {
      this.$router.push({ name: "delete-Patient", params: { id: email } });
    },

    generate() {
      window.open("/api/export/patients");
    },
  },
  mounted() {
    // if i use created() method here, then '/Patient' route will open it w/o even login
    this.allPatient();
  },
};
</script>