<template>
    <div>
        <button class="toggle" @click="toggleDatagenerator()">
            <span v-if="dataGenerator">Stop datagenerator</span>
            <span v-else>Start datagenerator</span>
        </button>
    </div>
</template>

<script>

export default {
    name: 'ControlPanelPage',   
    components: {
    },

    data: function () {
        return {
            data: [],
            dataGenerator: false,
            url: '127.0.0.1:2000',
            minPeople: 0,
            maxPeople: 10,
        }
    },

    methods: {
        toggleDatagenerator() {
            if (this.dataGenerator) {
                this.dataGenerator = false;
            } else {
                this.dataGenerator = true;
            }
        },

        setAmountOfPeople() {
            fetch(this.url+'/people_amount',{
                methods: 'POST',
                headers: {
                    'Content-Type':'application/json'
                },
                body: JSON.stringify({
                    'min_people': this.minPeople,
                    'max_people': this.maxPeople,
                })
                .then((response) => response.json())
                   
            }) 
        }


    }
}

</script>

<style>

.toggle {
    background-color: #0000ff;
    border: none;
    color: white;
    padding: 15px 32px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    border: 2px solid #0000ff;
    border-radius: 10px;
}

</style>