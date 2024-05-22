<template>
    <div>
        <el-button type="primary" @click="dialog = true">
            <el-icon>
                <Plus />
            </el-icon>
            &nbsp;&nbsp;交易</el-button>
        <el-drawer v-model="dialog" 
        title="请输入您想进行的交易" :before-close="handleClose" direction="rtl"
            class="demo-drawer">
            <div class="demo-drawer__content">
                <el-form :model="form">
                    <el-form-item label="股票代码" :label-width="formLabelWidth">
                        <el-input v-model="form.code" autocomplete="off" />
                    </el-form-item>
                    <el-form-item label="股票所属市场" :label-width="formLabelWidth">
                        <el-select v-model="form.place" placeholder="Please select stock area">
                            <el-option label="A股" value="cn" />
                            <el-option label="港股" value="hk" />
                        </el-select>
                    </el-form-item>
                    <el-form-item label="选购股数" :label-width="formLabelWidth">
                        <el-input v-model="form.num" autocomplete="off" />
                    </el-form-item>
                </el-form>
                <div class="demo-drawer__footer">
                    <el-button @click="cancelForm">取消交易</el-button>
                    <el-button type="primary" :loading="loading" @click="onClick">
                        {{ loading ? 'Submitting ...' : '提交交易' }}
                    </el-button>
                </div>
            </div>
        </el-drawer>
    </div>
    <div>
        <h1 style="margin-top: 10px;">交易记录:</h1>
        <el-table :data="stock_history.value" stripe style="width: 100%">
            <el-table-column prop="stock_code" label="股票代码" width="180" />
            <el-table-column prop="stock_name" label="股票名称" width="180" />
            <el-table-column prop="num" label="交易数目" />
            <el-table-column prop="price" label="每股金额" />
            <el-table-column label="总金额" :formatter="totalAmountFormatter" sortable :sort-method="sortTotalAmount"/>
            <el-table-column prop="type" label="交易类型" :formatter="typeFormatter"/>
            <el-table-column prop="time" label="交易时间" sortable/>
            <el-table-column label="操作">
                <template #default="scope">
                    <el-button size="small" @click="handle_sell">
                        卖出
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script setup>
import { ref, reactive,onMounted} from 'vue';
import { useStorage } from '@vueuse/core';
import axios from 'axios';
const dialog = ref(false)
const loading = ref(false)
let timer
const form = reactive({  //记录想进行交易的股票信息
  code: '',
  place: '',
  num: 0,
  account: undefined
})
const user = useStorage('user', ({
    name: '',
    remember: false,
    password: '',
    account: '',
    balance: 1000000,
    stocks_held: [{'code': '000001', 'place': 'cn', 'amount': 1000}, 
    {'code': '603000', 'place': 'cn', 'amount': 2000}
    ],
}));
const stock_history = reactive({
    value: [],
}
)
function handle_sell() {
    
}
async function buy_stock() { // 购买
    const path = 'http://localhost:5000/home/buy';
    form.account = user.value.account;
    try {
        const res = await axios.post(path, form);
        if (res.data.status === "success") {
            ElMessage.success('交易成功');
            get_stock_history();   
        } else {
            // handle login failure
            console.error('Login failed');
            ElMessage.error('交易失败，余额不足');
        }
    } catch (error) {
        console.error(error);
        ElMessage.error('网络问题，交易失败，请重试222');
    }
}

async function get_stock_history() { // 获取历史交易记录
    const path = 'http://localhost:5000/home/history';
    try {
        const res = await axios.post(path, user.value);
        if (res.data.status === "success") {
            stock_history.value = res.data.history;
            console.log(stock_history.value);
            console.log('获取历史交易记录成功');
        } else {
            
            console.error('获取历史交易记录失败');
        }
    } catch (error) {
        console.error(error);
        console.error('网络问题，获取历史交易失败，请重试222');
    }
}

onMounted(() => {
    get_stock_history()
})
const typeFormatter = (row) => {
    return row.type === 'buy' ? '买入' : '卖出';
}
const totalAmountFormatter = (row) => {
    return (row.price * row.num).toFixed(2);
}
const sortTotalAmount = (a, b) => {
    return (a.price * a.num) - (b.price * b.num);
}
const onClick = () => {
    buy_stock()
    loading.value = true
    setTimeout(() => {
        loading.value = false
        dialog.value = false
    }, 400)
}

const handleClose = (done) => {
    if (loading.value) {
        return
    }
    ElMessageBox.confirm('强制退出会放弃此次交易，是否继续？',{
        confirmButtonText: '是',
    cancelButtonText: '否',
    })
        .then(() => {
            loading.value = false
            dialog.value = false
            clearTimeout(timer)
            form.code = '';
    form.place = '';
    form.num = undefined;
            done();
        })
        .catch(() => {
            // catch error
        })
}

const cancelForm = () => {
    loading.value = false
    dialog.value = false
    clearTimeout(timer)
    form.code = '';
    form.place = '';
    form.num = undefined;
}
</script>

<style lang="scss" scoped>

</style>