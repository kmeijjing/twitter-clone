<template>
  <q-item
    clickable
    class="post-card flex items-start justify-between"
    @click.stop="router.push(`/post/${id}`)"
  >
    <q-item-section avatar>
      <q-avatar class="bg-grey-4" size="44px">
        <q-icon v-if="!profile_image" round color="grey-6" size="30px" name="person" @click.stop="goProfile" />
        <q-img v-else :src="`profileImgs/${user_id}/${profile_image}`" @click.stop="goProfile" />
      </q-avatar>
    </q-item-section>

    <q-item-section class="flex column no-wrap">
      <div class="account-section flex row items-center justify-between">
        <div class="user-container flex row">
          <span class="title q-mr-xs" @click.stop="goProfile">{{ name }}</span>
          <span class="desc">{{ email }} ∙ {{ created }}</span>
        </div>
        <PostMenuButton
          :post_user_id="user_id"
          @delete:post="$emit('delete:post')"
        />
      </div>
      <div class="content-container">
        <div class="tweet">{{ tweet }}</div>
        <div v-if="!!uploads" class="imgs" :class="`imgs-${uploads.length}`">
          <q-img
            v-for="(upload, i) in uploads"
            :key="i"
            :src="`uploads/${upload}`"
            :class="`img-${i}`"
            @click.stop="tweetImgsDialog(i)"
          />
        </div>
      </div>

      <div class="function-container flex items-center justify-between">
        <q-btn flat dense round :ripple="false" color="grey-8" icon="far fa-comment-alt" class="reply-btn" :label="Number(10).toLocaleString()" />

        <q-btn flat dense round :ripple="false" color="grey-8" icon="fas fa-retweet" class="repost-btn" :label="Number(10).toLocaleString()" />

        <q-btn
          flat
          dense
          round
          :ripple="false"
          :color="like ? 'pink' : 'grey-8'"
          :icon="like ? roundFavorite : roundFavoriteBorder"
          class="like-btn"
          :label="Number(like_count).toLocaleString()"
          @click.stop="onClickLike"
        />

        <q-btn flat dense round :ripple="false" color="grey-8" icon="far fa-share-square" class="share-btn" />
      </div>
    </q-item-section>
  </q-item>
</template>

<script>
import { watch } from 'vue';
import { Dialog, Cookies, useQuasar } from "quasar";
import { useRouter } from "vue-router";
import { api } from "@boot/axios";
import {
  roundComment,
  roundCached,
  roundFavoriteBorder,
  roundFavorite,
  roundIosShare,
} from "@quasar/extras/material-icons-round";
import { tweetFunctionButtons } from '@constants/tweet.js';
import TweetImgsDialog from '@components/common/TweetImgsDialog.vue';
import PostMenuButton from '@components/common/PostMenuButton.vue';

const buttons = [
  { title: "Reply", label: 10, icon: roundComment, color: "primary" },
  { title: "Repost", label: 1200, icon: roundCached, color: "cyan-7" },
  { title: "Like", label: 3200, icon: roundFavoriteBorder, color: "pink-12" },
  { title: "Share", label: 0, icon: roundIosShare, color: "blue-6" },
];

