<template>
  <div id="app">
  <h1> THIS IS THE DASHBOARD</h1>
    <!-- <Prescription msg="Welcome to Your Vue.js App"/> -->
    <router-link to="/dashboard">Home</router-link> |
    <router-link to="/prescription">Prescription</router-link>
    <router-link to="/add-patient"> Add Patient </router-link>
      <router-view/>
  </div>
</template>

<script>
// import Prescription from './components/Prescription.vue'

export default {
  name: 'App',
  components: {
   
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
