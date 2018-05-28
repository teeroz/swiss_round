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
    },
    github: {
      name: 'github',
      url: '/auth/kakao',
      authorizationEndpoint: 'https://kauth.kakao.com/oauth/authorize',
      clientId: '672b24cc4f5d7c23184d378fd6fd3cca',
      redirectUri: 'http://swiss.teeroz.net' + (process.env.NODE_ENV === 'development' ? ':8000' : '') + '/', // Your client app URL
      scope: null,
      scopeDelimiter: null,
      oauthType: '2.0',
      popupOptions: { width: 360, height: 450 }
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
