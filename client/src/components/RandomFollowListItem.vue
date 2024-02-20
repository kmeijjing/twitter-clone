<template>
  <q-item clickable class="random-follow-list-item">
    <q-avatar class="bg-deep-purple-2">
      <q-img v-if="profile_image" :src="`profileImgs/${id}/${profile_image}`" />
      <q-icon v-else name="person" color="indigo-4" size="30px" />
    </q-avatar>
    <q-item-section class="info">
      <div class="text-bold">{{ name }}</div>
      <div class="text-grey-7">{{ email }}</div>
      <div v-if="bioShow" class="bio">{{ bio }}</div>
    </q-item-section>
    <q-btn
      v-if="!following"
      dense
      rounded
      no-caps
      unelevated
      label="Follow"
      color="black"
      @click="clickFollow"
    />
    <q-btn
      v-else
      outline
      dense
      rounded
      no-caps
      unelevated
      :label="unfollowBtn ? 'Unfollow' : 'Following'"
      :color="unfollowBtn ? 'red-7' : 'grey-5'"
      @click="clickUnfollow"
      @mouseenter="unfollowBtn = true"
      @mouseleave="unfollowBtn = false"
      class="following-btn bg-white"
      :class="{ 'following-btn-text': !unfollowBtn }"
    />
  </q-item>
</template>

<script>
import { ref } from "vue";
import { Dialog, Cookies } from "quasar";
import ConfirmDialog from "@components/common/ConfirmDialog.vue";

export default {
  name: "RandomFollowListItem",
  props: {
    id: {
      type: Number,
      default: null,
    },
    name: {
      type: String,
      default: "",
    },
    email: {
      type: String,
      default: "",
    },
    bio: {
      type: String,
      default: "",
    },
    bioShow: {
      type: Boolean,
      default: true,
    },
    profile_image: {
      type: String,
      default: '',
    }
  },
  setup(props) {
    const user = Cookies.get('user');
    const following = ref(false);
    const unfollowBtn = ref(false);

    function clickFollow() {
    }

    function clickUnfollow() {
      Dialog.create({
        component: ConfirmDialog,
        componentProps: {
          title: `Unfollow @${props.name}?`,
          desc: "Their Tweets will no longer show up in your home timeline. You can still view their profile, unless their Tweets are protected.",
          firstBtnLabel: 'Unfollow',
          firstBtnColor: 'black',
          secondBtnLabel: 'Cancel',
        },
      }).onOk(() => {
      });
    }

    return {
      following,
      unfollowBtn,
      clickFollow,
      clickUnfollow,
    };
  },
};
</script>

<style lang="scss" scope>
.random-follow-list-item {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 16px;
  &:hover {
    background: $indigo-1;
  }
  .info {
    width: 100%;
    margin: 0 12px;
    > div {
      width: 100%;
      word-break: keep-all;
      white-space: nowrap;
      text-overflow: ellipsis;
      overflow: hidden;
    }
    > div:nth-of-type(2) {
      font-size: 13px;
      line-height: 13px;
    }
    .bio {
      margin-top: 5px;
    }
  }
  .q-btn {
    padding: 0 20px;
  }
  .following-btn {
    width: 102px;
  }
  .following-btn-text {
    .q-btn__content {
      .block {
        color: black;
      }
    }
  }
}
</style>
