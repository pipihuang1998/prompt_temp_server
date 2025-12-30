<template>
  <div style="font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px;">
    <nav style="margin-bottom: 20px; border-bottom: 1px solid #ccc; padding-bottom: 10px;">
      <router-link to="/" style="margin-right: 15px;">Home / List</router-link>
      <router-link to="/create">Create New Template</router-link>
    </nav>
    <router-view></router-view>
  </div>
</template>

<style>
button {
  padding: 8px 16px;
  cursor: pointer;
}
input, select, textarea {
  padding: 6px;
  margin-bottom: 5px;
}
label {
  display: block;
  font-weight: bold;
  margin-top: 10px;
}
</style>
