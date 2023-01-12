<template>
  <div class="container">
    <div class="graph-container">
      <canvas id="graph"></canvas>
    </div>
    <div>
      <label for="distance">Hallway distance:</label>
    <input @change="drawGraph" type="text" v-model="distance" />
    <button @click="clearCache">Clear cache</button>
    <button id="refresh" @click="getData">Refresh</button>
  </div>
  </div>
  
</template>
  
  <script>

import Chart from "chart.js/auto";
import data from "../data.json";

export default {

  name: "GraphPage",
  components: {},

  data: function () {
    return {
      data: [],
      url: data.url,
      distance: 100,
      myChart: null,
    };
  },

  methods: {
    getData() {
      document.getElementById("refresh").disabled = true;

      fetch(this.url + "/measurement")
        .then((response) => response.json())
        .then((data) => (this.data = data))
        .then(() => this.mapData())
        .then(() => this.drawGraph())
        .then(() => {
          setTimeout(() => {
            document.getElementById("refresh").disabled = false;
          }, 1000);
        });
    },

    clearCache() {
      fetch(this.url + "/clear-cache", {
        method: "GET",
      })
        .then((response) => response.json())
        .then(() => this.getData())
    },

    drawGraph() {
      if (this.myChart) {
        this.myChart.destroy();
      }

      const ctx = document.getElementById("graph").getContext("2d");
  
      const activitydata = this.data.distance;
      const sounddata = this.data.sound;
      const labels = this.data.time;

      const plugin = {
        id: "customCanvasBackgroundColor",
        beforeDraw: (chart, args, options) => {
          const { ctx } = chart;
          ctx.save();
          ctx.globalCompositeOperation = "destination-over";
          ctx.fillStyle = options.color || "#99ffff";
          ctx.fillRect(0, 0, chart.width, chart.height);
          ctx.restore();
        },
      };

      this.myChart = new Chart(ctx, {
        type: "line",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Activity",
              data: activitydata,
              backgroundColor: ["rgba(255, 99, 132, 0.2)"],
              borderColor: ["rgba(255, 99, 132, 1)"],
              borderWidth: 1,
            },
            {
              label: "Sound",
              data: sounddata,
              backgroundColor: ["rgba(54, 162, 235, 0.2)"],
              borderColor: ["rgba(54, 162, 235, 1)"],
              borderWidth: 1,
            },
          ],
        },
        options: {
          plugins: {
            customCanvasBackgroundColor: {
              color: "white",
            },
          },
          scales: {
            y: {
              beginAtZero: true,
            },
          },
        },
        plugins: [plugin],
      });
      this.myChart;
    },
    mapData() {
      this.data.distance = this.data.map((item) => {
        if (item.distance < this.distance) {
          return 150;
        } else {
          return 0;
        }
      });
      this.data.time = this.data.map((item) => {
        return item.time;
      });
      this.data.sound = this.data.map((item) => {
        return item.sound;
      });
    },
  },
  mounted() {
    this.getData();
  },
};
</script>
  
  <style scoped>
.graph-container {
  width: 100%;
  height: 60vh;
  text-align: center;
}
.container {
  text-align: center;
  width: 80%;
}
button {
  margin: 10px;
}
</style>