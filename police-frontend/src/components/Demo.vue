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

button {
    background-color: blue;
    color: white;
    border: none;
    padding: 10px 20px;
    cursor: pointer;
    border-radius: 10px;
    margin-left: 10px;
}

input {
    width: 6vw;
    padding: 5px 20px;
    margin: 8px 0;
    display: inline-block;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
}

</style>