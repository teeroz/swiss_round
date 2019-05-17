<template>
  <div>
    <the-navbar title="리그 생성">
    </the-navbar>

    <the-league-form
      :league="league"
      :defaultTitle="defaultTitle"
      :submitCallback="submit"/>
  </div>
</template>

<script>
import TheLeagueForm from '@/components/TheLeagueForm'

export default {
  name: 'LeagueCreatePage',

  components: {
    'the-league-form': TheLeagueForm
  },

  data: function () {
    return {
      league: {},
      defaultTitle: new Date().toLocaleDateString('ko-KR')
    }
  },

  methods: {
    submit: function () {
      this.$axios.swiss.post('league', this.league)
        .then(() => this.$router.push({ name: 'leagues' }))
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
