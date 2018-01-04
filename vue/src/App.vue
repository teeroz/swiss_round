<template>
  <div id="app">
    <router-view :key="$route.path"/>
  </div>
</template>

<script>
import Vue from 'vue'

import AjaxPlugin from '@/plugins/AjaxPlugin'

import TheNavbar from '@/components/TheNavbar'
import TheLoading from '@/components/TheLoading'

Vue.use(AjaxPlugin)

Vue.component('the-navbar', TheNavbar)
Vue.component('the-loading', TheLoading)

export default {
  name: 'app'
}
</script>
  
<style>
.list-group-item:first-child {
  border-top: 0;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
</style>
