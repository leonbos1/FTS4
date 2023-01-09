<template>
  <div class="manage">
    <div class="toggle-div">
      <button class="toggle-btn" @click="turnOffSituations()">
        <span>Stop all situations</span>
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
            <th>Occupants</th>
            <th>Start time</th>
          </tr>
          <tr v-for="situation in ongoingSituations" v-bind:key="situation.id">
            <td>{{ situation.room_name }}</td>
            <td>{{ situation.situation }}</td>
            <td>{{ situation.occupants }}</td>
            <td>{{ situation.time }}</td>
            <td>
              <button class="delete" @click="deleteSituation(situation.id)">
                Stop
              </button>
           <!-- for testing   <button class="delete" @click="generate(situation.id)">
                Generate
              </button> -->
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
    this.getData();
  },

  data: function () {
    return {
      data: [],
      dataGenerator: false,
      url: "http://127.0.0.1:2000",
      newSituation: {
        location: "",
      },
      rooms: [],
      situations: ["Fire", "Intruder", "Medical emergency", "Hostage"],
      selectedRoom: "",
      selectedSituation: "",
      ongoingSituations: [],
    };
  },

  methods: {
    generate(situation_id) {
      fetch(this.url + "/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          situation_id: situation_id,
        }),
      })
        .then(() => this.getData());
    },

    turnOffSituations() {
      fetch("http://localhost:2000/situations", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          all: true,
        })
      })
        .then((response) => response.json())
        .then(() => this.getData());
    },

    getData() {
      fetch("http://localhost:2000/situations")
        .then((response) => response.json())
        .then((data) => (this.ongoingSituations = data))
        //.then(() => console.log(this.ongoingSituations));
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

    getRoomKey(roomName) {
    return this.rooms.find((room) => room.name === roomName).id;
    },

    getRooms() {
      fetch(this.url + "/rooms")
        .then((response) => response.json())
        .then((data) => (this.rooms = data));
    },

    addSituation() {
      this.newSituation = {
        room_id: this.getRoomKey(this.selectedRoom),
        situation: this.selectedSituation,
        startTime: new Date().toLocaleTimeString(),
      };

      fetch("http://localhost:2000/situations", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.newSituation),
      })
        .then((response) => response.json())
        .then(() => this.getData());
    },

    deleteSituation(situation_id) {
      fetch("http://localhost:2000/situations", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          'all': false,
          'id': situation_id
        })
      })
        .then((response) => response.json())
        .then(() => this.getData());
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