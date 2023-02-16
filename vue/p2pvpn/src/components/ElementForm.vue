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
      <el-form-item label="生成私网网络" prop="Internet">
        <el-input v-model="ruleForm.Internet" placeholder="10.0.0.0~10.255.255.255或172.16.0.0~172.131.255.255或192.168.0.0!192.168.255.255，推荐:10.7.0.0"/>
      </el-form-item>
      <el-form-item label="选择掩码" prop="region">
        <el-select v-model="ruleForm.region" placeholder="个人用户:255.255.255.0">
          <el-option label="255.0.0.0" value="3" />
          <el-option label="255.255.0.0" value="2" />
          <el-option label="255.255.255.0" value="1" />
        </el-select>
      </el-form-item>
      <el-form-item label="节点数量" prop="count" >
        <el-input
          v-model="ruleForm.count"
          placeholder="想要组成私网的设备数量，255.255.255.0<255，255.255.0.0<255^2，255.0.0.0<255^3"
        />
      </el-form-item>
     
      <el-form-item>
        <el-button type="primary" @click="submitForm(ruleFormRef)">
          创建
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
      { required: true, message: '10.0.0.0~10.255.255.255或172.16.0.0~172.131.255.255或192.168.0.0!192.168.255.255', trigger: 'blur' },
      { min: 8, max: 12, message: 'Length should be 3 to 5', trigger: 'blur' },
    ],
    region: [
      {
        required: true,
        message: '请选择网络掩码',
        trigger: 'change',
      },
    ],
    count: [
      {
        required: true,
        message: '请选择将要生成的节点数量',
        trigger: 'blur',
      },
    ],
  })
  
  const submitForm = async (formEl: FormInstance | undefined) => {
    if (!formEl) return
    await formEl.validate((valid, fields) => {
      if (valid) {
        axios.post(
          'http://vpn.f0n.fun:5000/generate',
          {
            'Internet':ruleForm.Internet,
            "region" : ruleForm.region,
            "count" : ruleForm.count
          },
          {
            headers:{
              "Access-Control-Allow-Origin" : "*"
            },
          }
        ).then(res => {
          mes.value = res.data
          console.log(res.data)
        })
        centerDialogVisible.value = true
        console.log('submit!')
        console.log(ruleForm.Internet)
        console.log(ruleForm.count)
        console.log(ruleForm.region)
        
        
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
  