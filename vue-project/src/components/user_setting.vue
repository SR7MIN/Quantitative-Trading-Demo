<template>
    <div>
        <el-tabs v-model="activeName" type="card" class="demo-tabs" @tab-click="handleClick">
            <el-tab-pane label="账户信息" name="first">
                <div>
                    <el-card style="max-width: 480px; margin-bottom: 20px;">
                        <template #header>
                            <div class="card-header">
                                <span>基本信息</span>
                            </div>
                        </template>
                        <el-form ref="formRef" label-width="auto">
                            <el-form-item label="昵称" prop="name">{{ user.name }}</el-form-item>
                            <el-form-item label="账号" prop="zone">{{ user.account }}</el-form-item>
                            <el-form-item label="密码" prop="zone">{{ user.password }}</el-form-item>
                            <el-form-item label="邮箱" prop="time">您还没有绑定邮箱，
                                <el-button type="text" @click="bind_email">去绑定</el-button>
                            </el-form-item>
                            <el-button type="primary" @click="change_name">想换个名字？</el-button>
                        </el-form>

                    </el-card>
                    <el-card style="max-width: 480px">
                        <template #header>
                            <div class="card-header">
                                <span>账号安全</span>
                            </div>
                        </template>
                        <el-row>
                            您的账号安全等级：</br>
                        </el-row>
                        <div class="demo-progress">
                            <!-- <el-progress :percentage="50" /> 想弄一个进度条，但是显示有些问题 -->

                        </div>
                        <el-button primary @click="dialogFormVisible = true">
                            修改密码
                        </el-button>
                        <el-dialog v-model="dialogFormVisible" title="修改密码" width="500">
                            <el-form :model="newPassword" :rules="rules">
                                <el-form-item label="原密码" :label-width="formLabelWidth" prop="old">
                                    <el-input v-model="newPassword.old" autocomplete="off" />
                                </el-form-item>
                                <el-form-item label="新密码" :label-width="formLabelWidth" prop="password2">
                                    <el-input v-model="newPassword.new" autocomplete="off" />
                                </el-form-item>
                                <el-form-item label="确认密码" :label-width="formLabelWidth" prop="confirm">
                                    <el-input v-model="newPassword.confirm" autocomplete="off" />
                                </el-form-item>
                            </el-form>
                            <template #footer>
                                <div class="dialog-footer">
                                    <el-button @click="dialogFormVisible = false">Cancel</el-button>
                                    <el-button type="primary" @click="submitPasswordChange">
                                        Confirm
                                    </el-button>
                                </div>
                            </template>
                        </el-dialog>

                    </el-card>
                </div>
            </el-tab-pane>
            <el-tab-pane label="我的收藏" name="second">我的收藏</el-tab-pane>
            <el-tab-pane label="余额管理" name="third">余额管理</el-tab-pane>
        </el-tabs>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useStorage } from '@vueuse/core';
import axios from 'axios'; // 导入 axios 库，用于发送 HTTP 请求
const format = (percentage) => (percentage === 100 ? 'Full' : `${percentage}%`)
const newPassword = reactive({
    old: '',
    new: '',
    confirm: '',
})
const user = useStorage('user', ({
    name: '',
    remember: false,
    password: '',
    account: '',
}));

const dialogFormVisible = ref(false)
const formLabelWidth = '140px'
const can_change_or_not = ref(false) // 用于判断是否可以修改密码
const rules = reactive({
    password2: [
        { validator: validatePassword, trigger: 'blur' }
    ],
    old: [
        { validator: validate_old, trigger: 'blur' }
    ],
    confirm: [
        { validator: validate_confirm, trigger: 'blur' }
    ],
    // 其他字段的验证规则
});
function validatePassword(rule, value, callback) { //不知道为啥只有这个验证规则还不能正常运行
    const pattern = /^[a-zA-Z0-9.,!@#$%^&*()]{3,10}$/;
    if (!pattern.test(value)) {
        callback(new Error('密码应为3-10位的数字、字母和标点的组合'));
        can_change_or_not.value = false
    } else {
        callback();
        can_change_or_not.value = true
    }
}
function validate_old(rule, value, callback) {
    if (value !== user.value.password) {
        callback(new Error('原密码错误'));
        can_change_or_not.value = false
    } else {
        callback();
        can_change_or_not.value = true
    }
}
function validate_confirm(rule, value, callback) {
    if (value !== newPassword.new) {
        callback(new Error('两次密码输入不一致'));
        can_change_or_not.value = false
    } else {
        callback();
        can_change_or_not.value = true
    }
}
const change_name = () => {
    ElMessageBox.prompt('请输入您的新昵称', 'Tip', {
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel',
        inputPattern: /\S+/,
        inputErrorMessage: '昵称不能为空',
    })
        .then(async ({ value }) => {
            try {
                // 向后端发送一个 POST 请求，通知后端昵称已经改变
                const res = await axios.post('http://localhost:5000/home/change-nickname', {
                    account: user.value.account,
                    password: user.value.password,
                    newNickname: value,
                });
                if (res.data.status === "success") {
                    ElMessage({
                        type: 'success',
                        message: `昵称修改成功！`,
                    });
                    user.value.name = value;
                }
            } catch (error) {
                ElMessage({
                    type: 'error',
                    message: '昵称修改失败222',
                });
            }
        })
        .catch(() => {
            ElMessage({
                type: 'info',
                message: 'Input canceled',
            });
        });
}
const bind_email = () => { // 没和数据库交互，所以只能空填写，没作用，后续或可加入邮箱密码找回功能
    ElMessageBox.prompt('请输入您要绑定的邮箱', 'Tip', {
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel',
        inputPattern:
            /[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?/,
        inputErrorMessage: '无效邮箱',
    })
        .then(({ value }) => {
            ElMessage({
                type: 'success',
                message: `Your email is:${value}`,
            })
        })
        .catch(() => {
            ElMessage({
                type: 'info',
                message: 'Input canceled',
            })
        })
}
const submitPasswordChange = async () => {
    if (!can_change_or_not.value) {
        ElMessage({
            type: 'error',
            message: '密码修改失败',
        });
        return
    }
    try {
        // 向后端发送一个 POST 请求，通知后端密码已经改变
        // 请将 '/api/change-password' 替换为你的后端接口
        const res = await axios.post('http://localhost:5000/home/change-password', {
            account: user.value.account,
            password: user.value.password,
            newPassword: newPassword.new,
        });
        if (res.data.status === "success") {
            ElMessage({
                type: 'success',
                message: '密码修改成功',
            });
            user.value.password = newPassword.new;
        }
        else {
            ElMessage({
                type: 'error',
                message: '密码修改失败',
            });
        }

    } catch (error) {
        ElMessage({
            type: 'error',
            message: '密码修改失败',
        });
    }
    dialogFormVisible.value = false;
};
</script>

<style lang="scss" scoped>
.demo-progress .el-progress--line {
    margin-bottom: 15px;
    max-width: 600px;
}
</style>