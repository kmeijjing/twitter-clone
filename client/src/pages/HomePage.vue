<template>
  <q-page class="home-page flex row no-wrap">
    <div class="page-container">
      <div class="page-header">
        Home
      </div>

      <AddPostCard @success="addTweetOk" class="q-mt-md" />
      <q-separator class="q-mt-md" />

      <q-card flat>
        <q-list>
          <PostCard
            v-for="(t, i) in timelineArr"
            :key="t.id"
            :idx="i"
            :id="t.id"
            :account_id="t.account_id"
            :name="t.name"
            :email="t.email"
            :profile_image="t.profile_image"
            :created="t.created_at"
            :tweet="t.tweet"
            :like="t.like"
            :like_count="t.like_count"
            :uploads="t.uploads"
            @like="like(i)"
            @delete="deleteTweet(i)"
          />
        </q-list>
      </q-card>
    </div>

    <RightSideBar v-if="$q.screen.width >= 1020" />
  </q-page>
</template>

<script>
import { ref, onBeforeMount } from "vue";
import {
  roundComment,
  roundCached,
  roundFavoriteBorder,
  roundIosShare,
} from "@quasar/extras/material-icons-round";
import AddPostCard from "@components/AddPostCard.vue";
import PostCard from "@components/PostCard.vue";
import RightSideBar from "@layouts/RightSideBar.vue";


export default {
  name: "HomePage",
  components: { AddPostCard, PostCard, RightSideBar },
  setup() {
    const tweetContent = ref("");
    const timelineArr = ref([]);

    function getTimeline() {
      timelineArr.value = [
        {
          id: 1,
          user_id: 1,
          name: "John Doe",
          account_id: "@user",
          email: "hzdkv@example.com",
          profile_image: "",
          created_at: "2021-01-01 00:00:00",
          tweet:
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
          like: false,
          like_count: 0,
          uploads: "",
        },
        {
          id: 2,
          user_id: 1,
          name: "John Doe",
          account_id: "@user",
          email: "hzdkv@example.com",
          profile_image: "",
          created_at: "2021-01-01 00:00:00",
          tweet:
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
          like: false,
          like_count: 0,
          uploads: "",
        },
        {
          id: 3,
          user_id: 1,
          name: "John Doe",
          account_id: "@user",
          email: "hzdkv@example.com",
          profile_image: "",
          created_at: "2021-01-01 00:00:00",
          tweet:
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
          like: false,
          like_count: 0,
          uploads: "",
        },
        {
          id: 4,
          user_id: 1,
          name: "John Doe",
          account_id: "@user",
          email: "hzdkv@example.com",
          profile_image: "",
          created_at: "2021-01-01 00:00:00",
          tweet:
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
          like: false,
          like_count: 0,
          uploads: "",
        }
      ]
    }

    function like(idx) {
      if (timelineArr.value[idx].like === true) {
        timelineArr.value[idx].like_count -= 1;
      } else {
        timelineArr.value[idx].like_count += 1;
      }
      timelineArr.value[idx].like = !timelineArr.value[idx].like;
    }

    function deleteTweet(idx) {
    }

    function addTweetOk() {
      getTimeline();
    }

    onBeforeMount(() => {
      getTimeline();
    });

    return {
      roundComment,
      roundCached,
      roundFavoriteBorder,
      roundIosShare,

      tweetContent,
      timelineArr,

      like,
      deleteTweet,

      addTweetOk,
    };
  },
};
</script>

<style lang="scss">
.home-page {
  > .page-container {
    max-width: 600px;
    padding: 0 0 20px;
  }
}
</style>
