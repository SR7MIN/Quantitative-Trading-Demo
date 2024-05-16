<template>
    <div class="main-page">
      <header>
        <h1>金融交易平台</h1>
        <nav>
          <ul>
            <li><a href="#">首页</a></li>
            <li><a href="#">交易</a></li>
            <li><a href="#">账户</a></li>
            <li><a href="#">新闻</a></li>
            <li><a href="#">关于</a></li>
          </ul>
        </nav>
      </header>
      <section class="hero">
        <h2>欢迎来到金融交易平台</h2>
        <p>开始您的交易之旅，获取投资收益！</p>
        <button @click="register">立即注册</button>
      </section>
      <section class="features">
        <h2>我们的特点</h2>
        <div class="feature" v-for="(feature, index) in features" :key="index">
          <i :class="feature.icon"></i>
          <h3>{{ feature.title }}</h3>
          <p>{{ feature.description }}</p>
        </div>
      </section>
      <footer>
        <p>版权所有 &copy; 2024 金融交易平台</p>
      </footer>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  
  export default {
    name: 'MainPage',
    setup() {
      const features = ref([
        { icon: 'fas fa-chart-line', title: '高效的交易', description: '利用先进的技术进行快速且高效的交易。' },
        { icon: 'fas fa-lock', title: '安全保障', description: '采用多层次的安全措施保护您的资金和信息安全。' },
        { icon: 'fas fa-credit-card', title: '多样化的交易产品', description: '提供多种投资产品和交易工具，满足不同投资者的需求。' }
      ]);
  
      const register = () => {
        // 处理注册逻辑
        console.log('注册功能待实现');
      };
  
      return {
        features,
        register
      };
    }
  }
  </script>
  
  <style scoped>
  /* 在这里添加样式 */
  </style>