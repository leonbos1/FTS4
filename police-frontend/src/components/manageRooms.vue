<template>
  <div class="manage">
    <h1>Manage Rooms</h1>
    <table>
      <tr>
        <th>ID</th>
        <th>Location</th>
        <th></th>
      </tr>
      <tr v-for="room in rooms" v-bind:key="room.id">
        <td>{{ room.id }}</td>
        <td><input v-model="room.name" /></td>
        <button class="edit" v-on:click="editRoom(room.id)">Edit</button>
        <button class="delete" v-on:click="deleteRoom(room.id)">Delete</button>
      </tr>
      <tr>
        <td></td>
        <td><input v-model="newRoom.name" /></td>
        <button class="add" v-on:click="addRoom()">Add</button>
      </tr>
    </table>
  </div>
</template>

<script>
export default {
  name: "ManageRoomsPage",
  components: {},

  data: function () {
    return {
      data: [],
      rooms: [],
      newRoom: {
        location: "",
      },
      url: "http://ronleon.nl:2000",
    };
  },

  methods: {
    getData() {
      fetch(this.url+"/rooms")
        .then((response) => response.json())
        .then((data) => (this.rooms = data));
    },

    editRoom(id) {
      fetch(this.url+"/rooms", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.rooms.find((room) => room.id == id)),
      })
        .then((response) => response.json())
        .then(() => this.getData());
    },

    deleteRoom(id) {
      fetch(this.url + "/rooms", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.rooms.find((room) => room.id == id)),
      })
        .then((response) => response.json())
        .then(() => this.getData());
    },

    addRoom() {
      fetch(this.url+"/rooms", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.newRoom),
      })
        .then((response) => response.json())
        .then(() => this.getData());
    },
  },

  mounted() {
    this.getData();
  },
};
</script>

<style>

.manage {
    margin: 0 auto;
    background-color: #ffffff;
    border: 1px solid #000000;
    border-radius: 10px;
    padding: 20px;
    margin-top: 10vh;
    display: flex;
    flex-direction: column;
    align-items: center;
}

.add {
    background-color: #0011ff;
    color: white;
    padding: 5px 20px;
    margin: 8px 0;
    cursor: pointer;
    width: 5vw;
    border: none;
    border-radius: 4px;
}

.edit {
    background-color: #00bb0c;
    color: white;
    padding: 5px 20px;
    margin: 8px 0;
    cursor: pointer;
    width: 5vw;
    border: none;
    border-radius: 4px;
}

.delete {
    background-color: #ff0000;
    color: white;
    padding: 5px 20px;
    margin: 8px 0;
    cursor: pointer;
    width: 5vw;
    border: none;
    border-radius: 4px;
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

p {
    font-size: 1.5vw;
}



</style>