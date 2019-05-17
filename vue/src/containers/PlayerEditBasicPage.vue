<template>
  <div>
    <the-navbar title="플레이어 수정">
    </the-navbar>

    <the-player-form
      :player="player"
      :submitCallback="submit"/>
  </div>
</template>

<script>
import ThePlayerForm from '@/components/ThePlayerForm'

export default {
  name: 'PlayerEditBasicPage',

  components: {
    'the-player-form': ThePlayerForm
  },

  data: function () {
    return {
      player: {}
    }
  },

  created: function () {
    this.$axios.swiss.get(`league/${this.$route.params.league_id}/player/${this.$route.params.player_id}`)
      .then(res => {
        this.player = res.data.player
      })
  },

  methods: {
    submit: function () {
      return this.$axios.swiss.put(`league/${this.$route.params.league_id}/player/${this.$route.params.player_id}`, this.player)
        .then(() => this.$router.go(-1))
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
