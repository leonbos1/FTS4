import { createApp } from 'vue'
import App from './App.vue'
import Graph from './components/graph.vue'
import Home from './components/home.vue'
import { createRouter, createWebHistory } from 'vue-router' 

const routes = [
    { path: '/', component: Home },
    { path: '/graph', component: Graph }
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

createApp(App).use(router).mount('#app')
