<template>
  <div class="post-tab-content">
    <q-list>
      <PostCard
        v-for="(t, i) in postListArr"
        :key="t.id"
        :idx="i"
        :id="t.id"
        :user_id="t.user_id"
        :name="t.name"
        :email="t.email"
        :profile_image="t.profile_image"
        :created="t.created_at"
        :tweet="t.tweet"
        :like="t.like"
        :like_count="t.like_count"
        :uploads="t.uploads"
        @delete:post="onDeletePost(i)"
        @update:like="onUpdatelike(i)"
      />
      <q-inner-loading
        :showing="isLoading"
        color="primary"
        style="height: 250px;"
      />
    </q-list>
    <RandomFollowList />
  </div>
</template>

<script>
import { ref, onBeforeMount } from "vue";
import { Notify, Cookies } from "quasar";
import { api } from "@boot/axios";

import PostCard from "../PostCard.vue";
import RandomFollowList from "../RandomFollowList.vue";

export default {
  name: "PostTabContent",
  components: { PostCard, RandomFollowList },
  setup() {
    const isLoading = ref(false);
    const postListArr = ref([]);
    function getPostList() {
      isLoading.value = true;
      const user = Cookies.get('user');
      api.get(`/my-timeline/${user.id}`).then((res) => {
        postListArr.value = res.data.timeline.reverse();
        postListArr.value.forEach((t) => {
          if (t.uploads) {
            t.uploads = t.uploads.split(" ");
            t.uploads.pop();
          }
        })
      }).catch((err) => {
        console.log(err);
      }).finally(() => {
        isLoading.value = false;
      });
    }

    function onUpdatelike(idx) {
      if (postListArr.value[idx].like === true) {
        postListArr.value[idx].like_count -= 1;
      } else {
        postListArr.value[idx].like_count += 1;
      }
      postListArr.value[idx].like = !postListArr.value[idx].like;

    }

    function onDeletePost(idx) {
      let tweetId = postListArr.value[idx].id;
      const userId = Cookies.get('user').id;

      api.delete(`/tweet/${tweetId}/${userId}`).then(() => {
        postListArr.value.splice(idx, 1);
      }).catch((err) => {
        console.log(err);
      })
    }

    onBeforeMount(() => {
      getPostList();
    })

    return {
      isLoading,
      postListArr,
      onUpdatelike,
      onDeletePost,
    };
  },
};
</script>

<style lang="scss">
.post-tab-content {
  .random-follow-list {
    border-radius: 0 !important;
  }
}
</style>
