<template>
  <q-page class="post-detail-page">
    <div class="page-header flex row items-center">
      <q-btn
        flat
        dense
        round
        :ripple="false"
        icon="arrow_back"
        size="md"
        class="q-mr-sm"
        @click="router.go(-1)"
      />
      <strong>Post</strong>
    </div>

    <PostCard
      :id="tweet.id"
      :account_id="tweet.account_id"
      :name="tweet.name"
      :email="tweet.email"
      :profile_image="tweet.profile_image"
      :created="tweet.created_at"
      :tweet="tweet.tweet"
      :like="tweet.like"
      :like_count="tweet.like_count"
      :uploads="tweet.uploads"
    />

    <q-card class="reply-card" flat>
      <q-card-section class="reply-container">
        <div class="replying-to">
          <span class="text-grey-8 q-mr-xs">Replying to</span>
          <span class="text-primary">@jungshasa</span>
        </div>

        <div class="reply-form flex no-wrap">
          <q-avatar class="bg-grey-4" size="44px">
            <q-img v-if="profile_image" :src="`profileImgs/${user_id}/${profile_image}`" @click.stop="goProfile" />
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
  </q-page>
</template>

<script>
import PostCard from "src/components/PostCard.vue";
import { ref, onBeforeMount } from "vue";
import { Dialog, Cookies } from "quasar";
import { api } from "@boot/axios";
import { useRoute, useRouter } from "vue-router";
import { tweetReplyFunctionButtons } from '@constants/tweet.js';
import {
  roundComment,
  roundCached,
  roundFavoriteBorder,
  roundFavorite,
  roundIosShare,
} from "@quasar/extras/material-icons-round";

export default {
  name: "PostDetailPage",
  components: { PostCard },
  setup() {
    const route = useRoute();
    const router = useRouter();
    const user = Cookies.get('user');

    const replyVal = ref("");

    const tweet = ref({
      id: null,
      user_id: null,
      tweet: "",
      created_at: "",
      like_count: null,
      like: null,
      name: "",
      email: "",
      account_id: '',
      uploads:null,
    });

    function getTweet(val) {
      tweet.value = {
        id: 1,
        user_id: 1,
        tweet: "afdasfdsadfadfasdfsdaf",
        created_at: "2024-02-01",
        like_count: 1,
        like: false,
        name: "meijing",
        email: "a@a.com",
        account_id: 'kkk',
        uploads:null,
      }
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

    function clickLike() {
    }

    onBeforeMount(() => {
      getTweet(route.query.id);
    });

    return {
      tweetReplyFunctionButtons,
      roundComment,
      roundCached,
      roundFavoriteBorder,
      roundFavorite,
      roundIosShare,

      router,

      isFocusInput: ref(false),
      replyVal,
      addReply,
      tweet,
      goProfile,
      clickLike,
    };
  },
};
</script>

<style lang="scss">
.post-detail-page {
  padding: 0 0 20px;
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
</style>
