<template>
  <div class="home">
    <div class="hero-section">
      <h1>量化投研，从智投开始</h1>
      <p>我们提供免费的交易模拟、量化数据、投研工具、在线交流社区</p>
      <div class="cta-buttons">
        <el-button type="success" @click="handle_signup">立即注册</el-button>
        <el-button plain @click="handle_login">登录</el-button>
      </div>
    </div>
    <div class="illustrations">
      <!-- Add your illustrations here. This is a placeholder. -->
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
function handle_login() {
  router.push('/login')
}
function handle_signup() {
  router.push('/sign_up')
}
</script>

<style scoped>
.home {
  display: flex; /* 新增的代码 */
  align-items: center; /* 新增的代码 */
  justify-content: flex-start; /* 新增的代码 */
  text-align: left; /* 修改的代码 */

  /* text-align: center; */
  padding: 50px 20px;
  background-image: url('../assets/金软背景图1.png');
  /* 新增的代码 */
  background-size: cover;
  /* 新增的代码 */
  background-position: center;
  /* 新增的代码 */
  height: 100vh;
}

.hero-section {
  margin-bottom: 50px;
}

.hero-section h1 {
  font-size: 48px;
  margin-bottom: 20px;
  color: white;
}

.hero-section p {
  font-size: 18px;
  margin-bottom: 30px;
  color: white;
}
.el-button {
  /* 添加以下代码来调整按钮的大小 */
  padding: 20px 35px;
  font-size: 14px;
}
.cta-buttons {
  display: flex;
  justify-content: left;
  gap: 20px;
}

.register-btn {
  background-color: #4caf50;
  color: white;
}

.login-btn {
  background-color: #f0f0f0;
  color: #1d2d50;
}
</style>
