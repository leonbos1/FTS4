<template>
    <div class="container">
        <div class="graph-container">
            <canvas id="graph"></canvas>
        </div>
    </div>
  </template>
  
  <script>

import Chart from "chart.js/auto";

  export default {
    name: 'GraphPage',
    components: {
    },

    data: function () {
        return {
            data: []
        }
    },

    methods: {
        getData() {
            fetch("http://82.72.126.62:2000/distance")
            .then(response => response.json())
            .then(data => this.data = data)
            .then(() => this.mapData())
            .then(() => this.drawGraph())

        },
        drawGraph() {
            const ctx = document.getElementById('graph').getContext('2d');

            const activitydata = this.data.distance
            const sounddata = this.data.sound
            const labels = this.data.time

            const myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Activity',
                        data: activitydata,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                        ],
                        borderWidth: 1
                    },
                    {
                        label: "Sound",
                        data: sounddata,
                        backgroundColor: [
                            'rgba(54, 162, 235, 0.2)',
                        ],
                        borderColor: [
                            'rgba(54, 162, 235, 1)',
                        ],
                        borderWidth: 1
                    }
                
                ]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
            myChart
        },
        mapData() {
            //average of last 20 distances
            /*
            let hallwaywidth;
            for (let i = 0; i < 50; i++) {
                hallwaywidth += this.data.distance[i]
            }
            hallwaywidth = hallwaywidth / 50
            console.log(hallwaywidth)
            */
            
            
            this.data.distance = this.data.map((item) => {
                if (item.distance < 40) {
                    return 500
                } else {
                    return 0
                }
            })
            this.data.time = this.data.map((item) => {
                return item.time
            })
            this.data.sound = this.data.map((item) => {
                return item.sound
            })
        }
    },
    mounted() {
        this.getData()
    }

  }
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
  </style>