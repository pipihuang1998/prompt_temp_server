<template>
  <div>
    <h1>Use Template</h1>
    <div v-if="!template">Loading...</div>
    <div v-else>
      <h2>{{ template.name }}</h2>
      <p>{{ template.temp_description }}</p>

      <div style="background: #fff; padding: 20px; border: 1px solid #ddd; border-radius: 5px;">
        <div v-for="param in template.parameters_config" :key="param.key" style="margin-bottom: 15px;">
          <label>{{ param.label }} <span v-if="param.required" style="color: red;">*</span></label>

          <!-- Text -->
          <div v-if="param.type === 'text'">
             <textarea v-if="param.extension.is_textarea"
               v-model="formValues[param.key]"
               :placeholder="param.extension.placeholder"
               :maxlength="param.extension.max_length"
               style="width: 100%;"
             ></textarea>
             <input v-else
               v-model="formValues[param.key]"
               :placeholder="param.extension.placeholder"
               :maxlength="param.extension.max_length"
               style="width: 100%;"
             />
          </div>

          <!-- Select -->
          <div v-else-if="param.type === 'select'">
            <select v-model="formValues[param.key]" :multiple="param.extension.allow_multiple" style="width: 100%;">
              <option v-for="opt in param.extension.options" :key="opt" :value="opt">{{ opt }}</option>
            </select>
          </div>

          <!-- API Dynamic Select -->
          <div v-else-if="param.type === 'api_dynamic_select'">
             <div v-if="loadingOptions[param.key]">Loading options...</div>
             <select v-else v-model="formValues[param.key]" :multiple="param.extension.allow_multiple" style="width: 100%;">
               <option v-for="opt in (optionsMap[param.key] || [])" :key="opt.val" :value="opt.val">
                 {{ opt.label }}
               </option>
             </select>
          </div>

          <!-- KB Search (Simplified for demo) -->
          <div v-else-if="param.type === 'kb_search'">
             <input v-model="formValues[param.key]" placeholder="Search KB..." style="width: 100%;" />
             <small>KB ID: {{ param.extension.kb_id }} (Simulated search)</small>
          </div>

          <!-- Excel Input -->
          <div v-else-if="param.type === 'excel'">
             <textarea
               v-model="excelInputs[param.key]"
               @input="processExcelInput(param.key)"
               :placeholder="param.extension.placeholder"
               style="width: 100%; height: 100px; font-family: monospace;"
             ></textarea>
             <div style="font-size: 0.8em; color: gray;">Pasted data will be converted to Markdown table automatically.</div>
          </div>
        </div>

        <button @click="generate" style="background: blue; color: white; padding: 10px 20px; font-size: 1.1em;">Generate Prompt</button>
      </div>

      <div v-if="result" style="margin-top: 20px; background: #eef; padding: 15px; border: 1px solid blue;">
        <h3>Result:</h3>
        <pre>{{ result }}</pre>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

const route = useRoute()
const template = ref(null)
const formValues = ref({})
const result = ref('')

// For dynamic selects
const optionsMap = ref({})
const loadingOptions = ref({})
// For Excel
const excelInputs = ref({})

onMounted(async () => {
  try {
    const res = await axios.get(`/api/v1/template/${route.params.id}`)
    template.value = res.data

    // Initialize defaults and load dynamic options
    template.value.parameters_config.forEach(async (p) => {
      formValues.value[p.key] = p.default || ''

      if (p.type === 'api_dynamic_select') {
        await loadDynamicOptions(p)
      }
    })
  } catch (err) {
    alert('Error loading template')
  }
})

const loadDynamicOptions = async (param) => {
  loadingOptions.value[param.key] = true
  try {
    // Call proxy
    const res = await axios.post('/api/v1/render/proxy', {
      target_url: param.extension.data_source_url
    })

    // Assume res.data is a list of objects
    const list = Array.isArray(res.data) ? res.data : []

    // Map to label/value
    const labelKey = param.extension.label_field
    const valueKey = param.extension.value_field

    optionsMap.value[param.key] = list.map(item => ({
      label: item[labelKey],
      val: item[valueKey]
    }))
  } catch (err) {
    console.error(err)
    optionsMap.value[param.key] = []
  } finally {
    loadingOptions.value[param.key] = false
  }
}

const processExcelInput = (key) => {
  const raw = excelInputs.value[key] || ''
  // Convert tab-separated values to Markdown table
  const lines = raw.trim().split('\n')
  if (lines.length === 0) {
    formValues.value[key] = ''
    return
  }

  // Try to detect columns
  const rows = lines.map(line => line.split('\t'))
  // If only one column, maybe it's CSV? Let's assume TSV for Excel copy-paste.

  // Format as markdown
  if (rows.length === 0) return

  const headers = rows[0]
  const separator = headers.map(() => '---')

  let md = '| ' + headers.join(' | ') + ' |\n'
  md += '| ' + separator.join(' | ') + ' |\n'

  for (let i = 1; i < rows.length; i++) {
    md += '| ' + rows[i].join(' | ') + ' |\n'
  }

  formValues.value[key] = md
}

const generate = async () => {
  try {
    const res = await axios.post('/api/v1/render/execute', {
      template_id: template.value.id,
      params: formValues.value
    })
    result.value = res.data.prompt
  } catch (err) {
    alert('Error generating: ' + err.message)
  }
}
</script>
