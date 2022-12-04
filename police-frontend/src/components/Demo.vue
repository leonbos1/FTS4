<template>
  <div class="content">
    <h3>Set text in Unity scene</h3>
    <input type="text" v-model="textInput"/>
    <button v-on:click="setText">Set</button>
  </div>
</template>
  
  <script>
export default {
  name: "DemoPage",
  components: {},

  data: function () {
    return {
      textInput: "",
    };
  },

  methods: {
    setText() {
      fetch("http://localhost:2000/demo", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ text: this.textInput }),
      })
        .then((response) => response.json())
    },
  },
  mounted() {},
};
</script>
  
  <style scoped>
</style>