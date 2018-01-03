<template>
  <div>
    <the-navbar :title="thisPlayer.name + '의 가족설정'">
    </the-navbar>

    <div class="container form-group">
      <div class="card mt-3">
        <ul class="list-group list-group-flush">
          <li 
            v-for="(player, index) in players"
            :key="player.id"
            class="list-group-item align-items-center"
            >
            <div class="form-check ml-4 mb-0">
              <input 
                type="checkbox" 
                class="form-check-input" 
                style="margin-top: .4rem!important" 
                :id="'checkbox_' + player.id"
                :value="player.id"
                v-model="familyMembers"
                >
              <label class="form-check-label pl-1" :for="'checkbox_' + player.id">{{ player.name }}</label>
            </div>
          </li>
        </ul>
      </div>

      <div class="d-flex justify-content-end mt-3">
        <button type="button" class="btn btn-secondary col-2 mx-2" @click="cancel">취소</button>
        <button type="submit" class="btn btn-primary col-2" @click="submit">확인</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PlayerEditFamilyPage',

  data: function () {
    return {
      thisPlayer: { name: '' },
      players: [],
      familyMembers: []
    }
  },

  created: function () {
    this.$axios.swiss.get(`league/${this.$route.params.league_id}/player/${this.$route.params.player_id}`)
      .then(res => {
        this.thisPlayer = res.data.player
        this.familyMembers = this.thisPlayer.family.map(m => m['id'])

        this.$axios.swiss.get(`league/${this.$route.params.league_id}`)
          .then(res => {
            const players = res.data.players.filter(player => player.id !== this.thisPlayer.id)
            players.sort((a, b) => a.name > b.name)
            this.players = players
          })
      })
  },

  methods: {
    cancel: function () {
      this.$router.go(-1)
    },

    submit: function () {
      this.$axios.swiss.put(`league/${this.$route.params.league_id}/player/${this.$route.params.player_id}`,
                            { 'family': this.familyMembers })
        .then(res => this.$router.go(-1))
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
