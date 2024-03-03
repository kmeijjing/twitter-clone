<template>
  <q-page class="other-profile-page">
    <div class="page-container">
      <div class="page-header flex row items-center">
        <q-btn
          flat
          dense
          round
          :ripple="false"
          icon="arrow_back"
          class="q-mr-md"
          @click="$router.go(-1)"
        />
        <div>
          <div class="title">{{ user.name }}</div>
          <div class="subtitle" style="font-size: 13px">{{ myTimeline.length || 0 }} Posts</div>
        </div>
      </div>

      <ProfileInfoCard
        :user="user"
        :follows="follows"
        @update:user="getUser"
      />

      <div class="tabs-container">
        <q-tabs
          v-model="tab"
          dense
          class="text-grey"
          active-color="primary"
          indicator-color="primary"
          align="justify"
          narrow-indicator
        >
          <q-tab
            v-for="(t, i) in tabOptions.filter((v) => !v.private)"
            :key="i"
            no-caps
            :name="t.name"
            :value="t.value"
            :label="t.name"
            :ripple="false"
          />
        </q-tabs>
        <q-separator />

        <q-tab-panels
          v-model="tab"
          animated
          class="full-width"
        >
          <q-tab-panel name="Posts">
            <PostCard
              v-for="(t, i) in myTimeline"
              :key="t.id"
              :id="t.id"
              :user_id="t.user_id"
              :name="t.name"
              :email="t.email"
              :created="t.created_at"
              :tweet="t.tweet"
              :like_count="t.like_count"
              :like="t.like"
              @update:like="clickLike(i)"
            />
          </q-tab-panel>
        </q-tab-panels>
      </div>
    </div>
  </q-page>
</template>

<script>
import { ref, onBeforeMount } from "vue";
import { Dialog } from "quasar";
import { api } from "@boot/axios";
import { useRoute, useRouter } from "vue-router";
import { tabOptions } from "src/constants/profile";
import ProfileInfoCard from "@components/profile/ProfileInfoCard.vue";
import PostCard from "src/components/PostCard.vue";

export default {
  name: 'OtherProfilePage',
  components: { ProfileInfoCard, PostCard },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const tab = ref("Posts");

    const user = ref({});
    function getUser(userId) {
      api
        .get(`/user/${userId}`)
        .then((res) => {
          user.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    }

    const follows = ref({
      followings: [],
      followers: [],
    });
    function getFollow(userId) {
      api
        .get(`/follow/${userId}`)
        .then((res) => {
          follows.value.followings = res.data.followings;
          follows.value.followers = res.data.followings;
        })
        .catch((err) => {
          console.log(err);
        });
    }

    const myTimeline = ref([]);
    function getMyTimeline(userId) {
      api
        .get(`/my-timeline/${userId}`)
        .then((res) => {
          myTimeline.value = res.data.timeline;
        })
        .catch((err) => {
          console.log(err);
        });
    }

    function clickLike(idx) {
      if (myTimeline.value[idx].like === true) {
        myTimeline.value[idx].like_count -= 1;
      } else {
        myTimeline.value[idx].like_count += 1;
      }
      myTimeline.value[idx].like = !myTimeline.value[idx].like;
    }

    onBeforeMount(() => {
      const userId = route.params.userId;
      getUser(userId);
      getFollow(userId);
      getMyTimeline(userId);
    });

    return {
      tabOptions,
      router,

      tab,
      user,
      follows,
      getUser,
      myTimeline,
      clickLike,
    };
  },
};
</script>

<style lang="scss">
.other-profile-page {
  .page-container {
    max-width: 600px;
    padding: 0 0 20px;
    border-right: 1px solid rgb(239, 243, 244);
  }

  .tabs-container {
    margin-top: 20px;
    .q-tabs {
      height: 40px;
    }
    .q-tab-panels {
      .q-panel {
        .q-tab-panel {
          padding: 16px 0;
        }
      }
    }
  }
}
</style>
