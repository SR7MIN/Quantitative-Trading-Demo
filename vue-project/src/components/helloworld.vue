<template>
    <div class="home">
        <div class="hero-section">
            <h1>量化投研，从聚宽开始</h1>
            <p>我们提供免费的量化数据、投研工具、量化学习体系、在线交流社区</p>
            <div class="cta-buttons">
                <button class="register-btn">立即注册</button>
                <button class="login-btn">登录</button>
            </div>
        </div>
        <div class="illustrations">
            <!-- Add your illustrations here. This is a placeholder. -->
        </div>
    </div>
</template>

<script setup>


</script>

<style scoped>
.home {
    display: flex; /* 新增的代码 */
  align-items: center; /* 新增的代码 */
  justify-content: flex-start; /* 新增的代码 */
  text-align: left; /* 修改的代码 */

    /* text-align: center; */
    padding: 50px 20px;
    background-image: url('../assets/金软背景图2.jpg');
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

.cta-buttons {
    display: flex;
    justify-content: center;
    gap: 20px;
}

.register-btn,
.login-btn {
    padding: 15px 30px;
    border: none;
    cursor: pointer;
    font-size: 18px;
}

.register-btn {
    background-color: #4CAF50;
    color: white;
}

.login-btn {
    background-color: #f0f0f0;
    color: #1d2d50;
}
</style>