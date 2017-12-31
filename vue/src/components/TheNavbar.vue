<template>
  <nav class="navbar sticky-top navbar-dark bg-dark">
    <div class="navbar-brand">
      <span class="mr-2" v-if="mode == 'BACK'" @click="goBackHandler">
        <i class="fas fa-angle-left fa-lg" style="color: white;"></i>
      </span>
      <router-link :to="{ name: 'leagues' }" class="mr-2" v-else>
        <img src="/static/swiss-256.png" width="24" height="24" alt="" class="brand-icon mb-1"/>
      </router-link>
      {{ title }}
    </div>

    <slot>
    </slot>
  </nav>
</template>

<script>
export default {
  name: 'TheNavbar',

  props: {
    title: {
      type: String,
      default: '스위스라운드'
    },
    mode: {
      type: String,
      default: 'BACK'
    },
    goBack: {
      type: Function,
      default: null
    }
  },

  data: function () {
    return { }
  },

  methods: {
    goBackHandler: function () {
      this.goBack ? this.goBack() : this.$router.go(-1)
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .brand-icon {
    border-radius: .5rem;
  }
</style>
