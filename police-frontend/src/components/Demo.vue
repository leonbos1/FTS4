<template>
    <div class="content">
      <label for="postText">type text for demo</label>
      <input type="text" id ="postText" v-model="postText"/>
      <button v-on:click="test()">Set</button>
    </div>
</template>
  
<script>
import data from "../data.json";
export default {
  name: 'CreatePost',
  data(){
    return{
      formData:{
        postText:''
      },
      url: data.url,

    }
  },
  methods:{
    test(){
      // cors error
      fetch(this.url+"/demo", {
        method: "post",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          test:this.postText,
        })
      })

    }
  }

}

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