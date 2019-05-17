<template>
  <div>
    <the-navbar title="플레이어 추가">
    </the-navbar>

    <the-player-form
      :player="player"
      :submitCallback="submit"/>
  </div>
</template>

<script>
import ThePlayerForm from '@/components/ThePlayerForm'

export default {
  name: 'PlayerAddPage',

  components: {
    'the-player-form': ThePlayerForm
  },

  data: function () {
    return {
      player: {}
    }
  },

  methods: {
    submit: function () {
      return this.$axios.swiss.post(`league/${this.$route.params.league_id}/player`, this.player)
        .then(() => {
          this.player = {}
        })
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
