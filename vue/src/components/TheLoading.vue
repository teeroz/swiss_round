<template>
  <div>
    <div v-if="isLoading" class="loading">
      <img src="/static/loading.gif" width="100%"/>
    </div>
    <div v-else>
      <slot>
      </slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TheLoading',

  data: function () {
    return {
      isLoading: true
    }
  },

  methods: {
    stop: function () {
      this.isLoading = false
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .loading {
    min-width: 100%;
    min-height: 100%;
    min-height: 100vh;
    display: flex;
    align-items: center;
    padding-bottom: 3.5rem;
  }
</style>
