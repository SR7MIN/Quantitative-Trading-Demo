<template>
    <div>
        展示国内A股的全部股票信息
        <el-button type="primary" @click="Search_stock">
            <el-icon>
                <Search />
            </el-icon>
            股票查询</el-button>
    </div>
    <div>
        <img v-if="imageUrl" :src="imageUrl" alt="Stock Chart">
    </div>
</template>

<script setup>
import {ref, reactive} from 'vue';
import axios from 'axios';
const imageUrl = ref('');
const stock = reactive({
    code: '',
    name: '',
    price: '',
    // change: '',
    // percent: '',
    // high: '',
    // low: '',
    // volume: '',
    // amount: '',
    // turnover: '',
    // pe: '',
    // pb: '',
    // time: '',
})

const Search_stock = () => {
    ElMessageBox.prompt('请输入您要查询的股票代码', 'Tip', {
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel',
        inputPattern: /^\d{6}$/,
        inputErrorMessage: '无效代码',
    })
        .then(async ({ value }) => {
            try {
                const res = await axios.post('http://localhost:5000/home/stock', {
                    code: value
                });
                if (res.data.status === "succeed") {
                    ElMessage({
                        type: 'success',
                        message: `股票查询成功！`,
                    });
                    stock.code = value;
                    imageUrl.value='data:image/png;base64,' + res.data.image;
                }
                else {
                    ElMessage({
                        type: 'error',
                        message: '股票查询失败',
                    });
                }
            } catch (error) {
                ElMessage({
                    type: 'error',
                    message: '查找失败',
                });
                console.log(error);
            }
        })
        .catch(() => {
            ElMessage({
                type: 'info',
                message: '操作取消',
            });
        });
}
// const send_stock_code = async (value) => {
//     try {
//         // 向后端发送一个 POST 请求，通知后端要查询的股票代码
//         const res = await axios.post('http://localhost:5000/home/stock', {
//             code: value
//         });
//         return res
//     } catch (error) {
//         return 'error';
//     }
// }
// const Search_stock = () => { 
//     ElMessageBox.prompt('请输入您要查找的股票代码', 'Tip', {
//         confirmButtonText: 'OK',
//         cancelButtonText: 'Cancel',
//         inputPattern: /^\d{6}$/,
//         inputErrorMessage: '无效代码',
//     })
//         .then(async ({ value }) => {
//             const res = await send_stock_code(value);
//             if (res.data.status === "success") {
//                 ElMessage({
//                     type: 'success',
//                     message: `查找成功！`,
//                 });
//                 stock.code = value;
//             } else {
//                 ElMessage({
//                     type: 'error',
//                     message: '查找失败',
//                 });
//             }
//         })
//         .catch(() => {
//             ElMessage({
//                 type: 'info',
//                 message: '操作取消',
//             })
//         })
// }
</script>

<style lang="scss" scoped></style>
