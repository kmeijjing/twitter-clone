<template>
  <q-card class="profile-info-card" flat square>
    <q-card-section class="bg-photo-section bg-grey-4" style="height: 200px">
      <q-img
        v-if="user.bg_image"
        :src="`bgImgs/${myId}/${user.bg_image}`"
        style="height: 200px"
      />
    </q-card-section>

    <q-card-section class="profile-info-section">
      <div class="flex justify-end">
        <div class="profile-img">
          <q-avatar class="bg-grey-4" size="145px">
            <img v-if="user.profile_image" :src="`profileImgs/${myId}/${user.profile_image}`" />
            <q-icon name="person" color="grey-6" size="90px" />
          </q-avatar>
        </div>

        <div style="height: 36px;">
          <q-btn
            v-if="user.id === myId"
            outline
            rounded
            no-caps
            label="Edit Profile"
            color="dark"
            size="md"
            class="edit-btn"
            :ripple="false"
            @click="editProfileDialog"
          />
        </div>

        <!-- <div>
          <q-btn
            v-if="!following"
            dense
            rounded
            no-caps
            unelevated
            label="Follow"
            color="black"
            @click.stop="clickFollow"
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
            @click.stop="clickUnfollow"
            @mouseenter="unfollowBtn = true"
            @mouseleave="unfollowBtn = false"
            class="following-btn bg-white"
            :class="{ 'following-btn-text': !unfollowBtn }"
          />
        </div> -->
      </div>
      <div style="margin-top: 24px">
        <div class="text-bold name">{{ user.name }}</div>
        <div class="email q-pb-sm">{{ user.email }}</div>
        <div class="bio q-mt-sm">{{ user.bio }}</div>
        <div class="created flex row items-center q-my-sm">
          <q-icon name="calendar_month" />
          <span>Joined {{ user.created_at }}</span>
        </div>
        <div class="follow">
          <span class="q-mr-md">
            <strong class="q-pr-xs">{{ follows.followings.length }}</strong>
            <span class="text-grey-8">Following</span>
          </span>
          <span>
            <strong class="q-pr-xs">{{ follows.followers.length }} </strong>
            <span class="text-grey-8">Followers</span>
          </span>
        </div>
      </div>
    </q-card-section>
  </q-card>
</template>

<script>
import { Dialog, Cookies } from "quasar";
import EditProfileDialog from "@components/profile/EditProfileDialog.vue";

export default {
  name: 'ProfileInfoCard',
  props: {
    user: {
      type: Object,
      default: () => {},
      required: true,
    },
    follows: {
      type: Object,
      default: () => {},
      required: true,
    },
  },
  setup(props, { emit }) {
    const myId = Cookies.get('user').id;

    function editProfileDialog() {
      Dialog.create({
        component: EditProfileDialog,
        componentProps: {
          user: props.user,
        },
        persistent: true,
      }).onOk(() => {
        emit('update:user');
      });
    }
    return {
      myId,
      editProfileDialog,
    }
  },
}
</script>

<style lang="scss">
.profile-info-card {
  .profile-info-section {
    padding: 12px 16px;
    .profile-img {
      position: absolute;
      top: -80px;
      left: 12px;
      .q-avatar {
        &__content {
          border: 3px solid white;
        }
        img {
          object-fit: cover;
        }
      }
    }
    .edit-btn {
      height: 34px;
      &:before {
        border: 1px solid $grey-4;
      }
      .q-btn__content {
        font-size: 15px;
        font-weight: 700;
      }
    }
    .name {
      font-size: 20px;
    }
    .email {
      font-size: 15px;
      color: $grey-7;
      line-height: 16px;
    }
    .created {
      color: $grey-7;
      > .q-icon {
        margin-right: 4px;
      }
    }
    .follow {
      > span {
        cursor: pointer;
        &:hover {
          border-bottom: 1px solid black;
        }
      }
    }
  }
}
</style>
