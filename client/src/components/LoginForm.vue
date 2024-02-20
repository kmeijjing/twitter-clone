<template>
  <q-form class="login-form full-width q-gutter-y-md" @submit="login">
    <q-input
      type="text"
      v-model="loginInfo.email"
      rounded
      outlined
      placeholder="Your Email"
      autofocus
    />
    <q-input
      type="password"
      v-model="loginInfo.password"
      rounded
      outlined
      placeholder="Your Password"
    />
    <q-btn
      type="submit"
      rounded
      color="black"
      label="Sign In"
      :disable="!loginInfo.email || !loginInfo.password"
      class="button full-width"
    />
  </q-form>
</template>

<script>
import { ref } from "vue";

export default {
  name: "LoginForm",
  setup() {
    const loginInfo = ref({
      email: "",
      password: "",
    });

    function login() {
      console.log(loginInfo.value);
    }

    return {
      loginInfo,
      login,
    };
  },
};
</script>

<style lang="scss" scoped>
.login-form {
  margin-top: 20px;
  .q-field {
    margin: 5px 0 0;
  }
  .q-btn {
    margin-top: 20px;
    width: 100%;
    height: 50px;
  }
}
</style>
