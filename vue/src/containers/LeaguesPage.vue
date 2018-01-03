<template>
  <div>
    <the-navbar mode="HOME">
      <button type="button" class="btn btn-primary" @click="create">생성</button>
    </the-navbar>

    <the-loading ref="loading">
      <div class="list-group">
        <router-link
           :to="{name: 'league', params: {league_id: league.id}}"
           v-for="(league, index) in leagues"
           :key="league.id"
           class="list-group-item list-group-item-action border-left-0 border-right-0"
        >
          {{ league.title }}
        </router-link>
      </div>
    </the-loading>
  </div>
</template>

<script>
export default {
  name: 'LeaguesPage',

  data: function () {
    return {
      leagues: []
    }
  },

  created: function () {
    this.$axios.swiss.get('leagues')
      .then(res => {
        this.leagues = res.data.leagues
        this.$refs.loading.stop()
      })
  },

  methods: {
    create: function () {
      this.$router.push({ name: 'leagueCreate' })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
