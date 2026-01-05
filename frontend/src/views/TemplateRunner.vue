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
          <div v-if="param.description" style="font-size: 0.8em; color: gray; margin-bottom: 5px;">{{ param.description }}</div>

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
             <!-- Query Parameters -->
             <div v-if="param.extension.query_params && param.extension.query_params.length > 0" style="margin-bottom: 5px;">
               <div v-for="qp in param.extension.query_params" :key="qp" style="display: flex; gap: 5px; margin-bottom: 2px;">
                 <span style="font-size: 0.9em;">{{ qp }}:</span>
                 <input v-model="dynamicQueryParams[param.key][qp]" style="width: 150px;" placeholder="Value" />
               </div>
               <button @click="loadDynamicOptions(param)" style="font-size: 0.8em;">Refresh Options</button>
             </div>

             <div v-if="loadingOptions[param.key]">Loading options...</div>
             <select v-else v-model="formValues[param.key]" :multiple="param.extension.allow_multiple" style="width: 100%;">
               <option v-for="opt in (optionsMap[param.key] || [])" :key="opt.val" :value="opt.val">
                 {{ opt.label }}
               </option>
             </select>
          </div>

          <!-- Dify KB Search -->
          <div v-else-if="param.type === 'dify_kb_search'">
             <div style="display: flex; gap: 10px; margin-bottom: 5px;">
               <input v-model="kbSearchInputs[param.key]" placeholder="输入关键词检索..." style="flex: 1;" />
               <button @click="performDifySearch(param)">检索</button>
             </div>

             <div v-if="kbSearchResults[param.key]" style="max-height: 200px; overflow-y: auto; border: 1px solid #eee; padding: 5px; margin-bottom: 5px;">
               <div v-for="(item, idx) in kbSearchResults[param.key]" :key="idx"
                    style="padding: 5px; border-bottom: 1px dashed #eee; font-size: 0.9em; display: flex; align-items: start; gap: 5px;">
                 <input type="checkbox" v-model="item.selected" style="margin-top: 3px;" />
                 <div>
                   <div style="font-weight: bold;">Score: {{ item.score }}</div>
                   <div style="color: #666;">{{ item.content.substring(0, 100) }}...</div>
                 </div>
               </div>
             </div>
             <button v-if="kbSearchResults[param.key] && kbSearchResults[param.key].length > 0"
                     @click="confirmDifySelection(param)"
                     style="margin-bottom: 5px; font-size: 0.9em;">Confirm Selection</button>

             <textarea v-model="formValues[param.key]" placeholder="Selected content or manual input" style="width: 100%; height: 80px;"></textarea>
          </div>

          <!-- Summary KB Search -->
          <div v-else-if="param.type === 'summary_kb_search'">
             <div style="display: flex; gap: 10px; margin-bottom: 5px;">
               <input v-model="summarySearchInputs[param.key]" placeholder="输入内容检索摘要..." style="flex: 1;" />
               <button @click="performSummarySearch(param)">查询</button>
             </div>

             <div v-if="summarySearchResults[param.key]" style="margin-bottom: 10px;">
               <table style="width: 100%; border-collapse: collapse; font-size: 0.9em;">
                 <thead>
                   <tr style="background: #eee;">
                     <th style="border: 1px solid #ccc; padding: 5px;">Select</th>
                     <th v-for="col in param.extension.abstract_columns" :key="col" style="border: 1px solid #ccc; padding: 5px;">{{ col }}</th>
                     <th style="border: 1px solid #ccc; padding: 5px;">Score</th>
                   </tr>
                 </thead>
                 <tbody>
                   <tr v-for="(row, idx) in summarySearchResults[param.key]" :key="idx">
                     <td style="border: 1px solid #ccc; padding: 5px; text-align: center;">
                       <input type="checkbox" v-model="row.selected" />
                     </td>
                     <td v-for="col in param.extension.abstract_columns" :key="col" style="border: 1px solid #ccc; padding: 5px;">
                       {{ row.abstract[col] }}
                     </td>
                     <td style="border: 1px solid #ccc; padding: 5px;">{{ row.score ? row.score.toFixed(2) : '' }}</td>
                   </tr>
                 </tbody>
               </table>
               <button @click="confirmSummarySelection(param)" style="margin-top: 5px;">确认选择</button>
             </div>

             <textarea v-model="formValues[param.key]" placeholder="最终结果" style="width: 100%; height: 100px;"></textarea>
          </div>

          <!-- Excel Input -->
          <div v-else-if="param.type === 'excel'">
             <div v-if="param.extension.headers && param.extension.headers.length > 0" style="margin-bottom: 5px; font-weight: bold;">
               Columns: {{ param.extension.headers.join(' | ') }}
             </div>
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
const dynamicQueryParams = ref({})
// For KB Search
const kbSearchInputs = ref({})
const kbSearchResults = ref({})
// For Summary Search
const summarySearchInputs = ref({})
const summarySearchResults = ref({})
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
        // Init query params storage
        dynamicQueryParams.value[p.key] = {}
        if (p.extension.query_params) {
           p.extension.query_params.forEach(qp => {
             dynamicQueryParams.value[p.key][qp] = ''
           })
        }
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
    // Call proxy with params
    const query = dynamicQueryParams.value[param.key] || {}
    // Construct url with params if needed, but for now assuming backend proxy handles query params or body
    // Ideally we append to URL or send as payload. Let's send as payload.
    const res = await axios.post('/api/v1/render/proxy', {
      target_url: param.extension.data_source_url,
      query_params: query
    })

    // Assume res.data is a list of objects
    const list = Array.isArray(res.data) ? res.data : []

    // Map to label/value. Logic: try label/value fields if configured, else try infer, else fallback.
    // The requirement says: remove config for label/value, frontend logic default fallback.
    // "Default label_example1:value_example1 if not standard"

    optionsMap.value[param.key] = list.map(item => {
      // Check if item has label/value or label/val or name/id
      let label = item.label || item.name || item.text
      let val = item.value || item.val || item.id

      if (label === undefined || val === undefined) {
         // Fallback: use first two keys or just stringify
         const keys = Object.keys(item)
         if (keys.length >= 2) {
             // Heuristic: assume string keys might be label/val
             label = item[keys[0]]
             val = item[keys[1]]
         } else if (keys.length === 1) {
             label = item[keys[0]]
             val = item[keys[0]]
         } else {
             // Scalar or empty
             label = String(item)
             val = String(item)
         }
      }
      return { label, val }
    })
  } catch (err) {
    console.error(err)
    // Fallback logic for error or empty? Requirement says default logic for display if result doesn't match.
    // But here we might just have empty list on error.
    optionsMap.value[param.key] = []
  } finally {
    loadingOptions.value[param.key] = false
  }
}

