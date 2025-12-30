import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import TemplateList from './views/TemplateList.vue'
import TemplateEditor from './views/TemplateEditor.vue'
import TemplateRunner from './views/TemplateRunner.vue'

const routes = [
  { path: '/', component: TemplateList },
  { path: '/create', component: TemplateEditor },
  { path: '/edit/:id', component: TemplateEditor },
  { path: '/run/:id', component: TemplateRunner }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

createApp(App).use(router).mount('#app')
