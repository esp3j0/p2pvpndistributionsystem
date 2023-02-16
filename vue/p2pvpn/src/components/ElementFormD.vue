<template>
    <el-form
      ref="ruleFormRef"
      :model="ruleForm"
      :rules="rules"
      label-width="120px"
      class="demo-ruleForm"
      :size="formSize"
      status-icon
    >
      <el-form-item label="私网uuid" prop="Internet">
        <el-input v-model="ruleForm.Internet" placeholder="生成页面中创建的网络uuid"/>
      </el-form-item>
      <el-form-item label="选择操作系统" prop="region">
        <el-select v-model="ruleForm.region" placeholder="选择您的操作系统">
          <el-option label="Windows" value="w" />
          <el-option label="Linux" value="l" />
          <el-option label="Mac" value="m" />
        </el-select>
      </el-form-item>
      <el-form-item label="节点编号" prop="count" >
        <el-input
          v-model="ruleForm.count"
          placeholder="选择您生成的私人网络未被使用的一个节点编号, 该值需要小于生成的节点数量"
        />
      </el-form-item>
     
      <el-form-item>
        <el-button type="primary" @click="submitForm(ruleFormRef)">
          下载
        </el-button>
        <el-button @click="resetForm(ruleFormRef)">重置</el-button>
      </el-form-item>
    </el-form>

    <el-dialog v-model="centerDialogVisible" title="Info" width="30%" center>
      <span>
        {{ mes }}
      </span>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="centerDialogVisible = false">Cancel</el-button>
          <el-button type="primary" @click="centerDialogVisible = false">
            Confirm
          </el-button>
        </span>
      </template>
    </el-dialog>
  </template>
  
  <script lang="ts" setup>
  import { reactive, ref } from 'vue'
  import type { FormInstance, FormRules } from 'element-plus'
  import axios from 'axios'
  const centerDialogVisible = ref(false)
  const formSize = ref('default')
  const mes = ref('')
  const ruleFormRef = ref<FormInstance>()
  const ruleForm = reactive({
    Internet: '',
    region: '',
    count: '',
  })
  
  const rules = reactive<FormRules>({
    Internet: [
      { required: true, message: '生成页面中创建的网络uuid', trigger: 'blur' },
      { min: 6, max: 6, message: '长度为6', trigger: 'blur' },
    ],
    region: [
      {
        required: true,
        message: '请选择操作系统',
        trigger: 'change',
      },
    ],
    count: [
      {
        required: true,
        message: '请选择将要使用的节点编号',
        trigger: 'blur',
      },
    ],
  })
  
  const submitForm = async (formEl: FormInstance | undefined) => {
    if (!formEl) return
    await formEl.validate((valid, fields) => {
      if (valid) {
        if (ruleForm.region == 'w'){
          location.href = "http://vpn.f0n.fun:5000/downloadw/"+ruleForm.Internet+"/"+ruleForm.count
        }
        if (ruleForm.region == 'l'){
          location.href = "http://vpn.f0n.fun:5000/downloadl/"+ruleForm.Internet+"/"+ruleForm.count
        }
        if (ruleForm.region == 'm'){
          location.href = "http://vpn.f0n.fun:5000/downloadm/"+ruleForm.Internet+"/"+ruleForm.count
        }
      } else {
        console.log('error submit!', fields)
        console.log(parseInt(ruleForm.region))
      }
    })
  }
  
  const resetForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.resetFields()
  }
  

  
  </script>
  