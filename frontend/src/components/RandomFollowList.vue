<template>
  <q-card flat class="random-follow-list">
    <div class="card-title">Who to follow</div>
    <q-list>
      <RandomFollowListItem
        v-for="(u, i) in randomUsers"
        :key="i"
        :id="u.id"
        :name="u.name"
        :email="u.email"
        :bio="u.bio"
        :bioShow="false"
        :profile_image="u.profile_image"
      />
      <q-item clickable>
        <q-item-section class="text-primary">
          Show more
        </q-item-section>
      </q-item>
    </q-list>
  </q-card>
</template>

<script>
import { ref, onBeforeMount } from "vue";
import { Cookies } from "quasar";
import { api } from "@boot/axios";
import RandomFollowListItem from "@components/RandomFollowListItem.vue";

export default {
  name: "RandomFollowList",
  components: { RandomFollowListItem },
  setup () {
    const user = Cookies.get('user');
    const randomUsers = ref([]);

    function getUserRandom() {
      api
        .get(`/random-users/${user.id}`)
        .then((res) => {
          console.log(res);
          res.data.forEach((u) => {
            randomUsers.value.push({
              id: u.id,
              name: u.name,
              email: u.email,
              profile_image: u.profile_image
            });
          });
        })
        .catch((err) => {
          console.log(err);
        });
    }

    onBeforeMount(() => {
      getUserRandom();
    })

    return {
      randomUsers,
    }
  }

}
</script>

<style lang="scss">
.random-follow-list {
  overflow: hidden;
  .desc {
    padding: 0 16px;
    margin: -10px 0 12px;
    font-size: 13px;
    color: $grey-7;
  }
  .chips {
    padding: 0 16px;
    .q-chip {
      &__content {
        margin-right: 10px;
      }
    }
  }
}
</style>
