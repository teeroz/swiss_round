<template>
  <div>
    <the-navbar title="리그 수정">
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
  name: 'LeagueEditPage',

  components: {
    'the-league-form': TheLeagueForm
  },

  data: function () {
    return {
      league: {},
      defaultTitle: ''
    }
  },

  created: function () {
    this.$axios.swiss.get(`league/${this.$route.params.league_id}`)
      .then(res => {
        this.league = res.data.league
        this.defaultTitle = res.data.league.title
      })
  },

  methods: {
    submit: function () {
      this.$axios.swiss.put(`league/${this.$route.params.league_id}`, this.league)
        .then(() => this.$router.push({ name: 'league', params: { id: this.$route.params.league_id } }))
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
