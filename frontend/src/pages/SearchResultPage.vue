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
        <q-card-section v-if="!postListArr.length" class="no-data">
          <div>
            <div class="title">No results for<br />"{{ keyword }}"</div>
            <div class="desc">
              Try searching for something else, or check your Search settings to see if they’re protecting you from potentially sensitive content.
            </div>
          </div>
        </q-card-section>

        <q-list v-else>
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
        <q-card-section>
          <div>People</div>
          <!-- <follow-component
            v-for="(p, i) in people"
            :key="p.id"
            :idx="i"
            :id="p.id"
            :name="p.name"
            :email="p.email"
            :bio="p.bio"
            :profile_image="p.profile_image"
            :following="p.following"
            @updateFollow="updateFollow(i)"
          /> -->
        </q-card-section>
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
// import FollowComponent from "@components/FollowComponent.vue";
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
    const route = useRoute();
    const user = Cookies.get('user');
    console.log(user)
    const tab = ref("Top");

    const followList = ref([]);
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
          Loading.hide();
        });
    }

    const keyword = ref("");
    const people = ref([]);

    const postListArr = ref([]);
    function onSearch(val) {
      if (val) {
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

    function updateFollow(idx) {
      people.value[idx].following = !people.value[idx].following;
    }

    onBeforeMount(() => {
      keyword.value = route.params.keyword;
      onSearch(keyword.value);
    });

    return {
      tabOptions,

      tab,
      followList,
      keyword,
      people,
      postListArr,
      onUpdateKeyword,
      onSearch,
      onUpdatelike,
      onDeletePost,
      updateFollow,
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
      // .no-data {
      //   width: 275px;
      //   margin: 0 auto;
      //   padding: 30px 0;
      //   white-space: pre-line;
      //   word-break: keep-all;
      //   .title {
      //     font-size: 26px;
      //     margin-bottom: 10px;
      //     line-height: 34px;
      //   }
      // }
    }
  }
}
</style>
