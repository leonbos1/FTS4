<template>
  <div id="app">
    <div class="bg"></div>
    <div id="nav">
      <ul>
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/graph">Graph</router-link></li>
        <li><router-link to="/manage-sensors">Manage Sensors</router-link></li>
        <li><router-link to="/manage-rooms">Manage Rooms</router-link></li>
        <li><router-link to="/control-panel">Control panel</router-link></li>
        <li><router-link to="/demo">Demo</router-link></li>

      </ul>
    </div>
    <div class="container">
    <router-view/>
    </div>
  </div>
</template>

<script>
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
  color: #000000;
  margin-top: 0px;
  /* background-image: url("../public/background.png");
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  background-attachment: fixed; */
  height: 100%;
  width: 100%;
  position: fixed;
  
}

ul {
  list-style-type: none;
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: #333;
}

li {
  float: left;
}

li a {
  display: block;
  color: white;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
}

li a:hover:not(.active) {
  background-color: #111;
}

.active {
  background-color: #04AA6D;
}

div .nav {
  background-color: #333;
  overflow: hidden;
}

body {
  margin: 0;
  font-family: Arial, Helvetica, sans-serif;
}

.container {
  padding: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.bg {
  background-image: url("../public/background.png");
  background-repeat: no-repeat;
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  height: 100%;
  width: 100%;
  position: fixed;
  z-index: -1;
  filter: blur(5px);
  -webkit-filter: blur(5px);
}

</style>
