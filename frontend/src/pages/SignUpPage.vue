<template>
  <q-page class="flex flex-center q-mx-auto sign-up-page">
    <q-card dense class="full-width">
      <q-card-section>
        <div class="text-h5 text-weight-bold q-mb-xl">Sign Up</div>
        <q-form @submit="signUp" class="full-width q-gutter-y-md">
          <div class="input-container">
            <div class="label">Email</div>
            <q-input
              type="text"
              v-model="signupInfo.email"
              rounded
              outlined
              placeholder="Your Email"
              autofocus
            />
          </div>
          <div class="input-container">
            <div class="label">Name</div>
            <q-input
              type="text"
              v-model="signupInfo.name"
              rounded
              outlined
              placeholder="Your Name"
            />
          </div>
          <div class="input-container">
            <div class="label">Password</div>
            <q-input
              type="password"
              v-model="signupInfo.password"
              rounded
              outlined
              placeholder="Your Password"
            />
          </div>
          <div class="input-container">
            <div class="label">Confirm Password</div>
            <q-input
              type="password"
              v-model="signupInfo.confirn_password"
              rounded
              outlined
              placeholder="Your Confirm Password"
            />
          </div>
          <q-btn
            type="submit"
            rounded
            color="black"
            label="Sign up"
            :disable="
              !signupInfo.email ||
              !signupInfo.name ||
              !signupInfo.password ||
              !signupInfo.confirn_password
            "
          />
        </q-form>
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { Notify } from 'quasar'
import { api } from "@boot/axios";
import { useRouter } from "vue-router";


export default defineComponent({
  name: 'SignUpPage',
  setup() {
    const router = useRouter();
    const signupInfo = ref({
      email: "",
      name: "",
      password: "",
      confirn_password: "",
    });

    function signUp() {
      if (signupInfo.value.password === signupInfo.value.confirn_password) {
        api.post("/sign-up", signupInfo.value).then((res) => {
          if (res.status === 200) {
            router.replace({ name: 'SignUpSuccess'});
          }
        });
      } else {
        Notify.create({
          classes: "toast-message",
          message: "비밀번호를 확인해주세요.",
          color: "negative",
          position: "bottom",
        });
      }
    }
    return {
      signupInfo,
      signUp,
    }

  },
})
</script>

<style lang="scss">
.sign-up-page {
  max-width: 400px;
  .q-card {
    padding: 12px;
    border-radius: 28px;
    .q-card__section {
      background: white;
      padding: 30px 16px;
      .q-form {
        .label {
           font-size: 14px;
           font-weight: 500;
           padding-left: 12px;
        }
        .q-btn {
          margin-top: 20px;
          width: 100%;
          height: 50px;
        }
      }
    }
  }
}
</style>
