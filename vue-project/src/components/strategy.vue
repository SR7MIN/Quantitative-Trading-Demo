<template>
  <div class="strategy-edit">
    <h1>策略编辑</h1>
    
    <!-- 策略名称下拉框 -->
    <div class="select-strategy">
      <label for="strategySelection">选择策略:</label>
      <select id="strategySelection" v-model="selectedStrategy" @change="loadStrategyDetails">
        <option value="">新建策略</option>
        <option v-for="strategy in strategies" :key="strategy.id" :value="strategy.id">{{ strategy.name }}</option>
      </select>
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
    
    <!-- 保存按钮 -->
    <button type="button" @click="saveChanges" class="save-button">保存更改</button>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import ace from 'ace-builds/src-noconflict/ace';
import 'ace-builds/src-noconflict/mode-python';
import { VAceEditor } from 'vue3-ace-editor';
import 'ace-builds/src-noconflict/theme-monokai';

// 假设这是从API获取的初始策略数据
const initialStrategy = {
  Strategy_ID: 1,
  User_ID: 1,
  Strategy_Name: '示例策略',
  Strategy_Description: '这是一个示例策略的描述',
  Strategy_Code: "// 示例策略代码...\n//buy('code','volume',over='',below='');\n//sell('code''volume',over='',below='');",
  Creation_Date: '2023-04-01'
};

// 使用ref来创建可变的响应式数据对象
const editedStrategy = ref({ ...initialStrategy });

// 将策略代码作为 strategyComponent 的属性
const strategyComponent = ref(initialStrategy.Strategy_Code);

const saveChanges = async() => {
  const path = `http://localhost:5000/api/strategies/${editedStrategy.value.Strategy_ID}`;
  console.log('策略更新:', editedStrategy.value);
  try {
    const response = await axios.put(path, editedStrategy.value);
    console.log(response.data);
  }
  catch (error) {
    console.error('策略更新失败:', error);
  };
};
// import { ref } from 'vue';
import MarkdownIt from 'markdown-it';

// 创建 markdown-it 实例
const md = MarkdownIt({
  // 配置选项
  html: true,
  linkify: true,
});
// 响应式地存储Markdown文本
const markdownText = ref('# hello  \nthis is my strategy  \nwe can edit with markdown');
// 函数，用于更新渲染的Markdown HTML
function updateDescriptionPreview() {
  renderedMarkdown.value = md.render(markdownText.value);
}
// 响应式地存储渲染后的Markdown HTML
const renderedMarkdown = ref('');
// 初始化渲染
updateDescriptionPreview();
// 监听Markdown文本的变化，并更新渲染的HTML
watch(markdownText, updateDescriptionPreview);

import { onMounted } from 'vue';

onMounted(() => {
  document.addEventListener('keydown', (event) => {
    // 检查按下的键是否是Tab键
    if (event.key === 'Tab') {
      // 阻止默认行为，即不切换焦点
      event.preventDefault();
      // 获取当前焦点的元素
      const focusedElement = document.activeElement;
      // 如果焦点的元素是可输入的（如input或textarea）
      if (focusedElement.tagName.toLowerCase() === 'textarea' || (focusedElement.tagName.toLowerCase() === 'input' && focusedElement.getAttribute('type') !== 'button')) {
        // 将制表符字符插入到元素中
        const startPosition = focusedElement.selectionStart;
        const text = focusedElement.value;
        focusedElement.value = text.slice(0, startPosition) + '\t' + text.slice(focusedElement.selectionEnd);
        // 移动光标到制表符字符后面
        focusedElement.selectionStart = focusedElement.selectionEnd = startPosition + 1;
      }
    }
  });
});

</script>

<style scoped>
.strategy-edit {
  display: flex;
  flex-direction: column;
}
.select-strategy {
  margin-bottom: 20px;
}
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
.save-button {
  margin-top: 20px;
}

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