const performDifySearch = async (param) => {
  const query = kbSearchInputs.value[param.key]
  if (!query) return

  try {
    // This is a proxy call to the configured base_url via backend
    const res = await axios.post('/api/v1/render/proxy', {
      target_url: param.extension.base_url, // Or a specific Dify endpoint
      method: 'POST',
      headers: { 'Authorization': `Bearer ${param.extension.api_key}` },
      data: {
         inputs: {},
         query: query,
         response_mode: 'blocking',
         user: 'abc-123',
         dataset_id: param.extension.dataset_id,
         // Pass configured search parameters
         search_method: param.extension.search_method,
         top_k: param.extension.top_k,
         score_threshold: param.extension.score_threshold,
         vector_weight: param.extension.vector_weight
      }
      // Note: Actual Dify API might differ, implementing generic proxy per requirement
    })

    // Mock result for now if proxy returns raw or assume specific format
    // Requirement says "Dify Knowledge Base Retrieval"
    // Assuming backend proxy handles the details or we get a standard list back.
    // For now, let's assume we get a list of segments.

    // IF it is a custom proxy, let's assume it returns { records: [] }
    const data = res.data
    // TODO: adjust based on actual response format
    kbSearchResults.value[param.key] = data.records || []
  } catch (err) {
    console.error(err)
    alert('Search failed')
  }
}

const confirmDifySelection = (param) => {
  const results = kbSearchResults.value[param.key] || []
  const selected = results.filter(r => r.selected)

  // Concatenate documents
  const content = selected.map(r => r.content).join('\n\n')
  formValues.value[param.key] = content
}

const performSummarySearch = async (param) => {
  const query = summarySearchInputs.value[param.key]
  if (!query) return

  try {
    const res = await axios.post('/api/v1/render/proxy', {
      target_url: param.extension.base_url,
      method: 'POST',
      data: { query }
    })

    // Expecting { success_status: True, records: [ { score, segment: { abstract: {}, document: "" } } ] }
    if (res.data && res.data.records) {
       summarySearchResults.value[param.key] = res.data.records.map(r => ({
         ...r,
         selected: r.score >= (param.extension.score_threshold || 0.6)
       }))
    }
  } catch (err) {
    alert('Search failed: ' + err.message)
  }
}

const confirmSummarySelection = (param) => {
  const results = summarySearchResults.value[param.key] || []
  const selected = results.filter(r => r.selected)

  // Concatenate documents
  const content = selected.map(r => r.segment.document).join('\n\n')
  formValues.value[param.key] = content
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
