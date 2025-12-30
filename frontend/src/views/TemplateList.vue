<template>
  <div>
    <h1>Template List</h1>
    <div v-if="loading">Loading...</div>
    <table v-else style="width: 100%; border-collapse: collapse;">
      <thead>
        <tr style="background: #f0f0f0; text-align: left;">
          <th style="padding: 10px;">ID</th>
          <th style="padding: 10px;">Name</th>
          <th style="padding: 10px;">Description</th>
          <th style="padding: 10px;">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in templates" :key="item.id" style="border-bottom: 1px solid #eee;">
          <td style="padding: 10px;">{{ item.id }}</td>
          <td style="padding: 10px;">{{ item.name }}</td>
          <td style="padding: 10px;">{{ item.temp_description }}</td>
          <td style="padding: 10px;">
            <button @click="$router.push(`/edit/${item.id}`)">Edit</button>
            <button @click="$router.push(`/run/${item.id}`)" style="margin-left: 5px;">Run</button>
            <button @click="deleteTemplate(item.id)" style="margin-left: 5px; background: #ffcccc;">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div v-if="templates.length === 0 && !loading">No templates found.</div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const templates = ref([])
const loading = ref(false)

const fetchTemplates = async () => {
  loading.value = true
  try {
    const res = await axios.get('/api/v1/template/list')
    templates.value = res.data.items
  } catch (err) {
    alert('Error fetching templates: ' + err.message)
  } finally {
    loading.value = false
  }
}

const deleteTemplate = async (id) => {
  if (!confirm('Are you sure?')) return
  try {
    await axios.delete(`/api/v1/template/${id}`)
    fetchTemplates()
  } catch (err) {
    alert('Error deleting: ' + err.message)
  }
}

onMounted(fetchTemplates)
</script>
