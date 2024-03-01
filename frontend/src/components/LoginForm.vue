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
import { Notify, Cookies } from "quasar";
import { useRouter } from "vue-router";
import { api } from "@boot/axios";

export default {
  name: "LoginForm",
  setup() {
    const router = useRouter();
    const loginInfo = ref({
      email: "",
      password: "",
    });

    function login() {
      api.post("/login", loginInfo.value).then((res) => {
        if (res.status === 200) {
          const user = res.data.user;
          const token = res.data.access_token;
          Cookies.set("user", user, { expires: "1d" });
          Cookies.set("access_token", token, { expires: "1d" });
        }
        router.replace({ name: "Home" });
      }).catch(() => {
        Notify.create({
          classes: "toast-message",
          message: "로그인할 수 없습니다.",
          color: "negative",
          position: "bottom",
        });
      });
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
