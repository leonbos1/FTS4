<template>
<div>

    <table>

        <tr>
            <th>ID</th>
            <th>Location</th>
            
        </tr>

        <tr v-for="sensor in sensors" v-bind:key="sensor.id">
            <td>{{sensor.id}}</td>
            <td><input v-model="sensor.location"/></td>
            <button v-on:click="editSensor(sensor.id)">Edit</button>
            <button v-on:click="deleteSensor(sensor.id)">Delete</button>
        </tr>
        <tr>
            <td></td>
            <td><input v-model="newSensor.location"/></td>
            <button class="add" v-on:click="addSensor()">Add</button>
        </tr>


    </table>


</div>

</template>

<script>

export default {
  name: 'ManageSensorsPage',
  components: {
  },

  data: function () {
      return {
          data: [],
            sensors: [],
            newSensor: {
                location: ""
            }
      }
  },

    methods: {
        getData() {
            fetch("http://localhost:2000/sensors")
            .then(response => response.json())
            .then(data => this.sensors = data)
        },

        editSensor(id) {
            fetch("http://localhost:2000/sensors/" + id, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.sensors.find(sensor => sensor.id == id))
            })
            .then(response => response.json())
            .then(data => this.sensors = data)
        },

        deleteSensor(id) {
            fetch("http://localhost:2000/sensors/" + id, {
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.sensors.find(sensor => sensor.id == id))
            })
            .then(response => response.json())
            .then(data => this.sensors = data)
        }, 

        addSensor() {
            fetch("http://localhost:2000/sensors", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },    //geeft json object aan api, example: {"location": "Zp07/01"}
                body: JSON.stringify(this.newSensor)
            })
            .then(response => response.json())
            .then(data => this.sensors = data)
        }
    },

    mounted() {
        this.getData()
    }
}

</script>

<style>

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