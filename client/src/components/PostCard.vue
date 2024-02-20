<template>
  <q-item
    clickable
    class="post-card flex items-start justify-between"
    @click.stop="router.push(`/tweet?id=${id}`)"
  >
    <q-btn flat dense round :ripple="false" icon="more_horiz" size="sm" color="grey-8" class="more-btn" @click.stop>
      <q-menu class="btn-menu">
        <q-list>
          <q-item clickable @click="deleteTweet">
            <q-item-section class="text-negative">Delete</q-item-section>
          </q-item>
        </q-list>
      </q-menu>
    </q-btn>

    <q-item-section avatar>
      <q-avatar class="bg-grey-4" size="44px">
        <q-img v-if="profile_image" :src="`profileImgs/${user_id}/${profile_image}`" @click.stop="goProfile" />
        <q-icon v-else round color="grey-6" size="30px" name="person" @click.stop="goProfile" />
      </q-avatar>
    </q-item-section>

    <q-item-section class="flex column no-wrap">
      <div class="user-container flex row">
        <span class="title q-mr-xs" @click.stop="goProfile">{{ name }}</span>
        <span class="desc">@{{ account_id }} ∙ {{ created }}</span>
      </div>
      <div class="content-container">
        <div class="tweet">{{ tweet }}</div>
        <q-img
          v-for="(upload, i) in uploads"
          :key="i"
          :src="`uploads/${upload}`"
          @click.stop="tweetImgsDialog(i)"
        />
      </div>

      <div class="function-container flex items-center justify-between">
        <q-btn flat dense round :ripple="false" size="sm" color="grey-8" icon="far fa-comment-alt" class="reply-btn" :label="Number(10).toLocaleString()" />

        <q-btn flat dense round :ripple="false" size="sm" color="grey-8" icon="fas fa-retweet" class="repost-btn" :label="Number(10).toLocaleString()" />

        <q-btn flat dense round :ripple="false" size="sm" color="grey-8" icon="far fa-heart" class="like-btn" :label="Number(10).toLocaleString()" />

        <q-btn flat dense round :ripple="false" size="sm" color="grey-8" icon="far fa-share-square" class="like-btn" />
      </div>
    </q-item-section>
  </q-item>
</template>

<script>
import { Dialog, Cookies } from "quasar";
import { useRouter } from "vue-router";
import {
  roundComment,
  roundCached,
  roundFavoriteBorder,
  roundFavorite,
  roundIosShare,
} from "@quasar/extras/material-icons-round";
import { tweetFunctionButtons } from '@constants/tweet.js';
import ConfirmDialog from '@components/common/ConfirmDialog.vue';
import TweetImgsDialog from '@components/common/TweetImgsDialog.vue';

const buttons = [
  { title: "Reply", label: 10, icon: roundComment, color: "primary" },
  { title: "Repost", label: 1200, icon: roundCached, color: "cyan-7" },
  { title: "Like", label: 3200, icon: roundFavoriteBorder, color: "pink-12" },
  { title: "Share", label: 0, icon: roundIosShare, color: "blue-6" },
];

export default {
  name: "PostCard",

  props: {
    idx: Number,
    id: {
      type: Number,
      default: null,
    },
    user_id: {
      type: Number,
      default: null,
    },
    name: {
      type: String,
      default: "",
    },
    account_id: {
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
    },
    like_count: {
      type: Number,
      default: 0,
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

    function clickLike() {
    }

    function tweetImgsDialog(idx) {
      Dialog.create({
        component: TweetImgsDialog,
        componentProps: {
          uploads: props.uploads,
          idx: idx,
          id: props.id,
          like: props.like,
          like_count: props.like_count
        },
      });
    }

    function deleteTweet() {
      Dialog.create({
        component: ConfirmDialog,
        componentProps: {
          title: 'Delete tweet?',
          desc: 'This can’t be undone and it will be removed from your profile, the timeline of any accounts that follow you, and from Twitter search results.',
          firstBtnLabel: 'Delete',
          firstBtnColor: 'negative',
          secondBtnLabel: 'Cancel'
        }
      }).onOk(() => {
        emit("delete");
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
      clickLike,
      tweetImgsDialog,
      deleteTweet,

      tweetFunctionButtons,
    };
  },
};
</script>

<style lang="scss">
.post-card {
  padding: 20px 16px 16px;
  border-bottom: 1px solid $indigo-1;
  position: relative;
  > .more-btn {
    position: absolute;
    top: 14px;
    right: 16px;
  }
  > .q-item__section {
    &.q-item__section--avatar {
      padding-right: 12px;
    }
    > .user-container {
      .title {
        font-weight: bold;
        &:hover {
          cursor: pointer;
          text-decoration: underline;
        }
      }
      .desc {
        color: $grey-7;
      }
    }
    .content-container {
      .tweet {
        font-size: 16px;
      }
      .q-img {
        width: calc(50% - 3px);
        margin-right: 6px;
        margin-bottom: 6px;
        border-radius: 12px;
        border: 1px solid $indigo-1;
        &:nth-of-type(1),
        &:nth-of-type(3) {
          margin-right: 0;
        }
      }
    }
    .function-container {
      width: 100%;
      margin-top: 14px;
      > div {
        margin-right: 24px;
        &:last-of-type {
          margin-right: 0;
        }
        .q-btn {
          &__content {
            .q-icon {
              font-size: 18px;
            }
          }
        }
      }
      .like:hover {
        > span {
          color: $pink-12 !important;
        }
      }
    }
  }
}
</style>
