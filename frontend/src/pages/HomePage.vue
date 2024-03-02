<template>
  <q-page class="home-page flex row no-wrap" @wheel="onWheel">
    <div class="page-container full-width">
      <div class="page-header">
        <div class="title">
          Home
        </div>
      </div>

      <AddPostCard @success="addPostSuccess" class="q-mt-md" />

      <q-separator class="q-mt-md" style="background: rgb(239, 243, 244)" />

      <q-card flat>
        <q-card-section v-if="!postListArr.length">
          <div class="text-center text-grey-8 q-py-xl">
            <div class="text-h6">No Post</div>
            <div class="text-subtitle1">
              포스트가 없습니다.
            </div>
          </div>
        </q-card-section>
        <q-list v-else>
          <PostCard
            v-for="(t, i) in postListArr"
            :key="t.id"
            :idx="i"
            :id="t.id"
            :user_id="t.user_ids"
            :name="t.name"
            :email="t.email"
            :profile_image="t.profile_image"
            :created="t.created_at"
            :tweet="t.tweet"
            :like="t.like"
            :like_count="t.like_count"
            :uploads="t.uploads"
            @update:like="onUpdatelike(i)"
            @delete="onDeletePost(i)"
          />
        </q-list>
      </q-card>
    </div>

    <RightSideBar :mouseDeltaY="mouseDeltaY" />
  </q-page>
</template>

<script>
import { ref, onBeforeMount } from "vue";
import { api } from "@boot/axios";
import { Cookies } from "quasar";
import AddPostCard from "@components/AddPostCard.vue";
import PostCard from "@components/PostCard.vue";
import RightSideBar from "@layouts/RightSideBar.vue";


export default {
  name: "HomePage",
  components: { AddPostCard, PostCard, RightSideBar },
  setup() {
    const postListArr = ref([]);

    function getTimeline() {
      const user = Cookies.get('user');
      const params = {
        user_id: user.id,
        keyword: ''
,      }
      api.get('/timeline', { params }).then((res) => {
        postListArr.value = res.data.timeline.reverse();
        postListArr.value.forEach((t) => {
          if (t.uploads) {
            t.uploads = t.uploads.split(" ");
            t.uploads.pop();
          }
        })
      }).catch((err) => {
        console.log(err);
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

    function addPostSuccess() {
      getTimeline();
    }

    onBeforeMount(() => {
      getTimeline();
    });

    const mouseDeltaY = ref(0);
    function onWheel(event) {
      mouseDeltaY.value = event.deltaY;
    }

    return {
      postListArr,

      onUpdatelike,
      onDeletePost,

      addPostSuccess,
      onWheel,
      mouseDeltaY,
    };
  },
};
</script>

<style lang="scss">
.home-page {
  > .page-container {
    max-width: 600px;
    padding: 0 0 20px;
    border-right: 1px solid rgb(239, 243, 244);
  }
}
</style>
