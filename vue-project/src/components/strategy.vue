<template>
  <div class="strategy-edit">
    <!-- <h1>策略编辑</h1> -->
    
    <!-- 策略名称下拉框 -->
    <div class="select-strategy">
      <el-button type="primary" @click="createNewStrategy">新建策略</el-button>
      <el-button type="primary" @click="saveChanges" class="save-button">保存更改</el-button>
    </div>
    
    <div class="editor-layout">
      
      <!-- 左侧：策略代码 -->
      <div class="code-editor">
        <!-- <label for="strategyCode">策略代码:</label> -->
        <textarea id="strategyCode" v-model="editedStrategy.Strategy_Code" style="font-family: 'Courier New', monospace;"></textarea>

      </div>
      
      <!-- 右侧：策略描述（Markdown支持） -->
      <div class="description-editor">
        <label for="strategyDescription">策略描述:</label>
        <!-- Textarea 用于输入Markdown -->
        <textarea id="strategyDescription" v-model="markdownText"></textarea>
        <!-- 渲染Markdown到div中 -->
        <div v-html="renderedMarkdown" class="markdown-preview"></div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import axios from 'axios';
import ace from 'ace-builds/src-noconflict/ace';
import 'ace-builds/src-noconflict/mode-python';
import 'ace-builds/src-noconflict/theme-monokai';
import MarkdownIt from 'markdown-it';
import { ElMessage } from 'element-plus';

// 假设这是从API获取的初始策略数据
const initialStrategy = {
  Strategy_ID: 1,
  User_ID: 1,
  Strategy_Name: '示例策略',
  Strategy_Description: '这是一个示例策略的描述',
  Strategy_Code: "// 示例策略代码...\n//startegy('code=str',stop_loss_level='float',take_profit_level='float')",
  Creation_Date: '2023-04-01',
  result:ref({})
};

// 使用ref来创建可变的响应式数据对象
const editedStrategy = ref({ ...initialStrategy });
const strategies = ref([]); // 用户的策略列表
const selectedStrategy = ref(null); // 当前选中的策略ID

const markdownText = ref('# hello  \nthis is my strategy  \nwe can edit with markdown');
const renderedMarkdown = ref('');
// 创建 markdown-it 实例
const md = MarkdownIt({
  html: true,
  linkify: true,
});

function updateDescriptionPreview() {
  renderedMarkdown.value = md.render(markdownText.value);

}

// 初始化渲染
updateDescriptionPreview();
// 监听Markdown文本的变化，并更新渲染的HTML
watch(markdownText, updateDescriptionPreview);

// onMounted(() => {
//   // 假设这是登录后获取的用户ID
//   const userId = '1';
//   fetchStrategies(userId);
// });
const fetchStrategies = async (userId) => {
  try {
    const response = await axios.post(`http://localhost:5000/strategies`,userId);
    const fetchedStrategies = response.data;
    if (fetchedStrategies.length === 0) {
      // 如果没有策略，调用 createNewStrategy 函数新建一个策略
      createNewStrategy();
    } else {
      // 如果有策略，选择第一个策略
      selectedStrategy.value = fetchedStrategies[0].id;
      loadStrategyDetails(fetchedStrategies[0]);
    }
    if (strategies.value.length > 0 && !selectedStrategy.value) {
      selectedStrategy.value = strategies.value[0].id;
    }
  } catch (error) {
    console.error('策略列表获取失败:', error);
  }
};

const loadStrategyDetails = (strategy) => {
  editedStrategy.value = { ...strategy };
  updateDescriptionPreview(); // 更新Markdown预览
};

const createNewStrategy = () => {
  editedStrategy.value = {
    Strategy_ID: 1,
    User_ID: 1,
    Strategy_Name: '新策略',
    Strategy_Description: '# 这是一个新策略的描述  ',
    Strategy_Code: "strategy(688031,-0.05,0.10)",
    Creation_Date: new Date().toISOString().split('T')[0]
  };
  selectedStrategy.value = editedStrategy.value;
  markdownText.value = editedStrategy.value.Strategy_Description;

};
const trade = ref({});
import { getCurrentInstance } from "vue";
const systemId = getCurrentInstance()?.appContext.config.globalProperties.$systemId

const saveChanges = async () => {
  // 使用 prompt 函数弹出窗口让用户输入策略名称
  const strategyName = prompt('请输入策略名称：', '新策略名称');
  // 检查用户是否点击了“取消”或未输入任何内容
  if (strategyName) {
    // 更新当前策略的名称
    editedStrategy.value.Strategy_Name = strategyName;
    console.log(editedStrategy.value);
    // 继续保存策略的逻辑...
    try {
      const path = `http://localhost:5000/home/strategies`;
      const response = await axios.post(path, editedStrategy.value);
      // console.log(response.data);
      // trade=response.data;
      systemId.value=response.data;
      console.log(systemId.value);
      ElMessage.success('策略更新成功');
    } catch (error) {
      console.error('策略更新失败:', error);
      ElMessage.error('策略更新失败');
    }
  } else {
    // 用户点击了“取消”或未输入任何内容
    ElMessage.warning('保存已取消');
  }
};


// 阻止tab键切换焦点的代码保持不变
onMounted(() => {
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Tab') {
      event.preventDefault();
      const focusedElement = document.activeElement;
      if (['textarea', 'input'].includes(focusedElement.tagName.toLowerCase()) && focusedElement.getAttribute('type') !== 'button') {
        const startPosition = focusedElement.selectionStart;
        const text = focusedElement.value;
        focusedElement.value = text.slice(0, startPosition) + '\t' + text.slice(focusedElement.selectionEnd);
        focusedElement.selectionStart = focusedElement.selectionEnd = startPosition + 1;
      }
    }
  });
});
import {
  Check,
  Delete,
  Edit,
  Message,
  Search,
  Star,
} from '@element-plus/icons-vue'

</script>

<style scoped>
.strategy-edit {
  display: flex;
  flex-direction: column;
}
/* .select-strategy {
  margin-bottom: 20px;
} */
.editor-layout {
  display: flex;
  justify-content: space-between;
}
.code-editor, .description-editor {
  flex: 1;
  margin-right: 20px;
}
.code-editor textarea, .description-editor textarea {
  width: 100%;
  height: 625px;
  overflow-y: auto; 
  resize: none;
}
.description-editor textarea {
  height:300px;
  overflow-y: auto; 
  resize: none;
}
.markdown-preview {
  border: 1px solid #ddd;
  padding: 10px;
  height:300px;
  overflow-y: auto; 
  resize: none;
}
/* .save-button {
  margin-top: 20px;
} */

.code-editor textarea{
  font-family: 'Courier New', Courier, monospace; /* 使用等宽字体 */
  font-size:medium; /* 设置字体大小 */
  background-color: #f5f5f5; /* 柔和的背景色 */
  border: 1px solid #ccc; /* 添加边框 */
  border-radius: 4px; /* 轻微的圆角 */
  padding: 10px; /* 内边距 */
  margin: 10px 0; /* 外边距 */
  line-height: 1.5; /* 行高 */
  width: 95%; /* 宽度 */
  overflow: auto; /* 滚动条 */
}

/* 当textarea获得焦点时的样式 */
.code-editor:focus {
  outline: none; /* 移除默认轮廓 */
  border-color: #66afe9; /* 聚焦时改变边框颜色 */
  box-shadow: 0 0 8px rgba(102, 175, 233, 0.6); /* 添加阴影 */
}



</style>