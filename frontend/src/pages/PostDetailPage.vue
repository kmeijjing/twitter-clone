<template>
  <q-page class="post-detail-page flex row no-wrap">
    <div class="page-container full-width">
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
        <div class="title">Post</div>
      </div>

      <PostCard
        :id="post.id"
        :user_id="post.user_id"
        :name="post.name"
        :email="post.email"
        :profile_image="post.profile_image"
        :created="post.created_at"
        :tweet="post.content"
        :like="post.like"
        :like_count="post.like_count"
        :uploads="post.uploads"
        :isClickable="false"
        @update:like="onUpdateLike"
      />

      <q-card class="reply-card" flat>
        <q-card-section class="reply-container">
          <div class="replying-to">
            <span class="text-grey-8 q-mr-xs">Replying to</span>
            <span class="text-primary">@jungshasa</span>
          </div>

          <div class="reply-form flex no-wrap">
            <q-avatar class="bg-grey-4" size="44px">
              <q-img v-if="post.profile_image" :src="`profileImgs/${user_id}/${post.profile_image}`" @click.stop="goProfile" />
              <q-icon v-else round color="grey-6" size="30px" name="person" @click.stop="goProfile" />
            </q-avatar>

            <q-form class="full-width" :class="{ 'origin-form': !isFocusInput }" @submit="addReply(replyVal)">
              <q-input
                type="text"
                v-model="replyVal"
                placeholder="Post your reply"
                borderless
                dense
                autogrow
                @focus="isFocusInput = true"
              />
              <div class="flex no-wrap items-center justify-between">
                <div class="function-btns flex no-wrap">
                  <q-btn
                    v-for="btn in tweetReplyFunctionButtons"
                    :key="btn.label"
                    flat
                    dense
                    round
                    color="primary"
                    :icon="btn.icon"
                  />
                </div>
                <q-btn
                  type="submit"
                  rounded
                  color="primary"
                  label="Reply"
                  unelevated
                  no-caps
                  :disable="!replyVal"
                />
              </div>
            </q-form>
          </div>
        </q-card-section>
      </q-card>
    </div>

    <RightSideBar :isRandomFollowList="false" />

  </q-page>
</template>

<script>
import PostCard from "src/components/PostCard.vue";
import { ref, onBeforeMount } from "vue";
import { Cookies } from "quasar";
import { api } from "@boot/axios";
import { useRoute, useRouter } from "vue-router";
import { tweetReplyFunctionButtons } from '@constants/tweet.js';
import RightSideBar from "src/layouts/RightSideBar.vue";

export default {
  name: "PostDetailPage",
  components: { PostCard, RightSideBar },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const user = Cookies.get('user');

    const replyVal = ref("");

    const post = ref({
      id: null,
      content: '',
      created_at: '',
      like_count: 0,
      like: false,
      name: '',
      email: '',
      account_id: '',
      profile_image: null,
      uploads:null,
    });

    function getPost(val) {
      api
        .get(`/tweet/${val}/${user.id}`)
        .then((res) => {
          post.value = res.data;
          if(post.value.uploads) {
            post.value.uploads = post.value.uploads.split(" ");
            post.value.uploads.pop();
          }
        })
        .catch((err) => {
          console.log(err);
      });
    }

    function addReply(val) {
      console.log(val);
    }

    function goProfile(id) {
      if (id === user.id) {
        router.push("/profile");
      } else {
        router.push(`/user?u=${id}`);
      }
    }

    function onUpdateLike() {
      if (post.value.like === true) {
        post.value.like_count -= 1;
      } else {
        post.value.like_count += 1;
      }
      post.value.like = !post.value.like;
    }

    onBeforeMount(() => {
      getPost(route.params.id);
    });

    return {
      tweetReplyFunctionButtons,

      isFocusInput: ref(false),
      replyVal,
      addReply,
      post,
      goProfile,
      onUpdateLike,
    };
  },
};
</script>

<style lang="scss">
.post-detail-page {
  > .page-container {
    max-width: 600px;
    padding: 0 0 20px;
    border-right: 1px solid rgb(239, 243, 244);
    .reply-card {
      padding: 24px 16px;
      > .reply-container {
        .replying-to {
          margin-left: 58px;
        }
        .reply-form {
          .q-avatar {
            margin-right: 12px;
          }
          .origin-form {
            display: flex;
            flex-flow: row nowrap;
            align-items: center;
            justify-content: space-between;
            > div {
              margin-top: 0px !important;
              .function-btns {
                display: none;
              }
            }
          }
          .q-form {
            .q-field {
              width: calc(100% - 90px);
              &__inner {
                .q-field__control {
                  &-container {
                    .q-field__native {
                      font-size: 20px;
                      line-height: 24px;
                      &::placeholder {
                        color: $grey-7;
                      }
                    }
                  }
                }
              }
            }
            > div {
              margin-top: 8px;
              .function-btns {
                margin-left: -6px;
                gap: 4px;
              }
            }
          }
        }
      }
    }
  }
}
</style>
