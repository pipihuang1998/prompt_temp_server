<template>
  <div>
    <h1>{{ isEdit ? 'Edit' : 'Create' }} Template</h1>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
      <!-- Left: Template Content -->
      <div>
        <label>Template Name</label>
        <input v-model="form.name" style="width: 100%;" />

        <label>Description</label>
        <input v-model="form.temp_description" style="width: 100%;" />

        <label>Content (Use {{ variable }} syntax)</label>
        <textarea v-model="form.content" style="width: 100%; height: 200px; font-family: monospace;"></textarea>

        <button @click="analyzeVariables" style="margin-top: 10px;">Analyze Parameters</button>
      </div>

      <!-- Right: Parameter Configuration -->
      <div style="background: #f9f9f9; padding: 15px; border-radius: 5px;">
        <h3>Parameter Configuration</h3>
        <div v-if="!form.parameters_config || form.parameters_config.length === 0">
          Click "Analyze Parameters" to detect variables.
        </div>

        <div v-for="(param, idx) in form.parameters_config" :key="param.key" style="margin-bottom: 20px; border-bottom: 1px dashed #ccc; padding-bottom: 10px;">
          <div style="font-weight: bold; color: blue;">Variable: {{ param.key }}</div>

          <label>Display Label</label>
          <input v-model="param.label" style="width: 100%;" />

          <label>Type</label>
          <select v-model="param.type" @change="onTypeChange(param)" style="width: 100%;">
            <option v-for="(info, typeKey) in variableTypes" :key="typeKey" :value="typeKey">
              {{ info.label }}
            </option>
          </select>

          <div v-if="param.type && variableTypes[param.type]" style="margin-top: 10px; padding-left: 10px; border-left: 3px solid #ddd;">
            <strong>Type Settings:</strong>
            <div v-for="field in variableTypes[param.type].extension_schema" :key="field.key" style="margin-top: 5px;">
              <label style="font-size: 0.9em;">{{ field.label }}</label>

              <!-- String/Number Input -->
              <input
                v-if="field.type === 'string' || field.type === 'number'"
                :type="field.type === 'number' ? 'number' : 'text'"
                v-model="param.extension[field.key]"
                style="width: 90%;"
              />

              <!-- Boolean Switch -->
              <div v-else-if="field.type === 'boolean'">
                 <input type="checkbox" v-model="param.extension[field.key]" /> {{ field.label }}
              </div>

              <!-- List String (Simple comma separated for now) -->
              <div v-else-if="field.type === 'list_string'">
                <input
                  :value="param.extension[field.key] ? param.extension[field.key].join(',') : ''"
                  @input="e => param.extension[field.key] = e.target.value.split(',')"
                  placeholder="Comma separated values"
                  style="width: 90%;"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div style="margin-top: 20px; text-align: right;">
      <button @click="save" style="font-size: 1.2em; padding: 10px 20px; background: green; color: white;">Save Template</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const router = useRouter()
const isEdit = !!route.params.id

const variableTypes = ref({})
const form = ref({
  name: '',
  temp_description: '',
  content: '',
  parameters_config: []
})

// Fetch types on mount
onMounted(async () => {
  const res = await axios.get('/api/v1/template/types')
  variableTypes.value = res.data

  if (isEdit) {
    const tplRes = await axios.get(`/api/v1/template/${route.params.id}`)
    form.value = tplRes.data
  }
})

const analyzeVariables = async () => {
  if (!form.value.content) return
  try {
    const res = await axios.post('/api/v1/template/analyze', { content: form.value.content })
    const detectedVars = res.data

    // Merge detected vars with existing config
    // We want to keep existing config if variable still exists
    const currentConfigMap = {}
    form.value.parameters_config.forEach(p => {
      currentConfigMap[p.key] = p
    })

    const newConfig = detectedVars.map(v => {
      if (currentConfigMap[v]) {
        return currentConfigMap[v]
      } else {
        // Default new param
        return {
          key: v,
          label: v,
          type: 'text',
          default: '',
          required: true,
          extension: getDefaultExtension('text')
        }
      }
    })

    form.value.parameters_config = newConfig
  } catch (err) {
    alert('Analysis failed: ' + err.message)
  }
}

const getDefaultExtension = (type) => {
  const typeDef = variableTypes.value[type]
  if (!typeDef) return {}
  const ext = {}
  typeDef.extension_schema.forEach(field => {
    ext[field.key] = field.default
  })
  return ext
}

const onTypeChange = (param) => {
  // Reset extension when type changes
  param.extension = getDefaultExtension(param.type)
}

const save = async () => {
  try {
    if (isEdit) {
      await axios.put(`/api/v1/template/${route.params.id}`, form.value)
    } else {
      await axios.post('/api/v1/template', form.value)
    }
    router.push('/')
  } catch (err) {
    alert('Save failed: ' + err.message)
  }
}
</script>
