<template>
  <nav class="navbar">
    <div class="logo">JoinQuant</div>
    <ul class="nav-links">
      <li><a href="#">首页</a></li>
      <li><a href="#">策略研究</a></li>
      <li><a href="#">数据字典</a></li>
      <li><a href="#">社区</a></li>
      <li><a href="#">帮助</a></li>
      <li><a href="#">聚宽投资</a></li>
      <li><a href="#">本地数据</a></li>
    </ul>
    <div class="auth-buttons">
      <button class="register-btn">立即注册</button>
      <button class="login-btn">登录</button>
    </div>
  </nav>
</template>

<script setup></script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #1d2d50;
}

.logo {
  font-size: 24px;
  font-weight: bold;
}

.nav-links {
  list-style: none;
  display: flex;
  gap: 15px;
}

.nav-links li {
  display: inline;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-size: 18px;
}

.auth-buttons {
  display: flex;
  gap: 10px;
}

.register-btn,
.login-btn {
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  font-size: 16px;
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