export default {
  name: "PostCard",
  components: { PostMenuButton },
  props: {
    idx: Number,
    id: {
      type: Number,
      default: null,
    },
    user_id: {
      type: Number,
      default: null,
      required: true,
    },
    name: {
      type: String,
      default: "",
    },
    email: {
      type: String,
      default: "",
    },
    profile_image: {
      type: String,
      default: "",
    },
    created: {
      type: String,
      default: "",
    },
    tweet: {
      type: String,
      default: "",
    },
    like: {
      type: Boolean,
      default: false,
      required: true,
    },
    like_count: {
      type: Number,
      default: 0,
      required: true,
    },
    uploads: {
      type: [Array, String],
      default: null,
    },
  },
  setup(props, { emit }) {
    const router = useRouter();
    const user = Cookies.get('user');

    function goProfile() {
      if (props.user_id === user.id) {
        router.push("/profile");
      } else {
        router.push(`/user?u=${props.user_id}`);
      }
    }

    function onClickLike() {
      const param = {
        user_id: user.id,
        tweet_id: props.id,
      };
      api
        .post("/like", param)
        .then(() => {
          emit("update:like");
        })
        .catch((err) => {
          console.log(err.message);
        });
    }

    const $q = useQuasar();
    function tweetImgsDialog(idx) {
      const dialog = $q.dialog({
        component: TweetImgsDialog,
        componentProps: {
          uploads: props.uploads,
          idx: idx,
          post_id: props.id,
          like: props.like,
          like_count: props.like_count,
          updateLike: () => {
            emit("update:like")
          }
        },
      });
      watch(() => props.like, () => {
        dialog.update({
          like: props.like,
          like_count: props.like_count,
        });
      })
    }

    return {
      roundComment,
      roundCached,
      roundFavoriteBorder,
      roundFavorite,
      roundIosShare,

      router,
      user,
      buttons,
      goProfile,
      onClickLike,
      tweetImgsDialog,

      tweetFunctionButtons,
    };
  },
};
</script>

<style lang="scss">
.post-card {
  padding: 12px 16px 16px;
  border-bottom: 1px solid rgb(239, 243, 244);
  position: relative;
  > .q-item__section {
    &.q-item__section--avatar {
      padding-right: 12px;
    }
    .user-container {
      .title {
        font-weight: bold;
        &:hover {
          cursor: pointer;
          text-decoration: underline;
        }
      }
      .desc {
        color: $grey-8;
      }
    }
    .content-container {
      .tweet {
        font-size: 16px;
      }
      .imgs {
        border: 1px solid $grey-3;
        border-radius: 16px;
        overflow: hidden;
        margin-top: 12px;
        &.imgs-2 {
          display: flex;
          gap: 1px;
        }
        &.imgs-3 {
          display: grid;
          gap: 1px;
          .img-0 {
            grid-column: 1 / 2;
            grid-row: 1 / 3;
          }
          .img-1 {
            grid-column: 2 / 3;
            grid-row: 1 / 2;
          }
          .img-2 {
            grid-column: 2 / 3;
            grid-row: 2 / 3;
          }
        }
        &.imgs-4 {
          display: grid;
          gap: 1px;
          .img-0 {
            grid-column: 1 / 2;
            grid-row: 1 / 2;
          }
          .img-1 {
            grid-column: 2 / 3;
            grid-row: 1 / 2;
          }
          .img-2 {
            grid-column: 1 / 2;
            grid-row: 2 / 3;
          }
          .img-3 {
            grid-column: 2 / 3;
            grid-row: 2 / 3;
          }
        }
      }
    }
    .function-container {
      width: 100%;
      margin-top: 14px;
      .q-btn {
        &__content {
          .q-icon {
            font-size: 15px;
          }
          .block {
            font-size: 13px;
          }
        }
        .q-focus-helper {
          opacity: 0 !important;
        }
        &:hover {
          .q-icon {
            &:after {
               content: '';
               width: 40px;
               height: 40px;
               position: absolute;
               top: 50%;
               left: 50%;
               transform: translate(-50%, -50%);
               border-radius: 20px;
            }
          }
        }
      }
      .reply-btn, .share-btn {
        &:hover {
          .q-icon {
            color: $primary;
            &:after {
               background: rgba(3, 169, 244, 0.18);
            }
          }
          .block {
            color: $primary;
          }
        }
      }
      .repost-btn {
        &:hover {
          .q-icon {
            color: $green;
            &:after {
               background: rgba(76, 175, 80, 0.18);
            }
          }
          .block {
            color: $green;
          }
        }
      }
      .like-btn {
        &:hover {
          .q-icon {
            color: $pink;
            &:after {
               background: rgba(233, 30, 99, 0.18);
            }
          }
          .block {
            color: $pink;
          }
        }
      }
    }
  }
}
</style>
