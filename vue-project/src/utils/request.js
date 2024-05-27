import axios from 'axios'
import router from '../router/index.js'
let tooken = ''
const request = axios.create({
  baseURL: 'http://localhost:5000',
  timeout: 5000,
  // 请求接口跨域是否需要凭证
  withCredentials: false, // 是否携带cookie（跨域请求时，需要后端设置允许携带cookie）
})
export default request
