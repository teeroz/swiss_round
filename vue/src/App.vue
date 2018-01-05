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

import VueAxios from 'vue-axios'
import VueAuthenticate from 'vue-authenticate'
import axios from 'axios'

Vue.use(AjaxPlugin)

Vue.component('the-navbar', TheNavbar)
Vue.component('the-loading', TheLoading)

Vue.use(VueAxios, axios)
Vue.use(VueAuthenticate, {
  // Your API domain
  baseUrl: 'http://swiss.teeroz.net:8080/swiss/api',

  providers: {
    facebook: {
      clientId: '1713079558713926',
      redirectUri: 'http://swiss.teeroz.net' + (process.env.NODE_ENV === 'development' ? ':8000' : '') + '/' // Your client app URL
    }
  }
})

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
