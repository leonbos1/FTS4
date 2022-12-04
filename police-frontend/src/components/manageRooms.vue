<template>
  <div>
    <table>
      <tr>
        <th>ID</th>
        <th>Location</th>
      </tr>
      <tr v-for="room in rooms" v-bind:key="room.id">
        <td>{{ room.id }}</td>
        <td><input v-model="room.location" /></td>
        <button v-on:click="editRoom(room.id)">Edit</button>
        <button v-on:click="deleteRoom(room.id)">Delete</button>
      </tr>
      <tr>
        <td></td>
        <td><input v-model="newRoom.location" /></td>
        <button v-on:click="addRoom()">Add</button>
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
    };
  },

  methods: {
    getData() {
      fetch("http://localhost:2000/rooms")
        .then((response) => response.json())
        .then((data) => (this.rooms = data));
    },

    editRoom(id) {
      fetch("http://localhost:2000/rooms/" + id, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.rooms.find((room) => room.id == id)),
      })
        .then((response) => response.json())
        .then((data) => (this.rooms = data));
    },

    deleteRoom(id) {
      fetch("http://localhost:2000/rooms/" + id, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.rooms.find((room) => room.id == id)),
      })
        .then((response) => response.json())
        .then((data) => (this.rooms = data));
    },

    addRoom() {
      fetch("http://localhost:2000/rooms", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.newSensor),
      })
        .then((response) => response.json())
        .then((data) => (this.rooms = data));
    },
  },

  mounted() {
    this.getData();
  },
};
</script>

<style>
</style>