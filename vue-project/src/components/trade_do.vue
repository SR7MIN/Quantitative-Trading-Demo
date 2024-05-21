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
                            <el-option label="A股" value="shanghai" />
                            <el-option label="港股" value="beijing" />
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
        <el-table :data="tableData" stripe style="width: 100%">
            <el-table-column prop="type" label="股票代码" width="180" />
            <el-table-column prop="money" label="股票名称" width="180" />
            <el-table-column prop="percent" label="交易数目" />
            <el-table-column prop="money" label="交易金额" />
            <el-table-column prop="money" label="手续费" />
            <el-table-column prop="money" label="结算金额" />
            <el-table-column label="操作">
                <template #default="scope">
                    <el-button size="small" @click="handleEdit(scope.$index, scope.row)">
                        卖出
                    </el-button>
                </template>
            </el-table-column>
        </el-table>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
const dialog = ref(false)
const loading = ref(false)
let timer
const form = reactive({  //记录想进行交易的股票信息
  code: '',
  place: '',
  num: undefined
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
const onClick = () => {
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

<style lang="scss" scoped></style>