<template>
  <div class="manage">
    <h1>Manage Sensors</h1>
    <table>
      <tr>
        <th>ID</th>
        <th>Name</th>
        <th>Room</th>
      </tr>

      <tr v-for="sensor in sensors" v-bind:key="sensor.id">
        <td>{{ sensor.id }}</td>
        <td><input v-model="sensor.name" /></td>
        <td>
          <select v-model="sensor.room_id">
            <option v-for="room in rooms" :value="room.id" :key="room.id">
              {{ room.name }}
            </option>
          </select>
        </td>

        <button class="edit" v-on:click="editSensor(sensor.id)">Edit</button>
        <button class="delete" v-on:click="deleteSensor(sensor.id)">Delete</button>
      </tr>
      <tr>
        <td></td>
        <td><input v-model="newSensor.name" /></td>
        <td>
          <select v-model="newSensor.room_id">
            <option v-for="room in rooms" :value="room.id" :key="room.id">
              {{ room.name }}
            </option>
          </select>
        </td>

        <button class="add" v-on:click="addSensor()">Add</button>
      </tr>
    </table>
  </div>
</template>

<script>
export default {
  name: "ManageSensorsPage",
  components: {},

  data: function () {
    return {
      data: [],
      sensors: [],
      newSensor: {
        location: "",
      },
      rooms: [],
    };
  },

  methods: {
    getData() {
      fetch("http://localhost:2000/sensors")
        .then((response) => response.json())
        .then((data) => (this.sensors = data));
    },

    editSensor(id) {
      fetch("http://localhost:2000/sensors", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.sensors.find((sensor) => sensor.id == id)),
      })
        .then((response) => response.json())
        .then(() => this.getData());
    },

    deleteSensor(id) {
      fetch("http://localhost:2000/sensors", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.sensors.find((sensor) => sensor.id == id)),
      })
        .then((response) => response.json())
        .then(() => this.getData());
    }, 

    addSensor() {
      console.log(this.newSensor);
      fetch("http://localhost:2000/sensors", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        }, //geeft json object aan api, example: {"location": "Zp07/01"}
        body: JSON.stringify(this.newSensor),
      })
        .then((response) => response.json())
        .then(() => this.getData());
    },

    getRooms() {
      fetch("http://localhost:2000/rooms")
        .then((response) => response.json())
        .then((data) => (this.rooms = data));
    },
  },

  mounted() {
    this.getData();
    this.getRooms();
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

select {
    width: 6vw;
    padding: 5px 20px;
    margin: 8px 0;
    display: inline-block;
    border: 1px solid #ccc;
    border-radius: 4px;
    box-sizing: border-box;
}
</style>