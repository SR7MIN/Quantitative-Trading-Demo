<template>
    <div>
        <el-button type="primary" @click="dialog = true">
            <el-icon>
                <Plus />
            </el-icon>
            &nbsp;&nbsp;交易</el-button>
        <el-drawer v-model="dialog" title="请输入您想进行的交易" 
        :before-close="handleClose" direction="rtl" class="demo-drawer1">
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
        <el-table :data="stock_history.value" stripe style="width: 100%" height="500">
            <el-table-column prop="stock_code" label="股票代码" width="180" />
            <el-table-column prop="stock_name" label="股票名称" width="180" />
            <el-table-column prop="num" label="交易数目" />
            <el-table-column prop="price" label="每股金额" />
            <el-table-column label="总金额" :formatter="totalAmountFormatter" sortable :sort-method="sortTotalAmount" />
            <el-table-column prop="type" label="交易类型" :formatter="typeFormatter" />
            <el-table-column prop="time" label="交易时间" sortable />
            <el-table-column label="操作">
                <template #default="scope">
                    <div>
                    <el-button type="danger" @click="openSellDialog(scope.row)">
                        卖出
                    </el-button>
                    <el-drawer v-model="dialog2" title="请输入您想卖出的股数" 
                    :before-close="handleClose" 
                    direction="rtl" class="demo-drawer" >
                    <!-- :append-to-body="true" -->
            <div class="demo-drawer__content">
                <el-form :model="form">
                    <el-form-item label="卖出股数" :label-width="formLabelWidth">
                        <el-input v-model="form.num" autocomplete="off" />
                    </el-form-item>
                    <el-form-item label="总收益" :label-width="formLabelWidth">
                        {{ totalIncome }}
                    </el-form-item>
                </el-form>
                <div class="demo-drawer__footer">
                    <el-button @click="cancelForm">取消交易</el-button>
                    <el-button type="primary" :loading="loading" @click="onClick2">
                        {{ loading ? 'Submitting ...' : '提交交易' }}
                    </el-button>
                </div>
            </div>
        </el-drawer>
                    </div>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue';
import { get, useStorage } from '@vueuse/core';
import axios from 'axios';
import { nextTick } from 'vue';

const dialog = ref(false)
const dialog2 = ref(false)
const loading = ref(false) 
let timer
const form = reactive({  //记录想进行交易的股票信息
    code: '',
    place: '',
    num: 0,
    account: undefined,
    price: undefined
})

const user = useStorage('user', ({
    name: '',
    remember: false,
    password: '',
    account: '',
    balance: 1000000,
    all_property: 0,
    stocks_held: undefined,
}));
const stock_history = reactive({
    value: [],
}
)
const openSellDialog = (row) => {
    form.code = row.stock_code;
    dialog2.value = true;
    get_now_price();
}
async function get_now_price() { // 获取当前股票价格
    const path = 'http://localhost:5000/home/price';
    try {
        const res = await axios.post(path, form);
        if (res.data.status === "success") {
            form.price = res.data.price;
            console.log('获取当前股票价格成功');
            console.log(form.price);
        } else {
            console.error('获取当前股票价格失败');
        }
    } catch (error) {
        console.error(error);
        console.error('网络问题，获取当前股票价格失败，请重试');
    }
}
let totalIncome = computed(() => form.num * form.price);
async function sell_stock() {
    const path = 'http://localhost:5000/home/sell';
    form.account = user.value.account;
    try {
        const res = await axios.post(path, form);
        if (res.data.status === "success") {
            ElMessage.success('交易成功');
            user.value.balance = res.data.balance;
            get_stock_history();
        } else {
            
            ElMessage.error('交易失败，卖出的股票超过拥有量');
        }
    } catch (error) {
        console.error(error);
        ElMessage.error('网络问题，交易失败，请重试222');
    }
}
async function buy_stock() { // 购买
    const path = 'http://localhost:5000/home/buy';
    form.account = user.value.account;
    try {
        const res = await axios.post(path, form);
        if (res.data.status === "success") {
            ElMessage.success('交易成功');
            user.value.balance = res.data.balance;
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
            
            await nextTick();
            console.log(user.value.balance);  // Now it should print the updated balance
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
        dialog2.value = false
    }, 400)
}
const onClick2 = () => {
    sell_stock()
    loading.value = true
    setTimeout(() => {
        loading.value = false
        dialog.value = false
        dialog2.value = false
    }, 400)
}

const handleClose = (done) => {
    if (loading.value) {
        return
    }
    ElMessageBox.confirm('强制退出会放弃此次交易，是否继续？', {
        confirmButtonText: '是',
        cancelButtonText: '否',
    })
        .then(() => {
            loading.value = false
            dialog.value = false
            dialog2.value = false
            clearTimeout(timer)
            form.code = '';
            form.place = '';
            form.num = undefined;
            form.price = undefined;
            done();
        })
        .catch(() => {
            // catch error
        })
}

const cancelForm = () => {
    loading.value = false
    dialog.value = false
    dialog2.value = false
    clearTimeout(timer)
    form.code = '';
    form.place = '';
    form.num = undefined;
    form.price = undefined;
}
</script>

<style lang="scss" scoped>
// .el-drawer__open .el-dialog__wrapper {
//     background-color: transparent !important;
// }
// .v-modal {
//     background-color: transparent !important;
// }
// .el-drawer__open .el-overlay {
//     background-color: transparent !important;
// }
// .demo-drawer {
//     background-color: transparent !important;
// }
</style>