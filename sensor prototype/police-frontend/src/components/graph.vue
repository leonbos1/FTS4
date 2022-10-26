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

            const data = this.data.distance
            const labels = this.data.time

            const myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Activity',
                        data: data,
                        backgroundColor: [
                            'rgba(255, 99, 132, 0.2)',
                        ],
                        borderColor: [
                            'rgba(255, 99, 132, 1)',
                        ],
                        borderWidth: 1
                    }]
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
            
            this.data.distance = this.data.map((item) => {
                if (item.distance < 100) {
                    return 0
                } else {
                    return 1
                }
            })
            this.data.time = this.data.map((item) => {
                return item.time
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