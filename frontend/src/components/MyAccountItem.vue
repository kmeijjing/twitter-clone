<template>
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
</template>

<script>
import { Cookies } from "quasar";
import { useRouter } from "vue-router";

export default {
  name: 'MyAccountItem',
  setup() {
    const router = useRouter();

    function logout() {
      Cookies.remove('access_token');
      Cookies.remove('user');
      router.push({ name: 'SignIn' });
    }
    return {
      logout,
    }
  },
}
</script>

<style lang="scss" scoped>
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

.my-account-menu {
  .q-list {
    padding: 12px 0;
    width: 200px;
    .q-item {
      min-height: 0;
      &__section {
        font-weight: bold;
      }
    }
  }
}

@media screen and (max-width: 1190px) {
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
</style>
