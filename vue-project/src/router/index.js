import { createRouter, createWebHistory } from 'vue-router';
import login from '../components/login.vue';
import Layout from '../components/index.vue';
import sign_up from '../components/sign_up.vue';
import helloworld from '@/components/helloworld.vue';
import strategy from '@/components/strategy.vue';
import risk_manage from '@/components/risk_manage.vue';
import user_setting from '@/components/user_setting.vue';
import shanghai from '@/components/shanghai.vue';

import feature from '@/components/feature.vue';

import trade_summary from '@/components/trade_summary.vue';
import exchange_rate from '@/components/exchange_rate.vue';
import internation from '@/components/internation.vue';
import trade_do from '@/components/trade_do.vue';
import trade_analyze from '@/components/trade_analyze.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: helloworld
    },
    {
      path: '/hello',
      component: helloworld
    },
    {
      path: '/login',
      name: 'login',
      component: login
    },
    {
      path: '/sign_up',
      name: 'sign_up',
      component: sign_up
    },
    {
      path: '/:index',
      name: 'index',
      component: Layout,
      children: [
        // UserHome will be rendered inside User's <router-view>
        // when /users/:username is matched
        { path: 'strategy', component: strategy },

        // UserProfile will be rendered inside User's <router-view>
        // when /users/:username/profile is matched
        { path: 'manage', component: risk_manage },

        // UserPosts will be rendered inside User's <router-view>
        // when /users/:username/posts is matched
        { path: 'setting', component: user_setting },

        { path: 'shanghai', component: shanghai },
          
        { path: 'feature', component: feature },
  
        { path: 'trade_summary', component: trade_summary },
  
        { path: 'exchange_rate', component: exchange_rate },
  
        { path: 'internation', component: internation },
                  
        { path: 'trade_do', component: trade_do },
    
        { path: 'trade_analyze', component: trade_analyze },
      ],
    }
  ]
})

export default router
