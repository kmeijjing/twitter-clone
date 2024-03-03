<template>
  <q-page class="profile-page flex no-wrap">
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

        <div>
          <div class="title">{{ user.name }}</div>
          <div class="subtitle" style="font-size: 13px">{{ user.posts.length || 0}} Post</div>
        </div>
      </div>

      <ProfileInfoCard
        :user="user"
        :follows="follows"
        @update:user="getUser"
      />

      <div class="tabs-container">
        <q-tabs
          v-model="tab"
          dense
          class="text-grey"
          active-color="primary"
          indicator-color="primary"
          align="justify"
          narrow-indicator
        >
          <q-tab
            v-for="(t, i) in tabOptions"
            no-caps
            :key="i"
            :name="t.name"
            :value="t.value"
            :label="t.name"
            :ripple="false"
          />
        </q-tabs>
        <q-separator />

        <q-tab-panels
          v-model="tab"
          animated
          class="full-width"
        >
          <q-tab-panel name="Posts">
            <PostTabContent />
          </q-tab-panel>
        </q-tab-panels>
      </div>
    </div>

    <RightSideBar :isRandomFollowList="false" />
  </q-page>
</template>

<script>
import { ref, onBeforeMount } from "vue";
import { Dialog, Cookies } from "quasar";
import { api } from "@boot/axios";
import { tabOptions } from "@constants/profile.js";
import ProfileInfoCard from "src/components/profile/ProfileInfoCard.vue";
import RightSideBar from "@layouts/RightSideBar.vue";
import PostTabContent from '@components/profile/PostTabContent.vue';

export default {
  name: 'ProfilePage',
  components: { ProfileInfoCard, PostTabContent, RightSideBar },
  setup() {
    const myId = Cookies.get('user').id;
    const tab = ref('Posts');

    const user = ref({
      posts: [],
    });
    const follows = ref({
      followings: [],
      followers: [],
    });
    function getUser() {
      api
        .get(`/user/${myId}`)
        .then((res) => {
          user.value = res.data;
        })
        .catch((err) => {
          console.log(err);
        });
    }

    function getFollow() {
      api
        .get(`/follow/${myId}`)
        .then((res) => {
          follows.value.followings = res.data.followings;
          follows.value.followers = res.data.followings;
        })
        .catch((err) => {
          console.log(err);
        });
    }

    onBeforeMount(() => {
      getUser();
      getFollow();
    });

    return {
      tabOptions,

      myId,
      tab,
      user,
      follows,
      getUser,
    };
  },
};
</script>

<style lang="scss">
.profile-page {
  .page-container {
    max-width: 600px;
    padding: 0 0 20px;
    border-right: 1px solid rgb(239, 243, 244);
    .profile-card {
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
    .tabs-container {
      .q-tabs {
        height: 40px;
      }
      .q-tab-panels {
        .q-panel {
          .q-tab-panel {
            padding: 0;
          }
        }
      }
    }
  }
}
</style>
