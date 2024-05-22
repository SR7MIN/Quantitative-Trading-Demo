<template>
    <div>
        可查询国内A股的全部股票信息
        <el-button type="primary" @click="Search_stock">
            <el-icon>
                <Search />
            </el-icon>
            股票查询</el-button>
    </div>
    <div ref="chartRef" style="width: 600px;height:400px;"></div>
    
</template>

<script setup>
import { ref, reactive } from 'vue';
import axios from 'axios';
import * as echarts from 'echarts';
import { ElLoading, ElMessage, ElMessageBox } from 'element-plus';
let chart = null;
const chartRef = ref(null);
const imageUrl = ref('');
const stock = reactive({
    code: '',
    name: '',
    data: ''
})
async function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
const Search_stock = () => { //加载动画一直不成功，不懂。
    const loading = ElLoading.service({ lock: true,fullscreen: true, text: "正在查询中..." });
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
               
                loading.close();
                if (res.data.status === "succeed") {
                    ElMessage({
                        type: 'success',
                        message: `股票查询成功！`,
                    });
                    stock.code = value;
                    stock.name = res.data.stock_name;
                    imageUrl.value = 'data:image/png;base64,' + res.data.image;
                    stock.data = res.data.data;
                    // 这里你可以处理response.data.data，它包含了股票数据

                    // 使用ECharts绘制图表
                    chart = echarts.init(chartRef.value);
                    chart.setOption({
                        title: {
                            text: `历史股价 - ${stock.name}`
                        },

                        tooltip: {
                            trigger: 'axis',
                            axisPointer: {
                                type: 'cross'
                            }
                        },
                        dataZoom: [{
                            type: 'slider',
                            start: 0,
                            end: 100
                        }, {
                            type: 'inside'
                        }],
                        xAxis: {
                            data: stock.data.map(item => item.日期),
                            type: 'category',
                            name: '日期'
                        },
                        yAxis: {
                            type: 'value',
                            min: Math.min(...stock.data.map(item => item.收盘)),
                            max: Math.max(...stock.data.map(item => item.收盘)),
                            name: '收盘价'
                        },
                        series: [{
                            name: '收盘价',
                            type: 'line',
                            data: stock.data.map(item => item.收盘)
                        }]
                    });
                }
                else {
                    ElMessage({
                        type: 'error',
                        message: '股票查询失败',
                    });
                }
            } catch (error) {
                loading.close();
                ElMessage({
                    type: 'error',
                    message: '查找失败',
                });
                console.log(error);
            }
        })
        .catch(() => {
            loading.close();
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
