import Vue from 'vue'
import Router from 'vue-router'
import AjaxPlugin from '@/plugins/AjaxPlugin'
import TheNavbar from '@/components/TheNavbar'
import TheLoading from '@/components/TheLoading'
import LeaguesPage from '@/containers/LeaguesPage'
import LeaguePage from '@/containers/LeaguePage'
import LeagueCreatePage from '@/containers/LeagueCreatePage'
import LeagueEditPage from '@/containers/LeagueEditPage'
import PlayerAddPage from '@/containers/PlayerAddPage'
import PlayerEditBasicPage from '@/containers/PlayerEditBasicPage'
import PlayerEditFamilyPage from '@/containers/PlayerEditFamilyPage'
import PlayerPage from '@/containers/PlayerPage'
import RoundPage from '@/containers/RoundPage'

Vue.use(Router)
Vue.use(AjaxPlugin)
Vue.component('the-navbar', TheNavbar)
Vue.component('the-loading', TheLoading)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'leagues',
      component: LeaguesPage
    },
    {
      path: '/league/:league_id',
      name: 'league',
      component: LeaguePage
    },
    {
      path: '/league/create',
      name: 'leagueCreate',
      component: LeagueCreatePage
    },
    {
      path: '/league/:league_id/edit',
      name: 'leagueEdit',
      component: LeagueEditPage
    },
    {
      path: '/league/:league_id/player/add',
      name: 'playerAdd',
      component: PlayerAddPage
    },
    {
      path: '/league/:league_id/player/:player_id',
      name: 'player',
      component: PlayerPage
    },
    {
      path: '/league/:league_id/player/:player_id/edit/basic',
      name: 'playerEditBasic',
      component: PlayerEditBasicPage
    },
    {
      path: '/league/:league_id/player/:player_id/edit/family',
      name: 'playerEditFamily',
      component: PlayerEditFamilyPage
    },
    {
      path: '/league/:league_id/round/:round_id',
      name: 'round',
      component: RoundPage
    }
  ]
})
