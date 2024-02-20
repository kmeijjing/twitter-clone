<template>
  <q-drawer
    v-model="drawer"
    show-if-above
    side="left"
    bordered
    :mini="$q.screen.width <= 1190"
    :width="240"
    :breakpoint="500"
    :class="$q.dark.isActive ? 'bg-grey-9' : 'bg-white'"
    class="left-drawer"
  >
    <q-scroll-area class="fit" :horizontal-thumb-style="{ opacity: 0 }">
      <q-list padding>
        <EssentialLink
          v-for="link in linksList"
          :key="link.title"
          :title="link.title"
          :icon="link.icon"
          :link="link.link"
        />

        <q-btn
          rounded
          unelevated
          no-caps
          label="Post"
          color="primary"
          class="add-post-btn"
          style="width: 200px"
          @click="openAddPostDialog"
        />

        <q-item clickable class="my-account-item absolute-bottom">
          <q-menu class="my-account-menu">
            <q-list>
              <q-item clickable>
                <q-item-section>다른 계정으로 로그인</q-item-section>
              </q-item>
              <q-item clickable @click="logout">
                <q-item-section>@meijing 로그아웃</q-item-section>
              </q-item>
            </q-list>
          </q-menu>

          <q-item-section avatar class="avatar-section">
            <q-avatar color="grey-6" text-color="white" icon="face" size="44px" />
          </q-item-section>

          <q-item-section class="profile-section">
            <div class="text-weight-bold">MK Kim</div>
            <div class="text-grey-8">@meijing</div>
          </q-item-section>

          <q-item-section side class="more-icon-section">
            <q-icon name="more_horiz" />
          </q-item-section>
        </q-item>
      </q-list>
    </q-scroll-area>
  </q-drawer>
</template>

<script>
import { defineComponent, ref } from 'vue'
import EssentialLink from "@components/EssentialLink.vue";
import AddPostDialog from "@components/AddPostDialog.vue";
import { linksList } from "@constants/menu.js"
import { Dialog, Cookies } from "quasar";
import { useRouter } from "vue-router";

export default defineComponent({
  name: "LeftSideMenu",
  components: {
    EssentialLink,
  },
  setup() {
    const router = useRouter();

    function logout() {
      Cookies.remove('access_token');
      Cookies.remove('user');
      router.push("/");
    }

    function openAddPostDialog() {
      Dialog.create({
        component: AddPostDialog,
        persistent: false,
      }).onOk(() => {
        router.push("/");
      });
    }

    return {
      drawer: ref(false),
      miniState: ref(true),
      linksList,
      logout,
      openAddPostDialog,
    }
  },
})
</script>

<style lang="scss">
.q-drawer {
  position: fixed;
  height: 100vh !important;
  .q-scrollarea {
    .q-scrollarea__container {
      .q-scrollarea__content {
        .q-list {
          padding: 58px 4px 0;
          display: grid;
          gap: 4px;
          .add-post-btn {
            height: 48px;
            .q-btn__content {
              font-size: 16px;
            }
          }
        }
      }
    }
  }
  .my-account-item {
    padding: 10px 16px;
    border-radius: 33px;
    left: 4px;
    right: 4px;
    bottom: 8px;
    width: calc(100% - 8px);
    .q-item__section {
      padding: 0;
    }
    .profile-section {
      margin: 0 4px;
    }
  }
}

.my-account-menu {
  width: 200px;
  .q-list {
    padding: 12px 0;
    .q-item {
      min-height: 0;
      &__section {
        font-weight: bold;
      }
    }
  }
}

@media screen and (max-width: 1190px) {
  .q-drawer {
    width: 70px;
    min-width: 70px;
    .q-scrollarea {
      .q-scrollarea__container {
        .q-scrollarea__content {
          .q-list {
            justify-content: center;
            .gnb-item {
              width: 48px;
              padding: 0;
              display: flex;
              align-items: center;
              justify-content: center;
              > .q-item__section--side {
                padding-right: 0;
              }
              > .q-item__section--main {
                display: none;
              }

            }
            .add-post-btn {
              width: 48px !important;
              .q-btn__content {
                font-size: 16px;
              }
            }
            .my-account-item {
              padding: 0;
              width: 44px;
              left: 50%;
              transform: translateX(-50%);
              .profile-section, .more-icon-section {
                display: none !important;
              }
              .avatar-section {
                width: 44px;
                min-width: 0;
              }
              .q-itme__section{
                padding: 0 !important;
              }
            }
          }
        }
      }
    }
  }
}
</style>
