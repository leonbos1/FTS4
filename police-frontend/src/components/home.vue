<template>
  <div class="content">
    <div class="inline-content">
      <h1>Future of the police</h1>
      <p>
        Welcome to our project! We are using smart sensors and buildings to
        provide important information to police officers through the use of
        augmented reality glasses. Our system allows officers to access
        real-time data and make more informed decisions, helping to improve
        public safety and make our communities safer.
      </p>
      <p>
        With our system, officers quickly have access to advanced information.
        This information is give many details about the current situation and
        allows officers to make better decisions. With the help of our project,
        officers will be able to better calculate the risk of a situation.
      </p>
      <p>
        The system mainly gives information about the behaviour of the people in
        the building. This information is gathered by smart sensors that will
        most likely exist in the future. The sensors will be able to detect
        certain behaviours and will send this information to the police.
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: "HomePage",
  components: {},

  data: function () {
    return {
      data: [],
    };
  },
};
</script>


<style scoped>
.content {
  display: flexbox;
  margin: 0 auto;
  height: 60vh;
  padding: 20px;
  text-align: center;
  border-radius: 10px;
  background-color: #ffffff;
  box-shadow: 0 0 10px 0 rgba(0, 0, 0, 0.2);
  width: 80vw;
}

p {
  font-size: 1.2em;
}

@media screen and (max-width: 500px) {
  p {
    font-size: 0.8em;
  }
}
</style>