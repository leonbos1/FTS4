<template>
  <div class="manage">
    <div class="toggle-div">
      <button class="toggle-btn" @click="toggleDatagenerator()">
        <span v-if="dataGenerator">Stop datagenerator</span>
        <span v-else>Start datagenerator</span>
      </button>
    </div>

    <div class="dropdown">
      <label for="rooms">Room</label>
      <select v-model="selectedRoom">
        <option v-for="room in rooms" :value="room.name" :key="room.id">
          {{ room.name }}
        </option>
      </select>
      <label for="situations">Situation</label>
      <select v-model="selectedSituation">
        <option
          v-for="situation in situations"
          :value="situation"
          :key="situation"
        >
          {{ situation }}
        </option>
      </select>
      <button class="add" @click="addSituation()">Add</button>
    </div>

    <div class="situations">
      <div class="ongoing-situations">
        <h1>Ongoing situations</h1>
        <table>
          <tr>
            <th>Room</th>
            <th>Situation</th>
            <th>Start time</th>
          </tr>
          <tr v-for="situation in ongoingSituations" v-bind:key="situation.id">
            <td>{{ situation.room_id }}</td>
            <td>{{ situation.situation }}</td>
            <td>{{ situation.startTime }}</td>
            <td>
              <button class="delete" @click="deleteSituation(situation.id)">
                Stop
              </button>
            </td>
          </tr>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "ControlPanelPage",
  components: {},

  mounted() {
    this.getRooms();
  },

  data: function () {
    return {
      data: [],
      dataGenerator: false,
      url: "http://127.0.0.1:2000",
      minPeople: 0,
      maxPeople: 10,
      rooms: [],
      situations: ["Fire", "Intruder", "Medical emergency", "Hostage"],
      selectedRoom: "",
      selectedSituation: "",
      ongoingSituations: [],
    };
  },

  methods: {
    toggleDatagenerator() {
      if (this.dataGenerator) {
        this.dataGenerator = false;
      } else {
        this.dataGenerator = true;
      }
    },

    // setAmountOfPeople() {
    //   fetch(this.url + "/people_amount", {
    //     methods: "POST",
    //     headers: {
    //       "Content-Type": "application/json",
    //     },
    //     body: JSON.stringify({
    //       min_people: this.minPeople,
    //       max_people: this.maxPeople,
    //     })
    //     .then((response) => response.json()),
    //   });
    // },

    getRooms() {
      fetch(this.url + "/rooms")
        .then((response) => response.json())
        .then((data) => (this.rooms = data));
    },

    addSituation() {
      //add room and situations to this.ongoingSituations
      this.ongoingSituations.push({
        id: this.ongoingSituations.length + 1,
        room_id: this.selectedRoom,
        situation: this.selectedSituation,
        startTime: new Date().toLocaleTimeString(),
      });
    },

    removeSituation(situation_id) {
      this.ongoingSituations = this.ongoingSituations.filter(
        (situation) => situation.id !== situation_id
      );
    },
  },
};
</script>

<style>
.situations {
  background-color: #ffffff;
  border: 1px solid #000000;
  border-radius: 10px;
  padding: 20px;
  margin-top: 1vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 40vw;
  height: 50vh;
  overflow: hidden;
}

.ongoing-situations {
    /*make scrollable when going outside of div*/
    overflow-y: scroll; 
    height: 100%;
    width: 100%;
}

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
  width: 50vw;
  height: 50vh;
}

/*when width is less than 450px
  make situations div 95% width */

@media screen and (max-width: 450px) {
    .situations {
        width: 95%;
    }

    .ongoing-situations {
        width: 100%;
    }

    .manage {
        width: 95%;
        margin: 0 auto;

    }

}

.toggle-btn {
  background-color: #0000ff;
  border: none;
  color: white;
  padding: 8px 25px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  cursor: pointer;
  border: 2px solid #0000ff;
  border-radius: 10px;
}

.dropdown {
  position: relative;
  display: inline-block;
}

select {
  margin: 10px;
}

table {
  border-collapse: collapse;
  width: 100%;
}

th,
td {
  text-align: left;
  padding: 8px;
}

tr:nth-child(even) {
  background-color: #f2f2f2;
}


</style>