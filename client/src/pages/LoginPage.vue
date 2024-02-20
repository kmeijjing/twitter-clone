<template>
  <q-layout>
    <q-page-container>
      <q-page class="flex flex-center q-mx-auto login-page">
        <q-card flat dense class="flex flex-center">
          <q-card-section class="text-center">
            <img
              alt="Miniter logo"
              src="~assets/miniter-logo.svg"
              style="width: 100px; height: 100px"
            />
            <div class="text-h6 text-weight-bold">
              지금 세계에서 무슨 일이 일어나고<br />
              있는지 알아보세요.
            </div>
          </q-card-section>

          <LoginForm />

          <div class="sign-up-content flex justify-center q-mt-sm">
            <div class="text-grey-8 q-mr-xs">
              Don't have an account?
            </div>
            <div class="text-grey-9" style="text-decoration: underline;">
              <router-link to="/signup">Sign up</router-link>
            </div>
          </div>
        </q-card>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script>
import LoginForm from "@components/LoginForm.vue";

export default {
  name: "LoginPage",
  components: { LoginForm },
  setup() {
    return {
    };
  },
};
</script>

<style lang="scss">
.login-page {
  max-width: 400px;
  .q-card {
    padding: 20px;
  }
}
</style>
