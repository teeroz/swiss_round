<template>
  <div>
    <the-navbar mode="HOME">
      <div>
        <span class="navbar-text mr-1">{{ username }}</span>
        <button type="button" class="btn btn-secondary navbar-toggler" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          <i class="fas fa-bars"></i>
        </button>
        <div class="dropdown-menu" style="right: 0; left: auto;">
          <button type="button" class="dropdown-item" @click="logout">로그아웃</button>
        </div>
      </div>
    </the-navbar>

    <the-loading ref="loading">
      <div class="list-group">
        <router-link
           :to="{name: 'leagueCreate'}"
           class="list-group-item list-group-item-action border-left-0 border-right-0 text-primary"
           >
          <i class="fas fa-plus"></i> <strong><span class="ml-1">리그 추가하기</span></strong>
        </router-link>
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
      username: '',
      leagues: []
    }
  },

  created: function () {
    this.$axios.swiss.get('leagues')
      .then(res => {
        this.leagues = res.data.leagues
        this.$refs.loading.stop()

        if (typeof this.$auth.user === 'undefined') {
          this.$axios.facebook.get('me', {access_token: this.$auth.getToken()})
            .then(res => {
              this.$auth.user = res.data
              this.username = this.$auth.user.name
            })
        } else {
          this.username = this.$auth.user.name
        }
      })
  },

  methods: {
    create: function () {
      this.$router.push({ name: 'leagueCreate' })
    },

    logout: function () {
      this.$auth.logout()
      this.$router.push({ name: 'login' })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
