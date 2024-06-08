import './assets/myself.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import request from './utils/request'
import 'ace-builds/src-noconflict/theme-monokai';

request.get('/hello').then(res => {
  console.log(res)
})

const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}
app.use(router)
app.config.globalProperties.$systemId = ref({});
app.mount('#app')
