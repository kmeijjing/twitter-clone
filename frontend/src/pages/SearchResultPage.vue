<template>
  <q-page class="search-result-page flex row no-wrap">
    <div class="page-container full-width">
      <div class="page-header flex no-wrap items-center">
        <q-btn
          flat
          dense
          round
          :ripple="false"
          icon="arrow_back"
          class="q-mr-md"
          @click="$router.go(-1)"
        />
        <SearchForm
          :searchKeyword="keyword"
          @update:keyword="onUpdateKeyword"
        />
        <q-btn
          flat
          dense
          round
          :ripple="false"
          icon="settings"
          class="q-ml-md"
        />
      </div>

      <q-card flat class="search-result-card-container">
        <div v-if="!postListArr.length && !isLoading" class="no-data">
          <div class="title">No results for "{{ keyword }}"</div>
          <div class="desc text-grey-8">
            Try searching for something else, or check your Search settings to see if they’re protecting you from potentially sensitive content.
          </div>
        </div>

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
            @update:like="onUpdatelike(i)"
            @delete="onDeletePost(i)"
          />
        </q-list>

        <q-inner-loading
          :showing="isLoading"
          color="primary"
          style="height: 250px;"
        />
      </q-card>
    </div>

    <RightSideBar :isSearchBar="false" />
  </q-page>
</template>

<script>
import { ref, onBeforeMount } from "vue";
import { Loading, Cookies } from "quasar";
import { api } from "@boot/axios";
import { useRoute } from "vue-router";
import SearchForm from "@components/SearchForm.vue";
import PostCard from "@components/PostCard.vue";
import RightSideBar from "@layouts/RightSideBar.vue";

const tabOptions = [
  { name: "Top", value: "top" },
  { name: "Latest", value: "latest" },
  { name: "People", value: "people" },
  { name: "Photos", value: "photos" },
  { name: "Videos", value: "videos" },
];

export default {
  name: "SearchResultPage",
  components: { SearchForm, PostCard, RightSideBar },
  setup() {
    const isLoading = ref(false);
    const route = useRoute();
    const user = Cookies.get('user');
    const tab = ref("Top");

    const followList = ref([]);
    const people = ref([]);

    function getFollow() {
      followList.value = [];
      api
        .get(`/follow/${user.id}`)
        .then((res) => {
          followList.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        })
        .finally(() => {
          people.value.forEach((p) => {
            followList.value.followings.forEach((f) => {
              if (p.id === f) {
                p.following = true;
              }
            });
          });
        });
    }

    const keyword = ref("");

    const postListArr = ref([]);
    function onSearch(val) {
      if (val) {
        isLoading.value = true;
        const params = {
          user_id: user.id,
          keyword: val,
        }
        api
          .get('timeline', { params }).then((res) => {
            postListArr.value = res.data.timeline.reverse();
            postListArr.value.forEach((t) => {
              if (t.uploads) {
                t.uploads = t.uploads.split(" ");
                t.uploads.pop();
              }
            })
            getFollow();
            people.value = [];
            people.value = res.data;
          })
          .catch((err) => {
            console.log(err);
          })
          .finally(() => {
            isLoading.value = false;
          });
      }
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
      const userId = user.id;
      api.delete(`/tweet/${tweetId}/${userId}`).then(() => {
        postListArr.value.splice(idx, 1);
      }).catch((err) => {
        console.log(err);
      })
    }

    function onUpdateKeyword(val) {
      keyword.value = val;
      onSearch(val);
    }

    onBeforeMount(() => {
      keyword.value = route.params.keyword;
      onSearch(keyword.value);
    });

    return {
      tabOptions,
      isLoading,
      tab,
      followList,
      keyword,
      people,
      postListArr,
      onUpdateKeyword,
      onSearch,
      onUpdatelike,
      onDeletePost,
    };
  },
};
</script>

<style lang="scss">
.search-result-page {
  > .page-container {
    max-width: 600px;
    padding: 0 0 20px;
    border-right: 1px solid rgb(239, 243, 244);
    .search-result-card-container {
      .no-data {
        width: 330px;
        margin: 0 auto;
        padding: 30px 0;
        white-space: pre-line;
        word-break: keep-all;
        .title {
          font-size: 31px;
          font-weight: 800;
          margin-bottom: 10px;
          line-height: 34px;
        }
      }
    }
  }
}
</style>
